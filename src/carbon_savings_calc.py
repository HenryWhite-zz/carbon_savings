import numpy as np

# Local imports
import src.constants as constants


def eval_electric(mpg=constants.mpg_avg,
                  annual_miles=constants.annual_miles_avg,
                  gas_cost=constants.cost_per_gallon_gasoline_avg,
                  kpm=constants.kpm_avg,
                  cost_per_kwh=constants.cost_per_kWh_avg,
                  CO2_per_MWh_lbs=constants.CO2_per_MWh_avg
                  ):
    """
    Evaluate the carbon emissions reduction and cost savings in switching
    from a gasoline car to an electric car.

    Args:
        mpg (float): Miles per gallon of gasoline car. Default is `mpg_avg`.
        annual_miles (int): Miles driven per year. Default is
                            `annual_miles_avg`.
        gas_cost (float): Cost of a gallon of gasoline in U.S. dollars.
                        Default is `cost_per_gallon_gasoline_average`.
        kpm (float): Kilowatt-hours per mile of electric car. Default is
                    `kpm_avg`.
        cost_per_kwh (float): Cost of 1 kWh electricity.
        C02_per_MWh_lbs: Pounds of CO2 emitted by 1 MWh electricity.

    Returns:
        dict: A dictionary containing the following key-value pairs:
            - 'co2_lbs_reduction' (float): The pounds of CO2 emissions saved by
                                switching to an electric car.
            - 'cost_dollars' (float): The fuel cost savings in dollars by
                                    switching to an electric car.
            - 'comp_cost' (float): The comprehensive cost savings in dollars
                                by switching to an electric car, including
                                the social cost of carbon.
            - 'CO2_total_electric' (float): Total CO2 emissions from electric
                                            vehicle.
            - 'CO2_total_gas' (float): Total CO2 emissions from gas
                                            vehicle.
    """
    # Instantiate savings
    savings = {}

    # Calcuate CO2 emissions per vehicle
    CO2_lbs_per_kwh = CO2_per_MWh_lbs/1000

    savings['CO2_total_electric'] = np.round(kpm
                                             * CO2_lbs_per_kwh
                                             * annual_miles)
    savings['CO2_total_gasoline'] = np.round(constants.CO2_from_gallon_gasoline_lbs  # noqa
                                             * (annual_miles/mpg))
    savings['co2_lbs_reduction'] = np.round(savings['CO2_total_gasoline'] -
                                            savings['CO2_total_electric'])

    # Calculate cost savings
    cost_electric = cost_per_kwh * kpm * annual_miles
    cost_gasoline = gas_cost * annual_miles/mpg
    savings['cost_dollars'] = np.round(cost_gasoline - cost_electric, 2)

    # Calculate savings with social cost of carbon
    savings['comp_cost'] = np.round((savings['cost_dollars'] +
                                     (constants.social_cost_CO2_lbs *
                                      savings['co2_lbs_reduction'])), 2)

    return savings
