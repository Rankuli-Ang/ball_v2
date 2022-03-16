"""The module contains Prognosticator class."""
import math
from functools import reduce


class Prognosticator:
    """The Prognosticator analyzes all the collected data in the field for analysis,
     processes and predicts the point where the ball will be
      at the end of the field of motion."""

    def __init__(self, world_height: int):
        self.world_height: int = world_height
        self.data: list = []
        self.sample: list = []

        self.peak_steps: list = []
        self.first_peak_index: int = 0
        self.last_peak_index: int = 0

    def collect_data(self, data: tuple) -> None:
        """Saves the received coordinates of the ball to the list."""
        self.data.append(data)

    def sampling(self) -> None:
        """Discards the tails of received data."""

        """When the ball enters and leaves the detection zone,
                the extremes contain noise.
                For this reason, extrema are removed from the sample. """
        self.sample = self.data[3:-1]

    def peaks_determination(self) -> None:
        """Defines all points in a sample with a minimum 'y'."""
        min_y = self.world_height
        current_index = 0

        for step in self.sample:
            if step[1] < min_y:
                min_y = step[1]
                self.peak_steps.clear()
                self.peak_steps.append(step)
                self.first_peak_index = current_index
                self.last_peak_index = current_index
            elif step[1] == min_y:
                self.peak_steps.append(step)
                self.last_peak_index = current_index
            current_index += 1

    def get_lufts(self, slice_graph: list, end_point_index: int):
        """Returns 2 lists of lufts between coordinate points."""

        """Luft is the distance between two points."""
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
            else:
                break
        return lufts_x, lufts_y

    def get_mean_steps(self, lufts_x: list, lufts_y: list):
        """Returns the mean steps in each plane."""
        mean_step_x = reduce(lambda m, n: m + n, lufts_x) / len(lufts_x)
        mean_step_y = reduce(lambda m, n: m + n, lufts_y) / len(lufts_y)
        return mean_step_x, mean_step_y

    def get_number_of_steps_remaining(self, remaining_distance: int, mean_step_x: int):
        """Returns the number of mean steps remaining to the target along the plane 'x'."""
        number_of_steps_remaining = math.ceil(remaining_distance / mean_step_x)
        return number_of_steps_remaining

    def get_mean_difference_of_lufts(self, different_lufts: list) -> float:
        """Returns the mean difference between lufts."""
        differences = []
        counter = 0
        for luft in different_lufts:
            if luft != different_lufts[-1]:
                counter += 1
                next_luft = different_lufts[counter]
                difference = luft - next_luft
                differences.append(difference)

        sum_lufts = 0
        for difference in differences:
            sum_lufts += difference

        result = abs(round((sum_lufts / len(differences)), 1))
        return result

    def get_different_lufts(self, lufts: list) -> list:
        """Return list of different lufts, from list of lufts."""
        different_lufts = []
        for luft in lufts:
            if luft in different_lufts:
                continue
            else:
                different_lufts.append(luft)
        return different_lufts

    def get_mean_number_of_luft_value(self, lufts: list, different_lufts: list) -> int:
        """Returns the value of the mean frequency of occurrence of a single luft."""
        luft_counters = []
        for luft_value in different_lufts:
            counter = 0
            for luft in lufts:
                if luft == luft_value:
                    counter += 1
            luft_counters.append(counter)

        sum_counters = 0
        for counter in luft_counters:
            sum_counters += counter
        mean_number_of_luft_value = round(sum_counters / len(luft_counters))
        return mean_number_of_luft_value

    def ascending_part_analysis(self, world_width: int, ball_radius: int,
                                sample: list,
                                first_peak_index: int) -> int:
        """Predicts the remaining up, plateau,
        and downtrend of the ball and returns the predicted 'y'. """

        """Preparatory phase."""
        end_point_index = first_peak_index
        lufts_x, lufts_y = self.get_lufts(sample, end_point_index)

        mean_step_x, mean_step_y = self.get_mean_steps(lufts_x, lufts_y)
        last_detected_step = self.data[-1]
        remaining_distance = world_width - last_detected_step[0] - ball_radius

        number_of_steps_remaining = self.get_number_of_steps_remaining(remaining_distance, mean_step_x)

        """Luft processing phase."""

        different_lufts_y = self.get_different_lufts(lufts_y)

        mean_number_of_luft_value = self.get_mean_number_of_luft_value(lufts_y, different_lufts_y)

        max_luft_y = max(different_lufts_y)
        max_luft_counter = 0
        for luft in lufts_y:
            if luft == max_luft_y:
                max_luft_counter += 1

        """Remains steps with max luft."""

        transitional_y = last_detected_step[1]
        not_processed_remaining_steps = number_of_steps_remaining

        if max_luft_counter < mean_number_of_luft_value:
            remaining_steps_with_max_luft = mean_number_of_luft_value - max_luft_counter
            if remaining_steps_with_max_luft >= number_of_steps_remaining:
                predicted_y = last_detected_step[1] + (max_luft_y * number_of_steps_remaining)
                return predicted_y
            else:
                transitional_y += remaining_steps_with_max_luft * max_luft_y
                not_processed_remaining_steps -= remaining_steps_with_max_luft

        luft_difference_y = self.get_mean_difference_of_lufts(different_lufts_y)

        """From max_y to zero_y part."""
        if max_luft_y < 0:
            result_luft = max_luft_y
            steps_to_zero = 0
            while result_luft < 0:
                result_luft += luft_difference_y
                steps_to_zero += 1

            double_mean_number_of_luft_value = mean_number_of_luft_value * 2
            if steps_to_zero == 1:
                if not_processed_remaining_steps <= double_mean_number_of_luft_value:
                    predicted_y = transitional_y
                    return predicted_y
                else:
                    not_processed_remaining_steps -= double_mean_number_of_luft_value
            else:
                while steps_to_zero > 1:
                    new_luft = max_luft_y + luft_difference_y
                    if not_processed_remaining_steps >= mean_number_of_luft_value:
                        not_processed_remaining_steps -= mean_number_of_luft_value
                        transitional_y += new_luft * mean_number_of_luft_value
                        if not_processed_remaining_steps <= 0:
                            predicted_y = transitional_y
                            return predicted_y
                    steps_to_zero -= 1
                not_processed_remaining_steps -= double_mean_number_of_luft_value
                if not_processed_remaining_steps <= 0:
                    predicted_y = transitional_y
                    return predicted_y

        """Descending part."""

        different_lufts_reverse = []
        for luft in different_lufts_y:
            new_luft = abs(luft)
            different_lufts_reverse.append(new_luft)

        different_lufts_reverse = sorted(different_lufts_reverse)

        for luft in different_lufts_reverse:
            if not_processed_remaining_steps > mean_number_of_luft_value:
                transitional_y += abs(luft) * mean_number_of_luft_value
                not_processed_remaining_steps -= mean_number_of_luft_value
            elif not_processed_remaining_steps == mean_number_of_luft_value:
                transitional_y += abs(luft) * mean_number_of_luft_value
                predicted_y = transitional_y
                return predicted_y
            else:
                transitional_y += abs(luft) * not_processed_remaining_steps
                predicted_y = transitional_y
                return predicted_y

    def plateau_part_analysis(self, world_width: int, ball_radius: int,
                              sample: list,
                              first_peak_index: int,
                              last_peak: tuple) -> int:
        """Predicts the remaining plateau,
        and downtrend of the ball and returns the predicted_y. """
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
        """Predicts the remaining downtrend of the ball
        and returns the predicted_y. """

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
        """Determines which part of the movement the ball is in,
        predicts further movement and returns the predicted_y."""

        self.sampling()

        """Peak detection part."""
        self.peaks_determination()
        # last_peak = self.get_last_peak(self.peak_steps)
        # last_peak_index = self.get_last_peak_index(self.sample, last_peak)

        """Determining the position of a point on the graph."""
        last_sample_step = self.sample[-1]
        last_sample_step_y = last_sample_step[1]
        previous_sample_step = self.sample[-2]
        previous_sample_step_y = previous_sample_step[1]

        if self.peak_steps[-1][1] < last_sample_step[1]:
            # Point on the descending part of the graph
            predicted_y = self.descending_part_analysis(world_width, ball_radius, self.sample,
                                                        self.last_peak_index)
            return predicted_y

        else:
            if last_sample_step_y == previous_sample_step_y:
                # Point on the plateau part of the graph
                predicted_y = self.plateau_part_analysis(world_width, ball_radius, self.sample,
                                                         self.first_peak_index, self.peak_steps[-1])
                return predicted_y

            else:
                # Point on the ascending part of the graph
                predicted_y = self.ascending_part_analysis(world_width, ball_radius, self.sample,
                                                           self.first_peak_index)
                return predicted_y
