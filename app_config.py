#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
"""

import os

# This is just a readable name for the project.
PROJECT_NAME = 'Code Switch: Changing Races'

# This just changes the folder name that you're deploying to.
# E.g., apps.npr.org/<project_slug>/index.html
PROJECT_SLUG = 'codeswitch-changing-races'

# This is what we're calling your project on github.
# Don't change unless you change all your git stuff.
# Which is hard.
REPOSITORY_NAME = 'codeswitch-launch-essay'

PRODUCTION_S3_BUCKETS = ['apps.npr.org', 'apps2.npr.org']
STAGING_S3_BUCKETS = ['stage-apps.npr.org']

S3_BUCKETS = []


def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKETS
    global SERVERS
    global DEBUG

    if deployment_target == 'production':
        S3_BUCKETS = PRODUCTION_S3_BUCKETS
        DEBUG = False
    else:
        S3_BUCKETS = STAGING_S3_BUCKETS
        DEBUG = True

DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)
