import json
import pandas as pd
from classes.classes import Scenario, ProductionPlan
from classes.operator import Operator
from classes.simulator_7 import Simulator
import numpy as np
from numpy import random
from matplotlib import pyplot as plt

# Settings
instance_size = 10
instance_id = 1
cp_output = 'feasible'
nr_scenarios = 10
scenario_seeds = random.randint(100000, size=nr_scenarios)
policy_type = 2
printing = True

# Read CP output and convert
instance_name = f"{instance_size}_{instance_id}_factory_1"
file_name = instance_name if cp_output == 'feasible' else f"{instance_name}_infeasible"
cp_output = pd.read_csv(f"results/cp_model/development/instances_type_2/start times {file_name}.csv", delimiter=",")
print(f'Makespan according to CP outout is {max(cp_output["end"].tolist())}')
earliest_start = cp_output.to_dict('records')


evaluation = []
for seed in scenario_seeds:
    # Read input instance
    my_productionplan = ProductionPlan(
        **json.load(open('factory_data/development/instances_type_2/instance_' + instance_name + '.json')))
    my_productionplan.set_earliest_start_times(earliest_start)
    my_productionplan.set_sequence(sequence=np.arange(instance_size))
    scenario_1 = my_productionplan.create_scenario(seed)

    # Set printing to True if you want to print all events
    operator = Operator(plan=scenario_1.production_plan, policy_type=policy_type, printing=False)
    my_simulator = Simulator(plan=scenario_1.production_plan, operator=operator, printing=False)

    # Run simulation
    makespan, lateness, nr_unfinished = my_simulator.simulate(sim_time=2000, write=False, output_location=f""
    f"simulators/simulator7/outputs/example_cp_output_to_simulator.csv")
    if printing:
        print(f'Run simulation for a scenario for instance {instance_name}')
        print(f'According to the simulation, the makespan is {makespan} and the lateness is {lateness}')
        print(f'The number of unfinished products {nr_unfinished}')
        print(f'The number of clashes (i.e. activities that could not be processed) is {my_simulator.nr_clashes}')

    evaluation.append({"seed": seed,
                       "makespan": makespan,
                       "lateness": lateness,
                       "nr_unfinished_products": nr_unfinished})


evaluation = pd.DataFrame(evaluation)
evaluation.to_csv(f"simulators/simulator7/outputs/evaluation_table_{instance_name}_policy={policy_type}.csv")
