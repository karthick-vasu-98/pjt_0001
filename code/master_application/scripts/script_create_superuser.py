import os
import datetime
import traceback
import sys
import shutil
import json
import glob
import ast
import traceback
from config import settings
from config import application_logger, app_master_choices
from django.core.management import call_command
from django.contrib.auth.admin import User,Group
from service_application.account_manager.models import *

logger = application_logger.createLogger("app_scripts")

dbengine = settings.DATABASES['default']['ENGINE']
dbname   = settings.DATABASES['default']['NAME']
dbhost   = settings.DATABASES['default']['HOST']
dbuser   = settings.DATABASES['default']['USER']
dbpass   = settings.DATABASES['default']['PASSWORD']

@application_logger.functionlogs(log="app_scripts")
def _create_user_kyc_profile(user):
    result = False
    user_kyc_profile = None
    try:
        user_kyc_profile = UserKYCProfile()
        user_kyc_profile.user = user
        user_kyc_profile.first_name = app_master_choices.SUPER_USER_FIRSTNAME
        user_kyc_profile.last_name = app_master_choices.SUPER_USER_LASTNAME
        user_kyc_profile.created_by = user
        user_kyc_profile.updated_by = user
        user_kyc_profile.save()
        result = True
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno,e))
    return user_kyc_profile


@application_logger.functionlogs(log="app_scripts")
def _create_account(user):
    result = False
    account = None
    try:
        account_type, result = AccountType.objects.get_or_create(code="PRO")
        
        account = Account()
        account.account_type = account_type
        account.name = str(account_type.name) + " Account"
        account.created_by = user
        account.updated_by = user
        account.save()

        #create AccountGroup + Group from DefaultAccountGroup
        default_account_group = DefaultAccountGroup.objects.filter(account_type=account_type)
        for default_group in default_account_group:
            group_name = account.account_type.name + "-" + account.uid + "-" + default_group.group_name
            account_group = AccountGroup()
            account_group.account = account                  
            account_group.group_name = group_name
            account_group.created_by = user
            account_group.updated_by = user
            account_group.save()
            group = Group()
            group.name = group_name
            group.save()
            if default_group.is_default:
                group.user_set.add(user)
            
        #create AccountSettings from DefaultAccountSettings
        default_account_settings = DefaultAccountSettings.objects.filter(account_type=account_type)
        for default_settings in default_account_settings:
            account_setting = AccountSettings()
            account_setting.account = account                  
            account_setting.name = default_settings.name
            account_setting.code = default_settings.code
            account_setting.key = default_settings.key
            account_setting.lov = default_settings.lov
            account_setting.selected_value = default_settings.default_value
            account_setting.created_by = user
            account_setting.updated_by = user
            account_setting.save()
            
        result = True
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno,e))
    return account


@application_logger.functionlogs(log="app_scripts")
def _create_account_user(account, user):
    result = False
    account_user = None
    try:
        if not AccountUser.objects.filter(account=account,user=user,datamode='ACTIVE').exists():
            account_user = AccountUser()
            account_user.account = account
            account_user.user = user
            account_user.is_default_account = True
            account_user.is_current_account = True
            account_user.is_first_time_login = True
            account_user.created_by = user
            account_user.updated_by = user
            account_user.save()
            
            account_settings = AccountSettings.objects.filter(account=account,datamode='ACTIVE')
            for account_setting in account_settings:
                if not AccountUserSettings.objects.filter(au_id=account_user,key=account_setting.key,datamode='ACTIVE').exists():
                    account_user_settings = AccountUserSettings()
                    account_user_settings.au_id = account_user                  
                    account_user_settings.name = account_setting.name
                    account_user_settings.code = account_setting.code
                    account_user_settings.key = account_setting.key
                    account_user_settings.selected_value = account_setting.default_value
                    account_user_settings.created_by = user
                    account_user_settings.updated_by = user
                    account_user_settings.save()

        result = True
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' %(exc_traceback.tb_lineno,e))
    return account_user


@application_logger.functionlogs(log="app_scripts")
def create_superuser():
    superuser = User()
    superuser.is_active = app_master_choices.SUPER_USER_ACTIVE
    superuser.is_superuser = app_master_choices.SUPER_USER_IS_SUPERUSER
    superuser.is_staff = app_master_choices.SUPER_USER_IS_STAFF
    superuser.username = app_master_choices.SUPER_USER_NAME
    superuser.email = app_master_choices.SUPER_USER_EMAIL
    superuser.set_password(app_master_choices.SUPER_USER_PASSWORD)
    superuser.first_name = app_master_choices.SUPER_USER_FIRSTNAME
    superuser.last_name = app_master_choices.SUPER_USER_LASTNAME
    superuser.save()
    _create_user_kyc_profile(superuser)
    account = _create_account(superuser)
    _create_account_user(account,superuser)

@application_logger.functionlogs(log="app_scripts")
def run():
    logger.info("Starting ...")
    create_superuser()
    logger.info("End !!!")