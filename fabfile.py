# -*- coding: utf-8 -*-

import json
from os.path import relpath, dirname
from fabric.api import env, local
from fabric.colors import yellow

def itest():
    itest_build()
    itest_pull()
    itest_run()

def itest_run():
    from docker import Client
    docker = Client()

    try:
        docker.remove_container('dca', force=True)
    except:
        pass
    app = docker.create_container(image='dce_course_admin', name='dca')
    docker.start(app['Id'])

    try:
        docker.remove_container('canvas', force=True)
    except:
        pass
    canvas = docker.create_container(image='lbjay/canvas-docker', name='canvas')
    docker.start(canvas['Id'], links=[('dca','dca')])

def itest_build():
    from docker import Client
    docker = Client()
    build_path = relpath(dirname(env.real_fabfile))
    for line in docker.build(build_path, 'dce_course_admin', stream=True):
        print yellow(json.loads(line).get('stream'))

def itest_pull():
    from docker import Client
    docker = Client()
    for line in docker.pull('lbjay/canvas-docker', stream=True):
        print yellow(json.loads(line).get('status'))
