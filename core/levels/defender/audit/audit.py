import random
import os
import json
import csv

from google.oauth2 import service_account
from core.framework import levels
from core.framework.cloudhelpers import deployments, iam, gcstorage, cloudfunctions

LEVEL_PATH = 'defender/compromised_key'

def create(second_deploy=True):
    print("Level initialization started for: " + LEVEL_PATH)
    nonce = str(random.randint(100000000000, 999999999999))

    user_db_name = f'userdata-db-{nonce}'

    register_func_template_args = {'db_name': user_db_name}
    register_func_url = cloudfunctions.upload_cloud_function(
            'core/levels/defender/resources/register_func',
            FUNCTION_LOCATION,
            template_args=register_func_template_args
            )

    config_template_args = {'nonce': nonce
                            'register_func_url': register_func_url
                            'root_password': 'Ax4**7^bBjwMz43*'}

    template_files = [
        'core/framework/templates/cloud_function.jinja',
        'core/framework/templates/iam_policy.jinja',
        'core/framework/templates/sql_db.jinja']
    
    if second_deploy:
        deployments.insert(LEVEL_PATH, template_files=template_files, config_template_args=config_template_args, second_deploy=True)
    else:
        deployments.insert(LEVEL_PATH, template_files=template_files,
                       config_template_args=config_template_args)
    try:
        print("Level setup started for: " + LEVEL_PATH)

        create_userdata_tables()
        user_keys = register_users()
        post_statuses()

        print(f'Level creation complete for: {LEVEL_PATH}')
        start_message = ('Helpful start message')

    except Exception as e: 
        exit()

def destroy():
    deployments.delete()

def create_userdata_tables():
    # Create the schema in the db for users and statuses

def register_users():
    # Load the synthetic user and developer information
    users = csv.DictReader(open('resources/users.csv', newline=''))
    devs = csv.DictReader(open('resources/devs.csv', newline=''))

    # Hit the db api to add users to the table and generate a bunch of account keys
    # might have to wait for the service accounts to register. Try every 60 seconds

def post_statuses():
    # Load statuses and post to db
