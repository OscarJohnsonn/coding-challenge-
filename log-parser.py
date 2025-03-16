import csv
from datetime import datetime

class Job:
    def __init__(self, pid, description):
        self.pid = pid
        self.description = description
        self.start_time = None
        self.end_time = None

    def set_start_time(self, timestamp):
        self.start_time = datetime.strptime(timestamp, '%H:%M:%S')

    def set_end_time(self, timestamp):
        self.end_time = datetime.strptime(timestamp, '%H:%M:%S')

class LogProcessor:
    def __init__(self,log_file):
        self.log_file  = log_file
        self.jobs = {}

    def parse_log(self):
        with open(self.log_file, newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                timestamp, description, status, pid = row
                pid = int(pid.strip())  #remove spages , convert to int

                if pid not in self.jobs: #if job not initialised initialise
                    self.jobs[pid] = Job(pid, description.strip())

                job = self.jobs[pid]

                if status.strip() == 'STArT':
                    job.set_start_time(timestamp.strip())
                elif status.strip() == 'END':
                    job.set_end_time(timestamp.strip())


#example
if __name__ == "__main__":
    log_processor = LogProcessor('logs.log')
    log_processor.parse_log()