# configuration to show green when the stock is in buy range (0% to 5%)
jscode_buy_range =\
"""
    function(params) {
        if ((params.value > 0) & (params.value < 5)) {
            return {
                'color': 'white',
                'backgroundColor': 'forestgreen'
            }
        } else {
            return {
                'color': 'white',
                'backgroundColor': 'slategray'
            }
        }
    };
"""

# configuration to show green when the stock is in buy range (0% to 5%) and red when the stock is below buy range
jscode_portfolio =\
"""
    function(params) {
        if ((params.value > 0) & (params.value < 5)) {
            return {
                'color': 'white',
                'backgroundColor': 'forestgreen'
            }
        } if (params.value < 0) {
            return {
                'color': 'white',
                'backgroundColor': 'red'
            }
        } else {
            return {
                'color': 'white',
                'backgroundColor': 'slategray'
            }
        }
    };
"""