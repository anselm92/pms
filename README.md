# PMS - Printing Management System
The PMS is a web-based software which provides easy management of both 2d and 3d printing orders.

## Quickstart
1. Create virtual environment with Python 3.6 and don't forget to activate the environment.
2. Install requirements: `pip install -r requirements.txt`
3. Prepare settings
  * Copy `local_settings.py.sample` to `local_settings.py` (see `pms/settings/`) and set `FILES_ROOT`,
  create directory and set folder permissions
  * If you want to use LDAP authentication, uncomment the `import` statement within `local_settings.py`,
  copy `local_ldap_auth_settings.py.sample` to `local_ldap_auth_settings.py` (see `pms/settings/`), and
  adjust the LDAP settings accordingly.
4. Apply migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Install necessary software dependencies (for PDF previews)
  * ImageMagick: http://www.imagemagick.org/script/download.php (**Note**: Version must be **smaller** than 7.0.0!)
  * Ghostscript: https://www.ghostscript.com/download/gsdnld.html
  * Redis https://redis.io/download
7. Run redis and worker
  * $ redis-server
  * change into the project directory (eg. Repos/pms/pms) the one where managa.py is located
  * run worker $ celery -A pms.settings.celery worker -l info -c 3
8. Run server: `python3 manage.py runserver 8000`

## Development Notes
* Regenerate translation files: `django-admin makemessages -l de`
* Recompile translation files: `django-admin.py compilemessages`

## Deployment
Note this manual is for CentOS, please use appropriate commands for other operating systems
###### Software requirements:

    sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
    sudo yum install python36u
    sudo yum install python36u-pip
    sudo yum install python36u-devel
    sudo yum install gcc
    sudo yum install openldap-devel
    sudo yum install ghostscript
    sudo yum install ImageMagick ImageMagick-devel
    sudo yum install redis

###### Project setup

    pip3.6 install virtualenv
    cd /opt
    virtualenv -p python3.6 pmsenv
    cd pmsenv && source bin/activate
    git clone https://git.fs.tum.de/printing/pms.git

your folder structure should now look like this /opt/pmsenv/pms/pms/ (manage.py)

    cd /opt/pmsenv/pms
    pip3.6 install -r requirements.txt
    python manage.py migrate

###### Setup apache

    mkdir /var/log/pms
    chown apache:apache /var/log/pms/
    yum install httpd-devel
    pip3.6 install mod_wsgi
    mod_wsgi-express module-config
    
	# put the output of this command before your virtual host definition!
	# except WSGI Python home, this has to point to your virtualenv!!!
	# > LoadModule wsgi_module "/usr/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"

create a config file for django:



		LoadModule wsgi_module "/usr/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
		WSGIPythonHome "/opt/pmsenv/"

		<VirtualHost *:80>
			ServerName pms.bwk-technik.de
			ServerAlias pms.bwk-technik.de
			ServerAdmin admin@bwk-technik.de

			WSGIScriptAlias / /opt/pmsenv/pms/pms/pms/wsgi.py
			WSGIDaemonProcess pms python-home=/opt/pmsenv/
			WSGIProcessGroup pms
			WSGIApplicationGroup %{GLOBAL}

			<Directory /var/pms/static>
					Order allow,deny
					Allow from all
					Require all granted
			</Directory>

			<Directory /opt/pmsenv/pms/pms>
					Order allow,deny
					Allow from all
					Require all granted
			</Directory>


			<Directory /var/pms/orders>
					Require all granted
			</Directory>

			Alias /media /var/pms/orders
			Alias /static /var/pms/static

			ErrorLog /var/log/pms/http_error.log
	</VirtualHost>


Prepare variable folders for media
   

    mkdir /var/pms
    mkdir /var/pms/static
    mkdir /var/pms/orders

Change permissions on /var/pms ! So apache cann access it

    chown -R apache:apache /var/pms
    python manage.py collectstatic
    service httpd restart

Test your installation, by now everything except order preview generation and emails should work

###### Configure services

    systemctl enable redis
    systemctl start redis

    mkdir /var/run/celery
    chown apache:apache /var/run/celery
    nano /etc/systemd/system/celery.service
    
Your service file should look like this

	[Unit]
    Description=Celery Service
    After=network.target

    [Service]
    Type=forking
    User=apache
    Group=apache
    EnvironmentFile=-/etc/celery/celery.conf
    WorkingDirectory=/opt/pmsenv/pms/pms
    ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
      --pidfile=${CELERYD_PID_FILE}'
    ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    
    [Install]
    WantedBy=multi-user.target

Next create a config file for the service 
    
    mkdir /etc/celery
    nano /etc/celery/celery.conf
    
Put this into the configuration file (adapt if necessary)

    # Name of nodes to start
    # here we have a single node
    CELERYD_NODES="w1"
    # or we could have three nodes:
    #CELERYD_NODES="w1 w2 w3"
    
    # Absolute or relative path to the 'celery' command:
    CELERY_BIN="/opt/pmsenv/bin/celery"
    #CELERY_BIN="/virtualenvs/def/bin/celery"
    
    # App instance to use
    # comment out this line if you don't use an app
    CELERY_APP="pms.settings.celery"
    # or fully qualified:
    #CELERY_APP="proj.tasks:app"
    
    # How to call manage.py
    CELERYD_MULTI="multi"
    
    # Extra command-line arguments to the worker
    CELERYD_OPTS="--time-limit=300 --concurrency=2"
    
    # - %n will be replaced with the first part of the nodename.
    # - %I will be replaced with the current child process index
    #   and is important when using the prefork pool to avoid race conditions.
    CELERYD_PID_FILE="/var/run/celery/%n.pid"
    CELERYD_LOG_FILE="/var/log/pms/%n%I.log"
    CELERYD_LOG_LEVEL="INFO"



Next enable and start celery

    systemctl daemon-reload
    systemctl start celery
    systemctl status celery
    
    

##### Lastly configure clean_orders to run periodically
TBD
