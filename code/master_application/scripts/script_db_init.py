import os
import traceback
import MySQLdb
import sys
import glob
import traceback
from config import settings
from config import application_logger, app_master_choices
from django.core.management import call_command

from scripts import script_create_superuser

logger = application_logger.createLogger("app_scripts")
dbengine = settings.DATABASES['default']['ENGINE']
dbname   = settings.DATABASES['default']['NAME']
dbhost   = settings.DATABASES['default']['HOST']
dbuser   = settings.DATABASES['default']['USER']
dbpass   = settings.DATABASES['default']['PASSWORD']

@application_logger.functionlogs(log="app_scripts")
def createDatabase():
    result=False
    try:
        db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass)
        logger.debug("creating database...{0}".format(dbname))
        cursor = db.cursor()
        createsql = "create SCHEMA %s CHARACTER SET utf16 COLLATE utf16_general_ci"% (dbname)
        cursor.execute(createsql)
        cursor.close()
        db.close()
        logger.debug("created database...{0}".format(dbname))
        result=True
    except Exception as error:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno, error))
        print('Error at %s:%s' %(exc_traceback.tb_lineno, error))
        raise error
    return result


@application_logger.functionlogs(log="app_scripts")
def dropDatabase():
    result=False
    try:
        db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass)
        cursor = db.cursor()
        dropsql = 'drop SCHEMA %s' % (dbname)
        logger.debug(dropsql)
        logger.debug("droping database...{0}".format(dbname))
        try:
            cursor.execute(dropsql)
            logger.debug("dropped database...{0}".format(dbname))
        except:
            logger.debug("database doesn't exist...{0}".format(dbname))
            logger.error(traceback.format_exc())
        cursor.close()
        db.close()
        
        result=True
    except Exception as error:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno, error))
        print('Error at %s:%s' %(exc_traceback.tb_lineno, error))
        raise error
    return result


@application_logger.functionlogs(log="app_scripts")
def run_migrations():
    result = False
    try:
        app_list = [ app for app in settings.INSTALLED_APPS ]
        for apps in app_list:
            apps = apps.replace(".","/")
            migration_path = os.path.join(settings.BASE_DIR, '%s/migrations'%(apps))
            for file in glob.glob(migration_path+"/0*.py"):
                os.remove(file)
        all_app_list = [ app for app in settings.INSTALLED_APPS ]
        for apps in all_app_list:
            if apps.startswith("apps"):
                apps = apps.rsplit(".",1)
                try:
                    call_command('makemigrations','--pythonpath', apps[0].replace(".","/"),apps[1], interactive=False)
                except Exception as error:
                    logger.error(traceback.format_exc())
                    raise error
        result = True
    except Exception as error:
        logger.error(traceback.format_exc())
        raise error
    call_command('makemigrations', interactive=False)
    call_command('migrate', interactive=False)
    return result


@application_logger.functionlogs(log="app_scripts")
def run():
    logger.info("Starting ...")
    dropDatabase()
    createDatabase()
    run_migrations()
    script_create_superuser.create_superuser()
    logger.info("End !!!")