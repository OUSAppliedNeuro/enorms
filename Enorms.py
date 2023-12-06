import Tools
import numpy as np

### @Author Tomasz Szczepanski
###
### Implementation of the E-norms method. Creates a containiner with the different datasets used by the method.
### Can be visualized by EnormsDashboard.py

class Enorms:
    def compute_deltas(a_dataset):
        a_deltas = []
        i_counter = 0
        a_deltas.append(0)
        while i_counter < len(a_dataset)-1:
            a_deltas.append(a_dataset[i_counter+1] - a_dataset[i_counter])
            i_counter += 1
        return a_deltas

    def compute_p3(self, a_dataset):
        return np.poly1d(np.polyfit(np.arange(0, len(a_dataset)), a_dataset, 3))

    def get_training_set(self):
        return self.a_set_training

    def get_deltas(self):
        return self.a_deltas

    def get_deltas_moving_average(self):
        return self.a_deltas_moving_average

    def get_training_moving_average(self):
        return self.a_set_training_moving_average

    def get_p3(self):
        return self.a_p3

    def __init__(self, a_set_training, i_window_size):
        self.i_window_size = i_window_size
        self.a_set_training = a_set_training
        self.a_set_training.sort()
        self.a_set_training_moving_average = Tools.get_moving_average(self.a_set_training, min(self.i_window_size, len(self.a_set_training)))
        self.a_deltas = Enorms.compute_deltas(self.a_set_training)
        self.a_deltas_moving_average = Tools.get_moving_average(self.a_deltas, min(self.i_window_size, len(self.a_set_training)))
        self.a_p3 = self.compute_p3(self.a_set_training)