import math
from functools import reduce
from math import ceil


class Prognosticator:

    def __init__(self):
        self.data: list = []

    def collect_data(self, data: tuple) -> None:
        """Saves the received coordinates of the ball to the list."""
        self.data.append(data)

    def sampling(self) -> list:
        """Discards the tails of received data."""

        """When the ball enters and leaves the detection zone,
                the extremes contain noise.
                For this reason, extrema are removed from the sample. """
        sample = self.data[3:-1]
        return sample

    def peaks_determination(self, world_height: int, sample: list) -> list:
        min_y = world_height
        peak_steps = []
        step_counter = 0

        for step in sample:
            if step[1] < min_y:
                min_y = step[1]
                peak_steps.clear()
                peak_steps.append(step)
                step_counter += 1

            elif step[1] == min_y:
                peak_steps.append(step)

        return peak_steps

    def get_first_peak(self, peak_steps: list) -> tuple:
        first_peak = peak_steps[0]
        return first_peak

    def get_first_peak_index(self, sample: list, first_peak: tuple) -> int:
        counter = 0
        for step in sample:
            if step != first_peak:
                counter += 1
            else:
                return counter

    def get_last_peak(self, peak_steps: list) -> tuple:
        last_peak = peak_steps[-1]
        return last_peak

    def get_last_peak_index(self, sample: list, last_peak: tuple) -> int:
        counter = 0
        for step in sample:
            if step != last_peak:
                counter += 1
            else:
                return counter

    def get_lufts(self, slice_graph: list, end_point_index: int):
        slice_graph_counter = 0
        lufts_x = []
        lufts_y = []
        for step in slice_graph:
            if slice_graph_counter != end_point_index:
                if slice_graph_counter + 1 < end_point_index:
                    next_step = slice_graph[slice_graph_counter + 1]
                    step_luft_x = float(next_step[0]) - float(step[0])
                    step_luft_y = float(next_step[1]) - float(step[1])
                    lufts_x.append(step_luft_x)
                    lufts_y.append(step_luft_y)
                    slice_graph_counter += 1
                    print('sx', step_luft_x)
                    print('sy', step_luft_y)
            else:
                break

        return lufts_x, lufts_y

    def get_mean_steps(self, lufts_x: list, lufts_y: list):
        mean_step_x = reduce(lambda m, n: m + n, lufts_x) / len(lufts_x)
        mean_step_y = reduce(lambda m, n: m + n, lufts_y) / len(lufts_y)
        return mean_step_x, mean_step_y

    def get_number_of_steps_remaining(self, remaining_distance: int, mean_step_x: int):
        number_of_steps_remaining = math.ceil(remaining_distance / mean_step_x)
        return number_of_steps_remaining

    def ascending_part_analysis(self):
        pass

    def plateau_part_analysis(self, world_width: int, ball_radius: int,
                              sample: list,
                              first_peak_index: int,
                              last_peak: tuple) -> int:
        end_point_index = first_peak_index
        lufts_x, lufts_y = self.get_lufts(sample, end_point_index)

        mean_step_x, mean_step_y = self.get_mean_steps(lufts_x, lufts_y)

        last_sample_step = sample[-1]
        last_detected_step = self.data[-1]
        if last_peak == last_sample_step:
            remaining_distance = world_width - last_detected_step[0] - ball_radius

            number_of_steps_remaining = self.get_number_of_steps_remaining(remaining_distance, mean_step_x)

            max_step_y = max(lufts_y)
            lufts_y_without_max = []
            for step in lufts_y:
                if step < max_step_y:
                    lufts_y_without_max.append(step)

            previous_max_step_y = max(lufts_y_without_max)
            mean_extreme_step = (max_step_y + previous_max_step_y) / 2

            calculated_deviation_y = last_detected_step[1] - (mean_extreme_step * number_of_steps_remaining)
            return calculated_deviation_y

    def descending_part_analysis(self, world_width: int, ball_radius: int,
                                 sample: list, last_peak_index: int) -> int:

        descending_graph = sample[last_peak_index:]
        end_point_index = len(descending_graph)
        lufts_x, lufts_y = self.get_lufts(descending_graph, end_point_index)

        mean_step_x, mean_step_y = self.get_mean_steps(lufts_x, lufts_y)

        last_detected_step = self.data[-1]
        remaining_distance = world_width - last_detected_step[0] - ball_radius

        number_of_steps_remaining = self.get_number_of_steps_remaining(remaining_distance, mean_step_x)
        predicted_y = last_detected_step[1] + (mean_step_y * number_of_steps_remaining)
        return predicted_y

    def prognostication(self, world_width: int, world_height: int, ball_radius: int) -> int:
        """"""

        """sampling part"""
        sample = self.sampling()

        print('ls', sample[-1])

        """Peak detection part."""
        peaks_steps = self.peaks_determination(world_height, sample)
        first_peak = self.get_first_peak(peaks_steps)
        first_peak_index = self.get_first_peak_index(sample, first_peak)
        last_peak = self.get_last_peak(peaks_steps)
        last_peak_index = self.get_last_peak_index(sample, last_peak)

        """Determining the position of a point on the graph."""
        last_sample_step = sample[-1]
        last_sample_step_y = last_sample_step[1]
        previous_sample_step = sample[-2]
        previous_sample_step_y = previous_sample_step[1]

        if last_peak[1] < last_sample_step[1]:
            # Point on the descending part of the graph
            predicted_y = self.descending_part_analysis(world_width, ball_radius,
                                                        sample, last_peak_index)
            return predicted_y

        else:
            if last_sample_step_y == previous_sample_step_y:
                # Point on the plateau part of the graph
                predicted_y = self.plateau_part_analysis(world_width, ball_radius,
                                                         sample,
                                                         first_peak_index,
                                                         last_peak)
                return predicted_y

            else:
                # Point on the ascending part of the graph
                pass
