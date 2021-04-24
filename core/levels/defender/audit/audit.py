import random
import os
import json
import csv
import sqlalchemy

from google.oauth2 import service_account
from core.framework import levels
from core.framework.cloudhelpers import (
    deployments,
    iam,
    gcstorage,
    cloudfunctions,
    db
)

LEVEL_PATH = 'defender/audit'
FUNCTION_LOCATION = 'us-central1'

def create(second_deploy=True):
    print("Level initialization started for: " + LEVEL_PATH)
    nonce = str(random.randint(100000000000, 999999999999))

    user_db_name = f'userdata-db-{nonce}'

    register_func_template_args = {'db_name': user_db_name}
    register_func_url = cloudfunctions.upload_cloud_function(
            'core/levels/defender/audit/resources/register_func',
            FUNCTION_LOCATION,
            template_args=register_func_template_args
            )

    config_template_args = {'nonce': nonce,
                            'register_url': register_func_url,
                            'root_password': 'psw'}

    template_files = [
        'core/framework/templates/cloud_function.jinja',
        'core/framework/templates/service_account.jinja',
        'core/framework/templates/iam_policy.jinja',
        'core/framework/templates/sql_db.jinja']

    if second_deploy:
        deployments.insert(
            LEVEL_PATH,
            template_files=template_files,
            config_template_args=config_template_args,
            second_deploy=True
        )
    else:
        deployments.insert(
            LEVEL_PATH,
            template_files=template_files,
            config_template_args=config_template_args
        )
    try:
        print("Level setup started for: " + LEVEL_PATH)

        create_tables(user_db_name)
        user_keys = register_users()
        post_statuses()

        print(f'Level creation complete for: {LEVEL_PATH}')
        start_message = ('Helpful start message')

    except Exception as e:
        exit()


def destroy():
    deployments.delete()

def register_users():
    # Load the synthetic user and developer information
    users = csv.DictReader(open('resources/users.csv', newline=''))
    devs = csv.DictReader(open('resources/devs.csv', newline=''))

    # Hit the db api to add users to the table and generate a bunch
    # of account keys might have to wait for the service accounts
    # to register. Try every 60 seconds


def post_statuses():
    # Load statuses and post to db
    statuses = csv.DictReader(open('resources/statuses.csv', newline=''))

#Table creation for  audit
def create_tables(user_db_name):
    db.connect(user_db_name)
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            """CREATE TABLE users (
                ID       INT PRIMARY KEY   NOT NULL,
                NAME     TEXT              NOT NULL,
                PHONE    TEXT              NOT NULL,
                ADDRESS  TEXT              NOT NULL
            );"""
        )