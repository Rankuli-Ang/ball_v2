from functools import reduce


class Prognosticator:

    def __init__(self):
        self.data: list = []
        self.prognosis = None

    def collect_data(self, data: tuple) -> None:
        """Saves the received coordinates of the ball to the list."""
        self.data.append(data)

    def prognostication(self, world_height: int, ball_radius: int) -> int:
        """"""
        """When the ball enters and leaves the detection zone, 
        the extremes contain noise. 
        For this reason, extrema are removed from the sample. """
        sample = self.data[3:-2]
        """Peak detection part."""
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

        if len(peak_steps) == 1:
            last_peak = sample.index(peak_steps[0])
        else:
            last_peak = sample.index(peak_steps[-1])

        """Luft between steps."""
        if last_peak == sample[-1]:
            ascending_graph = sample
            ascending_counter = 0
            lufts_x = []
            lufts_y = []
            for step in ascending_graph:
                if ascending_counter + 1 < len(ascending_graph):
                    next_step = ascending_graph[ascending_counter + 1]
                    step_luft_x = float(next_step[0]) - float(step[0])
                    step_luft_y = float(next_step[1]) - float(step[1])
                    lufts_x.append(step_luft_x)
                    lufts_y.append(step_luft_y)
                    print('sx', step_luft_x)
                    print('sy', step_luft_y)

            print('lx', lufts_x)
            print('ly', lufts_y)

            mean_step_x = reduce(lambda m, n: m + n, lufts_x) / len(lufts_x)
            mean_step_y = reduce(lambda m, n: m + n, lufts_y) / len(lufts_y)
            # run current settings
        else:
            descending_graph = sample[last_peak:]
            print('dg', descending_graph)
            descending_counter = 0
            lufts_x = []
            lufts_y = []
            for step in descending_graph:
                if descending_counter + 1 < len(descending_graph):
                    next_step = descending_graph[descending_counter + 1]
                    step_luft_x = float(next_step[0]) - float(step[0])
                    step_luft_y = float(next_step[1]) - float(step[1])
                    lufts_x.append(step_luft_x)
                    lufts_y.append(step_luft_y)
                    print('sx', step_luft_x)
                    print('sy', step_luft_y)

            print('lx', lufts_x)
            print('ly', lufts_y)

            mean_step_x = reduce(lambda m, n: m + n, lufts_x) / len(lufts_x)
            mean_step_y = reduce(lambda m, n: m + n, lufts_y) / len(lufts_y)

            last_detected_x = sample[-1][0]
            last_detected_y = sample[-1][1]
            analysis_bias = (world_height - ball_radius) - last_detected_x

            number_of_steps_remaining = round(analysis_bias / mean_step_x)
            predicted_y = last_detected_y + (mean_step_y * number_of_steps_remaining)

            return predicted_y
