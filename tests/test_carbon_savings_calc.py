from src.carbon_savings_calc import eval_electric


def test_eval_electric():
    assert eval_electric() == ({'co2_lbs_reduction': 3360.0,
                                'comp_cost': 859.7,
                                'cost_dollars': 570.13,
                                'CO2_total_electric': 3974,
                                'CO2_total_gasoline': 7334})
    assert eval_electric(mpg=25) == ({'co2_lbs_reduction': 6587.0,
                                      'comp_cost': 1706.05,
                                      'cost_dollars': 1138.37,
                                      'CO2_total_electric': 3974,
                                      'CO2_total_gasoline': 10561})
