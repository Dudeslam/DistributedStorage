
class MetricLog:
    def __init__(self, log_path):
        self.log_path = log_path
        self.current_run = 0
        f = open(self.log_path, "w")
        f.write("run, time \n")
        f.close()


    def log_entry(self, time):
        f = open(self.log_path, "a+")
        self.current_run += 1
        f.write(f"{self.current_run}, {time} \n")
        f.close()



