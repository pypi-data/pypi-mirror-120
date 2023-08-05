#
# Class for reversible lithium plating
#
import pybamm
from .base_plating import BasePlating


class ReversiblePlating(BasePlating):
    """Base class for reversible lithium plating.
    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    domain : str
        The domain of the model either 'Negative' or 'Positive'
    x_average : bool
        Whether to use x-averaged variables (SPM, SPMe, etc) or full variables (DFN)

    References
    ----------
    .. [1] SEJ O'Kane, ID Campbell, MWJ Marzook, GJ Offer and M Marinescu. "Physical
           Origin of the Differential Voltage Minimum Associated with Li Plating in
           Lithium-Ion Batteries". Journal of The Electrochemical Society,
           167:090540, 2019

    **Extends:** :class:`pybamm.lithium_plating.BasePlating`
    """

    def __init__(self, param, domain, x_average):
        super().__init__(param, domain)
        self.x_average = x_average
        pybamm.citations.register("OKane2020")

    def get_fundamental_variables(self):
        if self.x_average is True:
            c_plated_Li_av = pybamm.Variable(
                f"{self.domain.capitalize()} electrode lithium plating concentration",
                domain="current collector",
            )
            c_plated_Li = pybamm.PrimaryBroadcast(
                c_plated_Li_av, self.domain.lower() + " electrode"
            )
        else:
            c_plated_Li = pybamm.Variable(
                f"{self.domain.capitalize()} electrode lithium plating concentration",
                domain=self.domain.lower() + " electrode",
                auxiliary_domains={"secondary": "current collector"},
            )

        variables = self._get_standard_concentration_variables(c_plated_Li)

        return variables

    def get_coupled_variables(self, variables):
        param = self.param
        delta_phi = variables[f"{self.domain} electrode surface potential difference"]
        c_e_n = variables[f"{self.domain} electrolyte concentration"]
        T = variables[f"{self.domain} electrode temperature"]
        eta_sei = variables[f"{self.domain} electrode SEI film overpotential"]
        c_plated_Li = variables[
            f"{self.domain} electrode lithium plating concentration"
        ]
        j0_stripping = param.j0_stripping(c_e_n, c_plated_Li, T)
        j0_plating = param.j0_plating(c_e_n, c_plated_Li, T)
        phi_ref = param.U_n_ref / param.potential_scale
        eta_stripping = delta_phi + phi_ref + eta_sei
        eta_plating = -eta_stripping
        prefactor = 1 / (2 * (1 + self.param.Theta * T))
        j_stripping = j0_stripping * pybamm.exp(
            prefactor * eta_stripping
        ) - j0_plating * pybamm.exp(prefactor * eta_plating)

        variables.update(self._get_standard_overpotential_variables(eta_stripping))
        variables.update(self._get_standard_reaction_variables(j_stripping))

        # Update whole cell variables, which also updates the "sum of" variables
        if (
            "Negative electrode lithium plating interfacial current density"
            in variables
            and "Positive electrode lithium plating interfacial current density"
            in variables
            and "Lithium plating interfacial current density" not in variables
        ):
            variables.update(
                self._get_standard_whole_cell_interfacial_current_variables(variables)
            )

        return variables

    def set_rhs(self, variables):
        if self.x_average is True:
            c_plated_Li = variables[
                "X-averaged "
                + self.domain.lower()
                + " electrode lithium plating concentration"
            ]
            j_stripping = variables[
                "X-averaged "
                + self.domain.lower()
                + " electrode lithium plating interfacial current density"
            ]
        else:
            c_plated_Li = variables[
                f"{self.domain} electrode lithium plating concentration"
            ]
            j_stripping = variables[
                f"{self.domain} electrode lithium plating interfacial current density"
            ]

        Gamma_plating = self.param.Gamma_plating
        self.rhs = {c_plated_Li: -Gamma_plating * j_stripping}

    def set_initial_conditions(self, variables):
        if self.x_average is True:
            c_plated_Li = variables[
                "X-averaged "
                + self.domain.lower()
                + " electrode lithium plating concentration"
            ]
        else:
            c_plated_Li = variables[
                f"{self.domain} electrode lithium plating concentration"
            ]
        c_plated_Li_0 = self.param.c_plated_Li_0

        self.initial_conditions = {c_plated_Li: c_plated_Li_0}
