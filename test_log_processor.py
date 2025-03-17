import unittest
import os
import tempfile
from log_processor import LogProcessor, Job

class TestLogProcessor(unittest.TestCase):
    def setUp(self):
        #create a temporary log file 
        self.temp_log = tempfile.NamedTemporaryFile(delete=False, suffix='.log')
        self.temp_log.close()
    
    def tearDown(self):
        #clean up temporary file
        os.unlink(self.temp_log.name)
    
    def test_job_duration_calculation(self):
        job = Job(12345, "Test Job")
        job.set_start_time("10:00:00")
        job.set_end_time("10:05:30")
        
        self.assertEqual(job.get_duration(), 330)  #5 min 30 sec
        self.assertTrue(job.is_warning())
        self.assertFalse(job.is_error())
    
    def test_parse_complete_job(self):
        #write log content
        with open(self.temp_log.name, 'w') as f:
            f.write("10:00:00, Test Job, START, 12345\n10:05:30, Test Job, END, 12345")
        
        processor = LogProcessor(self.temp_log.name)
        processor.parse_log()
        
        self.assertEqual(len(processor.jobs), 1)
        self.assertEqual(processor.jobs[12345].get_duration(), 330)
        self.assertEqual(len(processor.incomplete_jobs), 0)
    
    def test_incomplete_job(self):
        #write test log content with incomplete job
        with open(self.temp_log.name, 'w') as f:
            f.write("10:00:00, Test Job, START, 12345")
        
        processor = LogProcessor(self.temp_log.name)
        processor.parse_log()
        
        self.assertEqual(len(processor.incomplete_jobs), 1)
        self.assertTrue(12345 in processor.incomplete_jobs)
    
    def test_overlapping_job(self):
        #write test log content with overlapping job
        with open(self.temp_log.name, 'w') as f:
            f.write("10:00:00, Job 1, START, 1001\n10:01:00, Job 1, START, 1001")
        
        processor = LogProcessor(self.temp_log.name)
        processor.parse_log()
        
        self.assertEqual(len(processor.overlapping_jobs), 1)
        self.assertTrue(1001 in processor.overlapping_jobs)

if __name__ == '__main__':
    unittest.main()
