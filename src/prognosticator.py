

class Prognosticator:

    def __init__(self):
        self.data: list = []
        self.prognosis = None

    def collect_data(self, data: tuple):
        self.data.append(data)

    def prognostication(self, world_height: int):
        min_y = 500
        peak_steps = []
        step_counter = 0

        for step in self.data:
            if step[1] < min_y:
                min_y = step[1]
                peak_steps.clear()
                peak_steps.append(step)
                step_counter += 1

            elif step[1] == min_y:
                peak_steps.append(step)

        if len(peak_steps) == 1:
            first_peak = self.data.index(peak_steps[0])
            last_peak = self.data.index(peak_steps[0])
        else:
            first_peak = self.data.index(peak_steps[0])
            last_peak = self.data.index(peak_steps[-1])





