import uuid
import random
from config import app_master_choices as gv
from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField


class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    code = models.CharField(max_length=6, unique=True, db_index=True)
    is_default = models.BooleanField(default=False)
    is_registration_allowed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ref_account_type'
        verbose_name = 'AccountType'
        verbose_name_plural = 'AccountTypes'


class DefaultAccountGroup(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return self.account_type.name + '-' + self.group_name

    class Meta:
        db_table = 'ref_account_default_group'
        verbose_name = 'DefaultAccountGroup'
        verbose_name_plural = 'DefaultAccountGroups'


class Account(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    uid = models.CharField(max_length=20, unique=True,editable=False, db_index=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.name, self.uid)

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)
        if self.uid == "":
            self.uid  = "%s%09d" % (gv.ACCOUNT_UID_PREFIX,int(self.id))
        super(Account, self).save()


class DefaultAccountSettings(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    code = models.CharField(max_length=6, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=50)
    lov = models.JSONField()
    default_value = models.CharField(max_length=50)
    mode = models.CharField(max_length=10, default='SYS', choices=gv.DATA_LOADED_BY_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ref_account_default_settings'
        verbose_name = 'DefaultAccountSettings'
        verbose_name_plural = 'DefaultAccountSettings'


class AccountGroup(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}/{1}".format(self.account.name,self.group_name)

    class Meta:
        unique_together = ('account', 'group_name')
        db_table = 'acct_group_account'
        verbose_name = 'AccountGroup'
        verbose_name_plural = 'AccountGroups'


class AccountUser(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    uid = models.CharField(max_length=20, unique=True, editable=False, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default_account = models.BooleanField(default=True)
    is_current_account = models.BooleanField(default=True)
    last_active_on = models.DateTimeField(blank=True, null=True)
    user_status = models.CharField(max_length=20, default='A', choices=gv.ACCOUNT_USER_STATUS_CHOICES)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.user.first_name, self.uid)

    def save(self):
        super(AccountUser, self).save()
        if self.uid == "":
            self.uid  = "%s%08d" % (gv.ACCOUNT_USER_UID_PREFIX,int(self.id))
            super(AccountUser, self).save()

    class Meta:
        db_table = 'acct_user_account'
        verbose_name = 'AccountUser'
        verbose_name_plural = 'AccountUsers'


class AccountUserActivities(models.Model):
    au_id = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=50) #choicefield/choices to be decided later
    device_ipaddress = models.CharField(max_length=50)
    device_type = models.CharField(max_length=10, default='PC', choices=gv.DEVICE_TYPE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1})".format(self.au_id.user.first_name, self.activity_name)


    class Meta:
        db_table = 'acct_user_activities'
        verbose_name = 'AccountUserActivities'
        verbose_name_plural = 'AccountUserActivities'


def get_referral_code():
    ref_code = ''
    try:
        ref_code = random.randint(10000,99999)
        if UserKYCProfile.objects.filter(referral_code=ref_code,datamode='A').exists():
            get_referral_code()
    except Exception as e:
        print("err",e)
    return ref_code


class UserKYCProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='User Avatar', upload_to=gv.IMAGE_REPO_FOLDER, blank=True, null=True)
    interest_tags = models.TextField(blank=True,null=True)
    cover_photo = models.ImageField(verbose_name="Cover Photo", upload_to=gv.IMAGE_REPO_FOLDER, blank=True, null=True)
    nick_name = models.CharField(max_length=100,blank=True,null=True)
    first_name = models.CharField(max_length=150,blank=True,null=True)
    last_name = models.CharField(max_length=150,blank=True,null=True)
    phone_number = PhoneNumberField()
    email_verified = models.BooleanField(default=False)
    email_verify_code = models.CharField(max_length=200,blank=True,null=True)
    email_verified_date = models.DateTimeField(blank=True,null=True)
    email_verify_otp = models.CharField(max_length=10,blank=True,null=True)
    phone_number_verified = models.BooleanField(default=False)
    phone_number_verify_code = models.CharField(max_length=200,blank=True,null=True)
    phone_number_verified_date = models.DateTimeField(blank=True,null=True)
    phone_number_verify_otp = models.CharField(max_length=10,blank=True,null=True)
    alternate_phone_number = models.CharField(max_length=15,blank=True,null=True)
    alternate_email = models.EmailField(blank=True,null=True)
    referral_code = models.CharField(max_length=10,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name = "%(class)s_createdby", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name = "%(class)s_updatedby", on_delete=models.CASCADE)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.user.username)

    class Meta:
        db_table = 'acct_user_kyc_profile'
    
    def save(self, *args, **kwargs):
        super(UserKYCProfile, self).save(*args, **kwargs)
        if not self.referral_code:
            self.referral_code = get_referral_code() 
        super(UserKYCProfile, self).save()


class UserRegisteredDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100)
    device_browser = models.CharField(max_length=100,blank=True)
    device_os = models.CharField(max_length=100,blank=True)
    device_type = models.CharField(max_length=100,blank=True)
    device_city = models.CharField(max_length=100,blank=True)
    device_region = models.CharField(max_length=100,blank=True)
    device_country = models.CharField(max_length=100,blank=True)
    device_ip = models.CharField(max_length=100,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.user.username)

    class Meta:
        db_table = 'user_registered_device'


class MasterPermission(models.Model):
    app_name = models.CharField(max_length=100)
    permission_name = models.CharField(max_length=255)
    permission_desc = models.TextField()
    permission_code = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.permission_name)

    class Meta:
        db_table = 'master_permission'


class AccountSettings(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    description = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=50)
    lov = models.JSONField(blank=True,null=True)
    default_value = models.CharField(max_length=50)
    selected_value = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1}:{2})".format(self.account.name, self.key,self.selected_value)


    class Meta:
        db_table = 'acct_settings'
        verbose_name = 'AccountSettings'
        verbose_name_plural = 'AccountSettings'


class AccountUserSettings(models.Model):
    au_id = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    description = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=50)
    lov = models.JSONField(blank=True,null=True)
    default_value = models.CharField(max_length=50)
    selected_value = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}({1}:{2})".format(self.au_id.user.first_name, self.key,self.selected_value)


    class Meta:
        db_table = 'acct_user_settings'
        verbose_name = 'AccountUserSettings'
        verbose_name_plural = 'AccountUserSettings'