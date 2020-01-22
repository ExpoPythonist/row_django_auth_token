#!/usr/bin/python3
import os

import unittest
from unittest import skip

from client.jobs_client import JobsClient
from client.jobs_serializer import JobsSerializer


class TestSqlAlchemy(unittest.TestCase):
    def setUp(self):
        server_and_port = os.environ['SERVER_AND_PORT']
        # self.base_url = server_and_port + "/results"
        # self.client_results = ClientResultsSqlAlchemy(server_and_port)
        # self.client_votes = ClientVotesSqlAlchemy(server_and_port)
        self.client_jobs = JobsClient(server_and_port)

        from pathlib import Path
        base_module_path = os.path.dirname(Path(os.path.abspath(__file__)).parent)
        self.file_26_jobs_path = os.path.join(base_module_path, r'resources', r'jobs_greenhouse_26_jobs.jl')
        
        # make sure file exists
        self.assertTrue(os.path.isfile(self.file_26_jobs_path))
        
    def helper_clear_database(self):
        self.client_jobs._for_test_clear_all_jobs()

    @skip
    def test_add_single_job(self):
        self.helper_clear_database()
    
        job_str1 = '{"found_url": "https://www.acme.com/acme/", "full_description": "job desc 1 java python", "job_location": "New York, NY", "job_title": "Job Title 1", "job_url": "https://www.acme.com/acme/jobs/url_1", "seen_time_epoch": 1577549228, "short_description": "", "tags_string": ""}'
        job_obj1 = JobsSerializer._deserialize_job_single(job_str1)
        job_added1 = self.client_jobs.add_job_single(job_obj1)
    
        self.assertEqual(job_obj1.job_url, job_added1.job_url)
        self.assertEqual(job_obj1.job_title, job_added1.job_title)
        self.assertEqual(job_obj1.full_description, job_added1.full_description)
        self.assertEqual(job_obj1.short_description, job_added1.short_description)
        self.assertEqual(job_obj1.tags_string, job_added1.tags_string)
        self.assertEqual(job_obj1.found_url, job_added1.found_url)
        self.assertEqual(job_obj1.seen_time_epoch, job_added1.seen_time_epoch)
    
    def test_add_jobs_from_file(self):
        self.client_jobs.add_jobs_from_file(self.file_26_jobs_path)

    @skip("this test can not be run on production since it tries to delete the database")
    def test_get_all_jobs(self):
        self.helper_clear_database()

        self.client_jobs.add_jobs_from_file(self.file_26_jobs_path)
        
        jobs_ids = set()
        page = 0
        jobs_from_db = self.client_jobs.get_all_jobs(page=page)
        while len(jobs_from_db) > 0:
            print("got jobs with page [%d]" % (page))
            for job in jobs_from_db:
                jobs_ids.add(job.id)
                
            page += 1
            jobs_from_db = self.client_jobs.get_all_jobs(page=page)

        print("len(jobs_ids) len: %d" % (len(jobs_ids)))
        self.assertEqual(26, len(jobs_ids))

    @skip("this is not production ready test")
    def test_get_jobs_with_keywords(self):
        # self.helper_clear_database()
        
        job_str1 = '{"found_url": "https://www.acme.com/acme/", "full_description": "job desc 1 java python", "job_location": "New York, NY", "job_title": "Job Title 1", "job_url": "https://www.acme.com/acme/jobs/url_1", "seen_time_epoch": 1577549228, "short_description": "", "tags_string": ""}'
        job_obj1 = JobsSerializer._deserialize_job_single(job_str1)
        job_added1 = self.client_jobs.add_job_single(job_obj1)
        
        job_str2 = '{"found_url": "https://www.acme.com/acme/", "full_description": "job desc 2 java", "job_location": "New York, NY", "job_title": "Job Title 2", "job_url": "https://www.acme.com/acme/jobs/url_2", "seen_time_epoch": 1577549228, "short_description": "", "tags_string": ""}'
        job_obj2 = JobsSerializer._deserialize_job_single(job_str2)
        job_added2 = self.client_jobs.add_job_single(job_obj2)
        
        job_str3 = '{"found_url": "https://www.acme.com/acme/", "full_description": "job desc 3 python", "job_location": "New York, NY", "job_title": "Job Title 3", "job_url": "https://www.acme.com/acme/jobs/url_3", "seen_time_epoch": 1577549228, "short_description": "", "tags_string": ""}'
        job_obj3 = JobsSerializer._deserialize_job_single(job_str3)
        job_added3 = self.client_jobs.add_job_single(job_obj3)

        jobs_java = self.client_jobs.get_all_jobs(keywords_str='java')
        jobs_python = self.client_jobs.get_all_jobs(keywords_str='  python')                    # space intended
        jobs_java_or_python = self.client_jobs.get_all_jobs(keywords_str='python, java  ')      # space intended
        
        self.assertEqual(2, len(jobs_java))
        self.assertEqual(2, len(jobs_python))
        self.assertEqual(3, len(jobs_java_or_python))

        for job in jobs_java:
            self.assertTrue('java' in job.full_description)
        for job in jobs_python:
            self.assertTrue('python' in job.full_description)
        for job in jobs_java_or_python:
            self.assertTrue(('java' in job.full_description) or ('python' in job.full_description))
            

