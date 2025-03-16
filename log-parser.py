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
    
    def get_duration(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).seconds
        return 0
    
    def is_warning(self):
        return self.get_duration() > 300  #warning if > 5 min

    def is_error(self):
        return self.get_duration() > 600  #error if > 10 min
    
    def is_complete(self):
        return self.start_time is not None and self.end_time is not None
    
    def is_short(self):
        return self.is_complete() and self.get_duration() < 20  #< 20 seconds
    
    def is_long(self):
        return self.is_complete() and self.get_duration() > 1800  #> 30 minutes
    

class LogProcessor:
    def __init__(self,log_file):
        self.log_file  = log_file
        self.jobs = {}
        self.overlapping_jobs = []
        self.incomplete_jobs = []

    def parse_log(self):
        active_jobs = set() #tracks current jobs

        with open(self.log_file, newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                timestamp, description, status, pid = row
                pid = int(pid.strip())  #remove spages , convert to int

                if pid not in self.jobs: #if job not initialised initialise
                    self.jobs[pid] = Job(pid, description.strip())

                job = self.jobs[pid]

                if status.strip() == 'START':
                    job.set_start_time(timestamp.strip())
                    #checks for overlapping jobs
                    if pid in active_jobs:
                        self.overlapping_jobs.append(pid)
                    active_jobs.add(pid)
                elif status.strip() == 'END':
                    job.set_end_time(timestamp.strip())
                    if pid in active_jobs:
                        active_jobs.remove(pid)


        for pid, job in self.jobs.items():#to find incomplete , no start end
            if not job.is_complete():
                self.incomplete_jobs.append(pid)
    
    def generate_report(self):
        for job in self.jobs.values():
            duration = job.get_duration()
            if job.is_error():
                print(f"ERROR: Job {job.pid} - {job.description} took {duration} seconds (longer than 10 minutes).")
            elif job.is_warning():
                print(f"WARNING: Job {job.pid} - {job.description} took {duration} seconds (longer than 5 minutes).")
            else:
                print(f"Job {job.pid} - {job.description} took {duration} seconds.")
            
        print(f"\nOverlapping jobs: {self.overlapping_jobs}")
        print(f"Incomplete jobs: {self.incomplete_jobs}")

    def print_logs(self):
        for job in self.jobs.values():
            print(f"{job.pid}: {job.description} | Start: {job.start_time} | End: {job.end_time} | Duration: {job.get_duration()} seconds")
            


#example
if __name__ == "__main__":
    log_processor = LogProcessor('logs.log')
    log_processor.parse_log()
    log_processor.generate_report()
