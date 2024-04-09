from django.db import models
from config import app_master_choices as gv
from config import settings
from django.utils.text import slugify
from service_application.account_manager.models import Account, AccountUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomerType(models.Model):
    code = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)


class Customer(models.Model):
    uid = models.CharField(max_length=64)
    customer_type = models.ForeignKey(CustomerType, null=True, blank=True, on_delete=models.CASCADE)
    account_user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    language_1 = models.CharField(max_length=255, null=True, blank=True, choices=settings.LANGUAGES)
    language_2 = models.CharField(max_length=255, null=True, blank=True, choices=settings.LANGUAGES)
    mobile_app_usage = models.BooleanField(default=False)
    source = models.CharField(max_length=255, null=True, blank=True)
    sub_source = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        if not self.uid or self.uid =="":
            self.uid = "CUST"+"-"+"%04d"%(self.id)
            super(Customer, self).save()
            
    class Meta:
        db_table = 'individual_customer'


class CompanyType(models.Model):
    code = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)


class CorporateProfile(models.Model):
    uid = models.CharField(max_length=64)
    company_type = models.ForeignKey(CompanyType, null=True, blank=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_mobile_nummber = PhoneNumberField(null=True, blank=True)
    company_email_address = models.EmailField(null=True, blank=True)
    company_website = models.CharField(max_length=255, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    company_gst_number = models.CharField(max_length=64, null=True, blank=True)
    company_pan_number = models.CharField(max_length=64, null=True, blank=True)
    cin_number = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    company_country = models.CharField(max_length=255, null=True, blank=True)
    company_state = models.CharField(max_length=255, null=True, blank=True)
    company_city = models.CharField(max_length=255, null=True, blank=True)
    company_city_area = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=8, null=True, blank=True)
    preferred_location_tag = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    poc_name = models.CharField(max_length=255, null=True, blank=True)
    poc_type = models.CharField(max_length=255, null=True, blank=True, default="PRIMARY", choices=gv.ACCOUNT_CONTACT_LEVEL_CHOICES)
    poc_phone = PhoneNumberField(null=True, blank=True)
    poc_email = models.EmailField(null=True, blank=True)
    alt_phone_number1 = PhoneNumberField(null=True, blank=True)
    alt_phone_number2 = PhoneNumberField(null=True, blank=True)
    display_status = models.CharField(max_length=32, default='DRAFT', choices=gv.COMPANY_STATUS)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.company_name)


class CompanyMasterStaffDesignation(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    code = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)


class CompanyStaff(models.Model):
    uid = models.CharField(max_length=20, db_index=True)
    salutation = models.CharField(max_length=8, choices=gv.SALUTATION_TYPE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    employee_id = models.CharField(verbose_name="Employee ID",max_length=64, db_index=True)
    designation = models.ForeignKey(CompanyMasterStaffDesignation, verbose_name="DESIGNATION", on_delete=models.CASCADE)
    dob = models.DateField(verbose_name="DOB", null=True, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=8, null=True, blank=True, choices=gv.GENDER)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    pan_card = models.CharField(verbose_name="PAN CARD", max_length=16, null=True, blank=True)
    ric_number = models.CharField(verbose_name="NRIC NUMBER",max_length=64, null=True, blank=True)
    adhaar_number = models.CharField(verbose_name="AADHAR NUMBER",max_length=16, null=True, blank=True)
    staff_photo = models.ImageField(verbose_name="Staff Photo", upload_to=gv.IMAGE_REPO_FOLDER, null=True, blank=True)
    email = models.EmailField()
    mobile_number = PhoneNumberField()
    alternate_mobile_number = PhoneNumberField(null=True, blank=True)
    personal_address = models.TextField(null=True, blank=True)
    staff_kyc_photo = models.ImageField(verbose_name="Staff KYC Photo", upload_to=gv.IMAGE_REPO_FOLDER, null=True, blank=True)
    staff_kyc_driving_licence = models.ImageField(verbose_name="Staff KYC Driving Licence", upload_to=gv.IMAGE_REPO_FOLDER, null=True, blank=True)
    staff_kyc_aadhar_file = models.ImageField(verbose_name="Staff KYC Aadhar File", upload_to=gv.IMAGE_REPO_FOLDER, null=True, blank=True)
    staff_kyc_signature = models.ImageField(verbose_name="Staff KYC Signature", upload_to=gv.IMAGE_REPO_FOLDER, null=True, blank=True)
    language_preference = models.JSONField(null=True, blank=True)
    company = models.ForeignKey(CorporateProfile, on_delete=models.CASCADE)
    account_user = models.ForeignKey(AccountUser, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.first_name)

    def save(self, *args, **kwargs):
        super(CompanyStaff, self).save(*args, **kwargs)
        if not(self.uid):
            self.uid = "HZST-%04d"%(self.id)
            super(CompanyStaff, self).save()

    class Meta:
        db_table = 'company_staff'


class CompanyReview(models.Model):
    company = models.ForeignKey(CorporateProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.company.company_name)


class CompanyMasterService(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)
    
    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        db_table = 'company_master_service'


class CompanyMasterFeature(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)
    
    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        db_table = 'company_master_feature'


class CompanyService(models.Model):
    service = models.ForeignKey(CompanyMasterService, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(CorporateProfile, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.company.company_name)

    class Meta:
        db_table = 'company_service'


class CompanyFeature(models.Model):
    feature = models.ForeignKey(CompanyMasterFeature, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(CorporateProfile, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.company.company_name)

    class Meta:
        db_table = 'company_feature'


class ComapnyPOC(models.Model):
    company = models.ForeignKey(CorporateProfile, null=True, blank=True, on_delete=models.CASCADE)
    poc_name = models.CharField(max_length=255, null=True, blank=True)
    poc_mobile_number = PhoneNumberField(null=True, blank=True)
    poc_email = models.EmailField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0} - {1}".format(self.company.company_name, self.poc_name)

    class Meta:
        db_table = 'company_poc'