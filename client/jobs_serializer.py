#!/usr/bin/python3

import json
from typing import List, Dict
from marshmallow import fields

from alchem import ma
from client.jobs_model import JobDescription


class JobSchema(ma.Schema):
    # https://realpython.com/flask-connexion-rest-api-part-2/
    
    id = fields.Int()
    job_url = fields.Str()
    found_url = fields.Str()
    job_title = fields.Str()
    job_location = fields.Str(required=False, default="")
    short_description = fields.Str(required=False, default="")
    full_description = fields.Str(required=False, default="")
    tags_string = fields.Str(required=False, default="")
    # seen_time_epoch = fields.Integer(required=False)
    seen_time_epoch = fields.Int()
    
    # class Meta:
    #     fields = ("id", "job_url", "found_url", "job_title", "job_location", "short_description", "full_description",
    #               "tags_string", "seen_time_epoch")


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

class JobsSerializer():
    
    @staticmethod
    def _serialize_job_single(job_object: JobDescription) -> str:
        job_json_str = job_schema.dumps(job_object)
        return job_json_str
    
    @staticmethod
    def _serialize_job_single_to_dict(job_object: JobDescription) -> Dict:
        job_json_str = job_schema.dump(job_object)
        return job_json_str
    
    @staticmethod
    def _job_dict_to_obj(result_dict) -> JobDescription:
        job_obj = JobDescription()

        # if it's not from db, we have no "id" field
        if 'id' in result_dict.keys():
            job_obj.id = result_dict['id']
        
        if 'job_url' in result_dict.keys():                 job_obj.job_url = result_dict['job_url']
        if 'found_url' in result_dict.keys():               job_obj.found_url = result_dict['found_url']
        if 'job_title' in result_dict.keys():               job_obj.job_title = result_dict['job_title']
        if 'job_location' in result_dict.keys():            job_obj.job_location = result_dict['job_location']
        if 'short_description' in result_dict.keys():       job_obj.short_description = result_dict['short_description']
        if 'full_description' in result_dict.keys():        job_obj.full_description = result_dict['full_description']
        if 'tags_string' in result_dict.keys():             job_obj.tags_string = result_dict['tags_string']
        if 'seen_time_epoch' in result_dict.keys():         job_obj.seen_time_epoch = result_dict['seen_time_epoch']
        
        return job_obj

    @staticmethod
    def _deserialize_job_single(s: str) -> JobDescription:
        # delete None values
        d = json.loads(s)
        keys_to_del = []
        for k,v in d.items():
            if v is None:
                keys_to_del.append(k)
        for k in keys_to_del:
            del d[k]
                
        # job_dict = job_schema.loads(s, partial=True) # partial=('job_location','short_description','full_description','tags_string',))
        job_dict = job_schema.load(d, partial=True) # partial=('job_location','short_description','full_description','tags_string',))
        # job_obj = self._job_dict_to_obj(job_dict)
        job_obj = JobsSerializer._job_dict_to_obj(job_dict)
        return job_obj
    
    @staticmethod
    def trim_fields(job_obj : JobDescription):
        if job_obj.found_url is not None and len(job_obj.found_url) > 512:
            job_obj.found_url = job_obj.found_url[:512]
        
        if job_obj.job_location is not None and len(job_obj.job_location) > 512:
            job_obj.job_location = job_obj.job_location[:512]
            
        if job_obj.short_description is not None and len(job_obj.short_description) > 512:
            job_obj.short_description = job_obj.short_description[:512]
            
        if job_obj.full_description is not None and len(job_obj.full_description) > 10000:
            job_obj.full_description = job_obj.full_description[:10000]
            
        if job_obj.tags_string is not None and len(job_obj.tags_string) > 512:
            job_obj.tags_string = job_obj.tags_string[:512]
            
    
    @staticmethod
    def _deserialize_jobs_array(s: str) -> List[JobDescription]:
        results = jobs_schema.loads(s)
        jobs_objs = []
        for result_dict in results:
            job_obj = JobsSerializer._job_dict_to_obj(result_dict)
            jobs_objs.append(job_obj)
        
        return jobs_objs
