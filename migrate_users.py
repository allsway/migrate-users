#!/usr/bin/python
import sys
import csv
import requests
import json
import configparser
import xml.etree.ElementTree as ET

# Returns API key
def get_key():
    return config.get('Params', 'apikey')

# Returns the Alma API base URL
def get_base_url():
    return config.get('Params', 'baseurl')

# Returns user API url
def get_user_url(id):
    return get_base_url() + '/users?apikey=' + get_key()

# Reads in header row of file and maps header to indices
def read_header(header):
    indices = {}
    index = 0
    for h in header:
        indices[index] = h
        indices[h] = index
        index = index + 1
    return indices

# posts user record to Alma
def post_user(user,primary_id):
    url = get_user_url(primary_id)
    print(url)
    print (user)
    headers = {"Content-Type" : "application/json"}
    r = requests.post(url, data = user, headers = headers)
    print (r.content)

# Makes email JSON element
def make_email(val,email_type):
    email_dict = {}
    dict = {}
    dict['email_address'] = val
    dict['description'] = 'null'
    dict['preferred'] = 'true'
    dict['segment_type'] = 'External'
    dict['email_type'] = [{'value': email_type,'desc': email_type}]
    email_dict['email'] = [dict]
    return email_dict

# Maps record_type JSON
def make_record_type(val):
    dict = {}
    dict['value'] = val
    dict['desc'] = val.lower()
    return dict

def add_account_type(user_json):
    user_json['account_type'] = {"value":"EXTERNAL","desc":"External"}
    user_json['external_id'] = "SIS"
    return user_json

def make_user_group(val):
    dict = {}
    dict['value'] = val.lower()
    dict['desc'] = val
    return dict

# coverts user csv to use json format
def make_user_json(row,indices):
    user_json = {}
    for index in range(0,len(row)):
        field_name = indices[index]
        if field_name == 'primary_id':
            primary = row[index]
            user_json[field_name] = row[index]
        elif field_name == 'record_type':
            user_json[field_name] = make_record_type(row[index])
        elif field_name == 'email_address':
            email = make_email(row[index],row[indices['email_type']])
            user_json['contact_info'] = email
        elif field_name == 'user_group':
            user_json['user_group'] = make_user_group(row[index])
        elif field_name != 'email_type':
            print (field_name)
            user_json[field_name] = row[index]
    user_json = add_account_type(user_json)
    user_json = json.dumps(user_json)
    print(user_json)
    post_user(user_json,primary)

# Reads in user CSV file
def read_users(users):
    fields = {}
    f = open(users, 'rt')
    try:
        reader = csv.reader(f)
        header = next(reader)
        indices = read_header(header)
        for row in reader:
            make_user_json(row,indices)
    finally:
        f.close()

# Read config file
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Takes in csv export of Koha users
users = sys.argv[2]
read_users(users)
