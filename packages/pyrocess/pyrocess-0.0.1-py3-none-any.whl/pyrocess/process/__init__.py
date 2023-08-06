from pyrocess.strategies import ExpensiveIOStrategy as _ExpensiveIOStrategy


class ProcessingContext:
    def __init__(self, callbacks, strategy=_ExpensiveIOStrategy):
        self.callbacks = callbacks
        self.strategy = strategy

    def execute(self, bacthes: int = 128):
        for step in range(0, len(self.callbacks), bacthes):
            processes = []

            for callback in self.callbacks[step : step + bacthes]:
                process = self.strategy(target=callback)
                process.start()

                processes.append(process)

            self.execute_process_patch(processes)

    def execute_process_patch(self, processes):
        for process in processes:
            process.join()
