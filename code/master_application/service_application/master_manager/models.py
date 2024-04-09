import uuid
from config import app_master_choices as gv
from django.db import models
from django.template.defaultfilters import slugify

class MasterDataRegistry(models.Model):
    code = models.CharField(max_length=32, unique=True, db_index=True)
    app_name = models.CharField(max_length=200, db_index=True)
    app_display_name = models.CharField(max_length=200, blank=True, null=True)
    model_name = models.CharField(max_length=200, db_index=True)
    model_display_name = models.CharField(max_length=200, blank=True, null=True)
    displayable_fields = models.TextField(blank=True, null=True)
    editable_include_fields = models.TextField(blank=True, null=True)
    editable_exclude_fields = models.TextField(blank=True, null=True)
    search_fields = models.TextField(blank=True, null=True)
    sort_by_fields = models.TextField(blank=True, null=True)
    is_mc_required = models.BooleanField(default=False) # memcache: load table data in dynamic gv
    is_ui_required = models.BooleanField(default=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        verbose_name = 'MasterDataRegistry'
        verbose_name_plural = 'MasterDataRegistry'
        db_table = 'ref_master_data_registry'

    def __str__(self):
        return self.model_name


class KVMaster(models.Model):
    key_category = models.CharField(max_length=200, db_index=True)
    key_code = models.CharField(max_length=20, unique=True, db_index=True)
    key_name = models.CharField(max_length=200, db_index=True)
    key_value = models.CharField(max_length=200)
    key_desc = models.CharField(max_length=200, blank=True, null=True)
    data_loaded_by = models.CharField(max_length=10, default='USER', choices=gv.DATA_LOADED_BY_CHOICES) # Data loaded by System or entered by User
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return self.key_code

    class Meta:
        db_table = 'ref_key_value_master'
        verbose_name = 'KVMaster'
        verbose_name_plural = 'KVMaster'


class Continent(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True,verbose_name='Continent Name')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='Created On')
    updated_on = models.DateTimeField(auto_now=True,verbose_name='Updated On')
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES,verbose_name='Datamode')

    class Meta:
        db_table = 'ref_continent'
        verbose_name = 'Continent'
        verbose_name_plural = 'Continents'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(unique=True, max_length=200)
    iso_4217_alpha = models.CharField(max_length=200)
    iso_4217_numeric = models.CharField(max_length=200)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    capital_city = models.CharField(max_length=200)
    telephone_calling_code = models.CharField(max_length=5)
    internet_domain_code = models.CharField(max_length=5)
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    code = models.CharField(max_length=32, unique=True, db_index=True)
    country = models.ForeignKey(Country, related_name='country',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_state'
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    state = models.ForeignKey(State, related_name='state',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, related_name='region_state', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_city'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class CityArea(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_cityarea'
        verbose_name = 'CityArea'
        verbose_name_plural = 'CityAreas'

    def __str__(self):
        return self.name


class Postalcode(models.Model):
    postalcode = models.CharField(unique=True, max_length=200)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    city_area = models.ForeignKey(CityArea,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'ref_postalcode'
        verbose_name = 'PostalCode'
        verbose_name_plural = 'PostalCodes'

    def __str__(self):
        return self.postalcode