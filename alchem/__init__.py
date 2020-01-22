#!/usr/bin/python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
import os

'''
setup on local env:
export AUTH__AUTH0_DOMAIN=dev-l6hghqp3.auth0.com
export AUTH__API_AUDIENCE=https://dev-l6hghqp3.auth0.com/api/v2/
export AUTH__RS256=RS256
export AUTH__CLIENT_SECRET=<ENTER SECRET HERE>

OR on Heroku environment:
heroku config:set AUTH__AUTH0_DOMAIN=dev-l6hghqp3.auth0.com
heroku config:set AUTH__API_AUDIENCE=https://dev-l6hghqp3.auth0.com/api/v2/
heroku config:set AUTH__RS256=RS256
heroku config:set AUTH__CLIENT_SECRET=<ENTER SECRET HERE>
'''

AUTH0_DOMAIN = os.environ.get('AUTH__AUTH0_DOMAIN')
API_AUDIENCE = os.environ.get('AUTH__API_AUDIENCE')
ALGORITHMS = os.environ.get('AUTH__RS256')
CLIENT_SECRET = os.environ.get('AUTH__CLIENT_SECRET')

app = None
db = SQLAlchemy(app)
ma = Marshmallow(app)
# api = Api(app)
api = None

