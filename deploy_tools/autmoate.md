# Stuff to Automate

## Provision Server

1. Create user account; add to sudo group
1. Add SSH key to authorized key; disallow root login via SSH
1. `sudo apt update; sudo apt upgrade`
1. `sudo apt install nginx git python3.6 python3.6-venv`
1. Add nginx config
1. Add Systemd job for gunicorn

--------------------

## Deploy

1. Create directory in /home/$USER/sites/$DOMAIN
1. git pull source code
1. Start virtual environment
1. `pip install -r requirements.txt`
1. `python3.6 manage.py migrate`
1. `python3.6 manage.py collectstatic --noinput`
1. `sudo systemctl restart gunicorn...`
1. `Run FTs`
