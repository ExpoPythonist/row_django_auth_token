#!/usr/bin/python3

from alchem import app, db, ma

# class Result(Base):
class JobDescription(db.Model):
    __tablename__ = 'jobs'
    # update "trim_fields" according to fields length
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_url = db.Column(db.String(512), nullable=True)
    found_url = db.Column(db.String(512), nullable=True)
    job_title = db.Column(db.String(512), nullable=True)
    job_location = db.Column(db.String(512), default="", nullable=True)
    short_description = db.Column(db.String(512), default="", nullable=False)
    full_description = db.Column(db.String(10000), default="", nullable=False)
    tags_string = db.Column(db.String(512), default="", nullable=False)
    seen_time_epoch = db.Column(db.Integer, nullable=True)
    

