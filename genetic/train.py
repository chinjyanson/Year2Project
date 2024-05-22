import importlib.util
from neural_net import Population
import math
import numpy as np
from utils import pad, mse, add_noise, plot_datas

"""
    Training on model data using genetic algorithm
"""

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# import a module using its name as a string
m = module_from_file("Data", "data/datavis.py")

cycles = m.cycles
data = m.Data()

data.randomise()

previous_cycles = cycles

pop = Population(40, None, 2)
pc = cycles[0][0]

print("actual: ", pc)  

for epoch in range(100):
    preds = []
    
    for num, model in enumerate(pop.models):
        predicted_import_costs = []
        
        for i in range(data.data_points):
            if(i == 0): input = [pc[0], pc[i+1]]
            elif(i == data.data_points-1): input = [pc[i-1], pc[i-2]]
            else: input = [pc[i-1], pc[i+1]]
    
            predicted_import_costs.append(model.query(input)[0][0])

        pop.fitnesses[num] = 1 / mse(pc, predicted_import_costs)
        preds.append(predicted_import_costs)

        # print(f"fitness by {num}: ", pop.fitnesses[num])  

    print(f"Best pred: {preds[np.argmax(pop.fitnesses)]}")

    # print average mse of newest population
    print("Average MSE: ", pop.average_mse())

    plot_datas(pc, preds[np.argmax(pop.fitnesses)])

    # init new population
    pop = Population(40, pop, 2)
