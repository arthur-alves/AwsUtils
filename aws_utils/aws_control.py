# coding: utf-8
"""This module contains some examples using AwsUtils."""
import os
from datetime import datetime
from aws_utils import AwsUtils

# Get you AWS key and secret in your AWS console
AWS_KEY = os.environ.get("AWS_KEY")
AWS_SECRET = os.environ.get("AWS_SECRET")

# Ids dos workers
WORKERS_ID = ['x-xxxxxx', 'x-xxxxxx']


def control_workers(start_or_stop):
    u"""That script control work's lifetime.

    Args:
    - start_or_stop @string: must be 'start' ou 'stop'
    """
    aws = AwsUtils(AWS_KEY, AWS_SECRET)
    now = datetime.now()

    if start_or_stop == 'start':
        aws.start_service(WORKERS_ID)
        print "started at {}".format(str(now))

    elif start_or_stop == 'stop':
        aws.stop_service(WORKERS_ID)
        print "stopped at {}".format(str(now))


def get_ssh_conf():
    u"""Update ssh conf file with instance data in AWS.

    This is usefull if you turn off your machines and don't have a local
    network in AWS (Because you lose your IP). With this, you don't need to go
    in AWS console to see instance data, to update your conf file, if you use
    ssh of course.
    """
    aws = AwsUtils(AWS_KEY, AWS_SECRET)
    aws.generate_ssh_conf()
    return aws
