from django.db import models
from config import app_master_choices as gv
from config import settings
from django.utils.text import slugify
from service_application.account_manager.models import Account, AccountUser
from service_application.customer_manager.models import *
from phonenumber_field.modelfields import PhoneNumberField


class MasterPropertyType(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.name)

    def save(self, *args, **kwargs):
        super(MasterPropertyType, self).save(*args, **kwargs)
        if not self.code or self.code =="":
            self.code = "PROPERTY-TYPE-"+"-"+"%04d"%(self.id)
            super(MasterPropertyType, self).save()
            
    class Meta:
        db_table = 'master_property_type'


class MasterPropertyFeature(models.Model):
    code = models.CharField(max_length=64, null=True, blank=True)
    feature_name = models.CharField(max_length=255, null=True, blank=True)
    feature_description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.feature_name)

    def save(self, *args, **kwargs):
        super(MasterPropertyFeature, self).save(*args, **kwargs)
        if not self.code or self.code =="":
            self.code = "PROPERTY-MASTER-FEATURES-"+"-"+"%04d"%(self.id)
            super(MasterPropertyFeature, self).save()
            
    class Meta:
        db_table = 'master_property_feature'


class MasterPropertySpecification(models.Model):
    property_type = models.ForeignKey(MasterPropertyType, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, null=True, blank=True)
    specification_name = models.CharField(max_length=255, null=True, blank=True)
    specification_description = models.TextField(null=True, blank=True)
    specification_data_type = models.CharField(max_length=255, null=True, blank=True, choices=gv.DATA_TYPE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.specification_name)

    def save(self, *args, **kwargs):
        super(MasterPropertySpecification, self).save(*args, **kwargs)
        if not self.code or self.code =="":
            self.code = "PROPERTY-MASTER-SPECIFICATION-"+"-"+"%04d"%(self.id)
            super(MasterPropertySpecification, self).save()
            
    class Meta:
        db_table = 'master_property_specification'


class Property(models.Model):
    uid = models.CharField(max_length=64, null=True, blank=True, db_index=True, unique=True)
    slug = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    code = models.CharField(max_length=32, null=True, blank=True, db_index=True, unique=True)
    property_type = models.ForeignKey(MasterPropertyType, null=True, blank=True, on_delete=models.CASCADE)
    is_company_owned = models.BooleanField(default=False)
    owner = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    corporate_profile = models.ForeignKey(CorporateProfile, null=True, blank=True, on_delete=models.CASCADE)
    property_title = models.CharField(max_length=255, null=True, blank=True)
    property_description = models.TextField(null=True, blank=True)
    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    address_3 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    city_area = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=8, null=True, blank=True)
    preferred_location_tag = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    display_status = models.CharField(max_length=32, default='DRAFT', choices=gv.PROPERTY_STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.code)

    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)
        self.slug = slugify(self.property_title)
        self.uid = "PROPERTY-"+"%04d"%(self.id)
        super(Property, self).save()

    class Meta:
        db_table = 'property'


class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    feature = models.ForeignKey(MasterPropertyFeature, null=True, blank=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.property.code)


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.property.code)


class PropertyReview(models.Model):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.property.code)
    

class PropertySpecification(models.Model):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    specification = models.ForeignKey(MasterPropertySpecification, null=True, blank=True, on_delete=models.CASCADE)
    specification_value = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    datamode = models.CharField(max_length=1, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return "{0}".format(self.property.code)
