#!/usr/bin/python3

import requests
import json

from typing import List

from client.jobs_serializer import JobsSerializer
from client.jobs_model import JobDescription
from client.get_auth_token import get_access_token

class JobsClient():
    def __init__(self, server_and_port): #='http://127.0.0.1:5001'):
        self.base_url = server_and_port + "/v1/jobs"
        self.base_url_batch = server_and_port + "/v1/jobs_batch"
        
        self.token_type, self.access_token = get_access_token()

    def __add_auth_headers(self, headers=None):     # keep headers=None and not headers={}! See:: https://docs.python-guide.org/writing/gotchas/
        if headers is None:
            headers = {}
            
        headers['Authorization'] = "%s %s" % (self.token_type, self.access_token)
        return headers

    def _for_test_clear_all_jobs(self):
        headers = {'Content-Type': 'application/json'}
        headers = self.__add_auth_headers(headers)
        
        response = requests.request("DELETE", self.base_url, headers=headers)  # , data=json.dumps(payload))
        return response

    def add_job_single(self, job_obj):
        job_dict = JobsSerializer._serialize_job_single_to_dict(job_obj)
        headers = self.__add_auth_headers()
        response = requests.request("POST", self.base_url, json=job_dict, headers=headers)

        # response = requests.request("POST", self.base_url, headers=headers, data=json.dumps(payload))
        result = JobsSerializer._deserialize_job_single(response.text)
        return result
    
    def add_jobs_from_file(self, file_path):
        files = [('file', open(file_path, 'rb'))]
        
        payload = {}
        headers = {}    # setting Content-Type to "application/x-www-form-urlencoded" causes Heroku error
        headers = self.__add_auth_headers(headers)

        # self.base_url_batch2 = "http://test-jobs-api-123123.herokuapp.com:80/v1/jobs_batch"
        # print("2:", self.base_url_batch2)
        # print("o:", self.base_url_batch)

        response = requests.request("POST", self.base_url_batch, headers=headers, data=payload, files=files)
        return response

    def get_job(self, job_id):
        url = self.base_url + "/" + str(job_id)
        # payload = {'foreign_key' : foreign_id}
        headers = {'Content-Type': 'application/json'}
        headers = self.__add_auth_headers(headers)
        response = requests.request("GET", url, headers=headers)
        result = JobsSerializer._deserialize_job_single(response.text)
        return result

    def get_all_jobs(self, page=0, per_page=10, keywords_str="") -> List[JobDescription]:
        '''
        getting 10 jobs at a time
        :param page:
        :param per_page:
        :param keywords_str: strings of keywords, separated by "," ; will search job descriptions with any of these keywords
        :return:
        '''
        payload = {'page': page, 'per_page': per_page, 'keywords' : keywords_str}

        headers = {'Content-Type': 'application/json'}
        headers = self.__add_auth_headers(headers)

        response = requests.request("GET", self.base_url, headers=headers, data=json.dumps(payload))
        results = JobsSerializer._deserialize_jobs_array(response.text)
        return results


