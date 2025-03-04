import json
from classes.classes import ProductionPlan, STN
import numpy as np
import pandas as pd

instance_size = 10
instance_id = 1
instance_name = f"{instance_size}_{instance_id}_factory_1"
my_productionplan = ProductionPlan(
    **json.load(open('factory_data/development/instances_type_2/instance_' + instance_name + '.json')))

stn = STN.from_production_plan(my_productionplan)

print(f'Apply Floyd-Warshall to STN without resource constraints')
shortest_distances = stn.floyd_warshall()
print(f'Makespan: {-shortest_distances[stn.HORIZON_IDX, stn.ORIGIN_IDX]}')

# Load cp output and make production plan and convert to edges that must be added to STN
from get_resource_chains import get_resource_chains
cp_output = pd.read_csv(f"results/cp_model/development/instances_type_2/start times {instance_name}.csv")
earliest_start = cp_output.to_dict('records')  # Convert to earliest start times
# Run deterministic simulation with earliest start times and obtain resource predecence constraints
resource_chains = get_resource_chains(production_plan=my_productionplan, earliest_start=earliest_start)

# Now add the edges with the correct edge weights to the STN
for pred_p, pred_a, succ_p, succ_a in resource_chains:
    # The finish of the predecessor should precede the start of the successor
    pred_idx = stn.translation_dict_reversed[(pred_p, pred_a, STN.EVENT_FINISH)]  # Get translation index from finish of predecessor
    suc_idx = stn.translation_dict_reversed[(succ_p, succ_a, STN.EVENT_START)]  # Get translation index from start of successor
    stn.add_interval_constraint(pred_idx, suc_idx, 0, np.inf)

print(f'Apply Floyd-Warshall to STN WITH resource constraints')
# Compute shortest distance graph path for this graph
shortest_distances = stn.floyd_warshall()
print(f'Makespan: {-shortest_distances[stn.HORIZON_IDX, stn.ORIGIN_IDX]}')
