import math
from functools import reduce


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
        """Defines all points in a sample with a minimum 'y'."""

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
        """Returns first point with a minimum 'y'."""
        first_peak = peak_steps[0]
        return first_peak

    def get_first_peak_index(self, sample: list, first_peak: tuple) -> int:
        """Returns index in simple of first point with a minimum 'y'."""
        counter = 0
        for step in sample:
            if step != first_peak:
                counter += 1
            else:
                return counter

    def get_last_peak(self, peak_steps: list) -> tuple:
        """Returns last point with a minimum 'y'."""
        last_peak = peak_steps[-1]
        return last_peak

    def get_last_peak_index(self, sample: list, last_peak: tuple) -> int:
        """Returns index in simple of last point with a minimum 'y'."""
        counter = 0
        for step in sample:
            if step != last_peak:
                counter += 1
            else:
                return counter

    def get_lufts(self, slice_graph: list, end_point_index: int):
        """Returns 2 lists of lufts between coordinate points."""
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
        print('lx', lufts_x)
        print('ly', lufts_y)
        return lufts_x, lufts_y

    def get_average_steps(self, lufts_x: list, lufts_y: list):
        """Returns the two average steps in each plane."""
        average_step_x = reduce(lambda m, n: m + n, lufts_x) / len(lufts_x)
        average_step_y = reduce(lambda m, n: m + n, lufts_y) / len(lufts_y)
        return average_step_x, average_step_y

    def get_number_of_steps_remaining(self, remaining_distance: int, mean_step_x: int):
        """Returns the number of averaged steps remaining to the target along the plane 'x'."""
        number_of_steps_remaining = math.ceil(remaining_distance / mean_step_x)
        return number_of_steps_remaining

    # terrible naming need to fix

    def get_luft_of_lufts(self, different_lufts: list) -> float:
        """Returns the average difference between lufts."""
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

    def ascending_part_analysis(self, world_width: int, ball_radius: int,
                                sample: list,
                                first_peak_index: int) -> int:
        """Predicts the remaining up, plateau,
        and downtrend of the ball and returns the predicted_y. """

        # unite mean and average

        """Preparatory phase."""
        end_point_index = first_peak_index
        lufts_x, lufts_y = self.get_lufts(sample, end_point_index)

        mean_step_x, mean_step_y = self.get_average_steps(lufts_x, lufts_y)
        print('mean_step_x', mean_step_x)
        last_detected_step = self.data[-1]
        remaining_distance = world_width - last_detected_step[0] - ball_radius
        print('remaining distance', remaining_distance)

        number_of_steps_remaining = self.get_number_of_steps_remaining(remaining_distance, mean_step_x)
        print('number_of_steps_remaining', number_of_steps_remaining)

        # scatter on separate methods

        different_lufts_y = []
        for luft in lufts_y:
            if luft in different_lufts_y:
                continue
            else:
                different_lufts_y.append(luft)
        print('diff lufts', different_lufts_y)

        counters = []
        for luft_value in different_lufts_y:
            counter = 0
            for luft in lufts_y:
                if luft == luft_value:
                    counter += 1
            counters.append(counter)

        sum_counters = 0
        for counter in counters:
            sum_counters += counter
        mean_number_of_luft_value = round(sum_counters / len(counters))

        print('mean number lufts', mean_number_of_luft_value)

        max_luft_y = max(different_lufts_y)
        print('max luft', max_luft_y)
        max_luft_counter = 0
        for luft in lufts_y:
            if luft == max_luft_y:
                max_luft_counter += 1
        print('max_luft_counter', max_luft_counter)

        transitional_y = last_detected_step[1]
        not_processed_remaining_steps = number_of_steps_remaining
        print('first not processed steps', not_processed_remaining_steps)

        if max_luft_counter < mean_number_of_luft_value:
            remaining_steps_with_max_luft = mean_number_of_luft_value - max_luft_counter
            print('remaining s with max luft', remaining_steps_with_max_luft)
            if remaining_steps_with_max_luft >= number_of_steps_remaining:
                predicted_y = last_detected_step[1] + (max_luft_y * number_of_steps_remaining)
                return predicted_y
            else:
                transitional_y += remaining_steps_with_max_luft * max_luft_y
                not_processed_remaining_steps -= remaining_steps_with_max_luft
                print('after max luft not processed steps', not_processed_remaining_steps)

        luft_difference_y = self.get_luft_of_lufts(different_lufts_y)
        print('luft difference', luft_difference_y)

        """From max_y to zero_y part."""
        if max_luft_y < 0:
            result_luft = max_luft_y
            steps_to_zero = 0
            while result_luft < 0:
                result_luft += luft_difference_y
                steps_to_zero += 1
            print('luft steps to zero', steps_to_zero)

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

        print('diff lufts reverse', different_lufts_reverse)

        for luft in different_lufts_reverse:
            if not_processed_remaining_steps > mean_number_of_luft_value:
                transitional_y += abs(luft) * mean_number_of_luft_value
                not_processed_remaining_steps -= mean_number_of_luft_value
                print('not processed steps', not_processed_remaining_steps)
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

        mean_step_x, mean_step_y = self.get_average_steps(lufts_x, lufts_y)

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

        mean_step_x, mean_step_y = self.get_average_steps(lufts_x, lufts_y)

        last_detected_step = self.data[-1]
        remaining_distance = world_width - last_detected_step[0] - ball_radius

        number_of_steps_remaining = self.get_number_of_steps_remaining(remaining_distance, mean_step_x)
        predicted_y = last_detected_step[1] + (mean_step_y * number_of_steps_remaining)
        return predicted_y

    def prognostication(self, world_width: int, world_height: int, ball_radius: int) -> int:
        """Determines which part of the movement the ball is in,
        predicts further movement and returns the predicted_y."""

        """sampling part"""
        sample = self.sampling()

        print('last simple', sample[-1])

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
            predicted_y = self.descending_part_analysis(world_width, ball_radius, sample,
                                                        last_peak_index)
            return predicted_y

        else:
            if last_sample_step_y == previous_sample_step_y:
                # Point on the plateau part of the graph
                predicted_y = self.plateau_part_analysis(world_width, ball_radius, sample,
                                                         first_peak_index, last_peak)
                return predicted_y

            else:
                # Point on the ascending part of the graph
                predicted_y = self.ascending_part_analysis(world_width, ball_radius, sample,
                                                           first_peak_index)
                return predicted_y
