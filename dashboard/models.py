from django.db import models


# Create your models here.
class snapShot(models.Model):
    state = models.CharField(max_length=100)
    state_ab = models.CharField(max_length=2)
    county = models.CharField(max_length=100)
    county_ab = models.CharField(max_length=2)
    fips = models.IntegerField(primary_key=True)
    county_name = models.CharField(max_length=100)
    year = models.IntegerField()
    tot_pop = models.IntegerField()
    med_hh_inc = models.IntegerField()
    estabs = models.IntegerField()
    emp = models.IntegerField()
    tot_hh_18 = models.IntegerField()
    tot_hh_no_int_18 = models.IntegerField()
    tot_hh_brdbnd_18 = models.IntegerField()
    unemployment_pct = models.FloatField()
    in_st_hq = models.IntegerField()
    branches = models.IntegerField()
    depsumbr = models.IntegerField()


class time_table(models.Model):
    state = models.CharField(max_length=100)
    state_ab = models.CharField(max_length=2)
    county = models.CharField(max_length=100)
    county_ab = models.CharField(max_length=3)
    fips = models.IntegerField()
    county_name = models.CharField(max_length=100)
    year = models.IntegerField()
    sm_ln_amt = models.IntegerField()
    med_ln_amt = models.IntegerField()
    lg_ln_amt = models.IntegerField()
    tot_pop = models.IntegerField()
    med_hh_inc = models.IntegerField()
    estabs = models.IntegerField()
    estabs_entry = models.IntegerField()
    estabs_exit = models.IntegerField()


class Meta:
    ordering = ('year',)


class neighbors(models.Model):
    countyname = models.CharField(max_length=100)
    fips = models.IntegerField()
    neighborname = models.CharField(max_length=100)
    fipsneighbors = models.IntegerField()


class geoJson(models.Model):
    type = models.CharField(max_length=7)
    properties = models.CharField(max_length=200)
    geometry = models.CharField(max_length=5000)
    fips = models.IntegerField(primary_key=True)
