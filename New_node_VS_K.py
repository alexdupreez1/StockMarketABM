import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Experiment import Experiment
from tqdm import tqdm

def run_experiment(params):
    """
    Run an experiment with the given parameters and return the result.

    Parameters:
    ----------
    params : dict
        Dictionary containing the parameters for the experiment.

    Returns:
    -------
    float
        Result of the fat tail experiment.
    """
    exp = Experiment(
        initial_price=0,
        time_steps=500,
        network_type='barabasi',
        number_of_traders=params['number_of_traders'],
        percent_fund=0.5,
        percent_chartist=0.5,
        percent_rational=params['percent_rational'],
        percent_risky=params['percent_risky'],
        high_lookback=params['high_lookback'],
        low_lookback=1,
        high_risk=params['high_risk'],
        low_risk=0.01,
        new_node_edges=params['new_node_edges'],
        connection_probability=0.5,
        mu=0.01,
        beta=1,
        alpha_w=2668,
        alpha_O=2.1,
        alpha_p=0
    )
    market = exp.run_simulation()
    return exp.fat_tail_experiment(500, market.prices)  # Assuming the Experiment class has a fat_tail_experiment method

# Default parameters for the experiment
default_params = {
    'number_of_traders': 150,
    'percent_rational': 0.1,
    'percent_risky': 0.1,
    'high_lookback': 15,
    'high_risk': 0.2,
    'new_node_edges': 5
}

# Parameter to vary - new node edges
new_node_edges = np.arange(1, 10, 1)  # From 1 to 10 in steps of 1

# Record results for analysis
avg_result = []
ci_upper = []
ci_lower = []

# Iterate over the range of new node edges
for num in tqdm(new_node_edges):
    results = []
    for _ in range(30):
        params = default_params.copy()
        params['new_node_edges'] = num
        result = run_experiment(params)
        results.append(result)
    avg_result.append(np.mean(results))
    ci_upper.append(np.percentile(results, 97.5))
    ci_lower.append(np.percentile(results, 2.5))

# Plotting the results
plt.plot(new_node_edges, avg_result, label='Average Result')
plt.plot(new_node_edges, ci_upper, linestyle='--', color='gray', label='95% CI Upper')
plt.plot(new_node_edges, ci_lower, linestyle='--', color='gray', label='95% CI Lower')
plt.fill_between(new_node_edges, ci_lower, ci_upper, color='gray', alpha=0.5, label='95% CI')
plt.xlabel('New Node Edges')
plt.ylabel('Fat Tail Experiment Result')
plt.legend()
plt.tight_layout()
plt.savefig('new_node_edge_sensitivity.jpeg')
plt.show()
