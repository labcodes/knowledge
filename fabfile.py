from fabric.api import runs_once, lcd, run, env, cd, local
from decouple import config
import os


PYTHON_PATH = '/home/labcodes/.virtualenvs/knowledge/bin/python'

env.hosts = ['labcodes.com.br']
env.user = 'labcodes'


def deploy():
    with cd('/home/labcodes/webapps/knowledge'):
        git_path = os.getcwd()

        update_repo_from_master()
        migrate_applications()
        collect_static_files()
        restart_nginx()
        restart_supervisor()
        register_deployment(git_path)


def update_repo_from_master():
    run('git pull origin master')


def migrate_applications():
    run(f'{PYTHON_PATH} manage.py migrate')


def collect_static_files():
    run(f'{PYTHON_PATH} manage.py collectstatic --no-input')


def restart_nginx():
    run('sudo service nginx restart')


def restart_supervisor():
    run('sudo supervisorctl restart knowledge')


@runs_once
def register_deployment(git_path):
    with(lcd(git_path)):
        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        organization_id = config('ORGANIZATION_ID', cast=str)
        app_id = config('APP_ID', cast=str)
        secret_token = config('SECRET_OPBEAT_TOKEN', cast=str)
        local('curl https://intake.opbeat.com/api/v1/organizations/{}/apps/{}/releases/'
              ' -H "Authorization: Bearer {}"'
              ' -d rev={}'
              ' -d branch={}'
              ' -d status=completed'.format(organization_id, app_id, secret_token, revision, branch))
