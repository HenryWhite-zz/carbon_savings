
# Set constants
# Average miles driven per year
# noqa Source: https://policyadvice.net/insurance/insights/how-much-do-americans-drive/
annual_miles_avg = 13476

# Average cost per gallon
# noqa Source: https://www.officialdata.org/gasoline-%28all-types%29/price-inflation/2022-to-2022
cost_per_gallon_gasoline_avg = 3.45

# Average cost per kWh
# noqa Source: https://www.eia.gov/electricity/monthly/update/
cost_per_kWh_avg = .1547

# Average kilowatt-hours per mile for electric cars
# Source: https://ecocostsavings.com/average-electric-car-kwh-per-mile/
kpm_avg = .346

# Average miles per gallon for gasoline cars
# Source: https://www.cnn.com/2022/04/01/energy/fuel-economy-rules/index.html
mpg_avg = 36

# Conversions
# noqa Source for pounds conversions: https://www.rapidtables.com/convert/weight/ton-to-pound.html
pounds_per_metric_ton = 2204.6226218

# Social cost of carbon
# According to middle value in EPA proposal 2022
# noqa Source: https://www.americanenergyalliance.org/2022/11/bidens-epa-reveals-astronomical-social-cost-of-carbon-proposal/
social_cost_CO2_metric_ton = 190.00
social_cost_CO2_lbs = social_cost_CO2_metric_ton/pounds_per_metric_ton

# CO2 from gasoline
# Source for CO2_from_gas: (https://www.epa.gov/energy/
# greenhouse-gases-equivalencies-calculator-calculations-and-references)
CO2_from_gallon_gasoline_metric_tons = .008887
CO2_from_gallon_gasoline_lbs = (
    CO2_from_gallon_gasoline_metric_tons * pounds_per_metric_ton)

# Average CO2 Per MWh
# Source: https://www.epa.gov/egrid/power-profiler#/
CO2_per_MWh_avg = 852.3

# Pounds of CO2 emitted per kWh produced for various fuel types
# Source: https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
CO2_by_fuel_type = {}
CO2_by_fuel_type['Solar'] = 0
CO2_by_fuel_type['Petroleum'] = 2.44
CO2_by_fuel_type['Hydro'] = 0
CO2_by_fuel_type['Natural gas'] = .97
CO2_by_fuel_type['Coal'] = 2.26
CO2_by_fuel_type['Wind'] = 0
