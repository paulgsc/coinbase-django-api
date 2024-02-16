# -------------------------------------------------
REQUIREMENTS.TXT
autobahn==23.1.2 this is most recent version that railway supports must update to this
twisted-iocpsupport==1.0.3 don't push this, railway doesn't support for some reason.
evnetlet -> exclude this as well
 
10 16.51 ERROR: Could not find a version that satisfies the requirement numpy==1.25.2 (from versions: 1.3.0, 1.4.1, 1.5.0, 1.5.1, 1.6.0, 1.6.1, 1.6.2, 1.7.0, 1.7.1, 1.7.2, 1.8.0, 1.8.1, 1.8.2, 1.9.0, 1.9.1, 1.9.2, 1.9.3, 1.10.0.post2, 1.10.1, 1.10.2, 1.10.4, 1.11.0, 1.11.1, 1.11.2, 1.11.3, 1.12.0, 1.12.1, 1.13.0, 1.13.1, 1.13.3, 1.14.0, 1.14.1, 1.14.2, 1.14.3, 1.14.4, 1.14.5, 1.14.6, 1.15.0, 1.15.1, 1.15.2, 1.15.3, 1.15.4, 1.16.0, 1.16.1, 1.16.2, 1.16.3, 1.16.4, 1.16.5, 1.16.6, 1.17.0, 1.17.1, 1.17.2, 1.17.3, 1.17.4, 1.17.5, 1.18.0, 1.18.1, 1.18.2, 1.18.3, 1.18.4, 1.18.5, 1.19.0, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.19.5, 1.20.0, 1.20.1, 1.20.2, 1.20.3, 1.21.0, 1.21.1, 1.21.2, 1.21.3, 1.21.4, 1.21.5, 1.21.6, 1.22.0, 1.22.1, 1.22.2, 1.22.3, 1.22.4, 1.23.0rc1, 1.23.0rc2, 1.23.0rc3, 1.23.0, 1.23.1, 1.23.2, 1.23.3, 1.23.4, 1.23.5, 1.24.0rc1, 1.24.0rc2, 1.24.0, 1.24.1, 1.24.2, 1.24.3, 1.24.4)

10 16.51 ERROR: No matching distribution found for numpy==1.25.2
pandas==2.0.3 railway only support up to this.

################# RUN THE FOLLOWING ############################
pip freeze --exclude=eventlet twisted-iocpsupport > requirements.txt
echo "autobahn==23.1.2" >> requirements.txt


---------------- CELERY --------------------------------
looks like Windows OS is trash, it doesn't support fork() system leading to exceptions with celery billiard

########## HOTFIX ###############
os.environ['FORKED_BY_MULTIPROCESSING'] = '1' # either in celery.py or settings.py

########## DEV ENV WORKAROUND ################
pip install eventlet -> celery -A your_app_name worker --pool=eventlet
command: celery -A your_app_name worker -l info --autoscale 2,8 --pool=eventlet

COINBASE
########################################
EXAMPLE
How to set scopes and meta 
scope=wallet:user:read,wallet:user:email,wallet:accounts:read,wallet:transactions:read,wallet:transactions:send&meta[send_limit_amount]=1&meta[send_limit_currency]=USD&meta[send_limit_period]=day


REDIS
#############################################
start redis server disabling save
-------------> redis-server --save "" --appendonly no <----------------