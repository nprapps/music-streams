#!/usr/bin/env python

from glob import glob
import os

from fabric.api import *

import app_config

"""
Base configuration
"""
env.deployed_name = app_config.PROJECT_SLUG
env.repo_name = app_config.REPOSITORY_NAME

env.deploy_to_servers = False
env.install_crontab = False
env.deploy_web_services = False

env.repo_url = 'git@github.com:nprapps/%(repo_name)s.git' % env
env.alt_repo_url = None  # 'git@bitbucket.org:nprapps/%(repo_name)s.git' % env
env.user = 'ubuntu'
env.python = 'python2.7'
env.path = '/home/%(user)s/apps/%(deployed_name)s' % env
env.repo_path = '%(path)s/repository' % env
env.virtualenv_path = '%(path)s/virtualenv' % env
env.forward_agent = True

SERVICES = [
    ('nginx', '/etc/nginx/sites-available/'),
    ('uwsgi', '/etc/init/')
]


def production():
    env.settings = 'production'
    env.s3_buckets = app_config.PRODUCTION_S3_BUCKETS


def staging():
    env.settings = 'staging'
    env.s3_buckets = app_config.STAGING_S3_BUCKETS


def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'


def master():
    """
    Work on development branch.
    """
    env.branch = 'master'


def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name


def _deploy_to_s3():
    """
    Deploy the gzipped stuff to S3.
    """
    s3cmd = 's3cmd -P --add-header=Cache-Control:max-age=5 --guess-mime-type --recursive --exclude-from gzip_types.txt sync gzip/ %s'
    s3cmd_gzip = 's3cmd -P --add-header=Cache-Control:max-age=5 --add-header=Content-encoding:gzip --guess-mime-type --recursive --exclude "*" --include-from gzip_types.txt sync gzip/ %s'

    for bucket in env.s3_buckets:
        env.s3_bucket = bucket
        local(s3cmd % ('s3://%(s3_bucket)s/%(deployed_name)s/' % env))
        local(s3cmd_gzip % ('s3://%(s3_bucket)s/%(deployed_name)s/' % env))


def _gzip_www():
    """
    Gzips everything in www and puts it all in gzip
    """
    local('python gzip_www.py')
    local('rm -rf gzip/live-data')


def deploy(remote='origin'):
    """
    Deploy the latest app to S3 and, if configured, to our servers.
    """
    require('settings', provided_by=[production, staging])

    if (env.settings == 'production' and env.branch != 'stable'):
        _confirm("You are trying to deploy the '%(branch)s' branch to production.\nYou should really only deploy a stable branch.\nDo you know what you're doing?" % env)

    _gzip_www()
    _deploy_to_s3()

    if env.get('deploy_to_servers', False):
        checkout_latest(remote)

        if env.get('install_crontab', False):
            install_crontab()


def _confirm(message):
    answer = prompt(message, default="Not at all")

    if answer.lower() not in ('y', 'yes', 'buzz off', 'screw you'):
        exit()


def shiva_the_destroyer():
    """
    Deletes the app from s3
    """
    require('settings', provided_by=[production, staging])

    _confirm("You are about to destroy everything deployed to %(settings)s for this project.\nDo you know what you're doing?" % env)

    with settings(warn_only=True):
        s3cmd = 's3cmd del --recursive %s'

        for bucket in env.s3_buckets:
            env.s3_bucket = bucket
            local(s3cmd % ('s3://%(s3_bucket)s/%(deployed_name)s' % env))


def super_merge():
    """
    Merge master branch into all init- branches.
    """
    _confirm("You are about to merge 'master' into all 'init-' branches.\nDo you know what you're doing?")

    local('git fetch')
    local('git checkout master')

    for branch in ['table', 'map', 'chat']:
        local('git checkout init-%s' % branch)
        local('git merge origin/init-%s --no-edit' % branch)
        local('git merge master --no-edit')

    local('git checkout master')

    local('git push --all')
