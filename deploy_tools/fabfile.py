import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/chammaaomar/coding-along-TDD.git"


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f-'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run('python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=yes')
    append('.env', f'SITENAME={env.host}')
    current_content = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_content:
        secret_key = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz', k=50))
        append('.env', f'DJANGO_SECRET_KEY={secret_key}')


def _update_static_files():
    run('./virtualenv/bin/python3.6 manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python3.6 manage.py migrate --noinput')
