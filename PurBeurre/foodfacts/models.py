""" This is an auto-generated Django model module.
 I used the command
 'python manage.py inspectdb > models.py'  in PowerShell
 PLEASE NOTE THAT THE MODEL IS NOT UTF-8 ENCODED.
 SO WHEN YOU'LL TRY TO START DJANGO
 YOU WILL GET THIS ERROR :
 "source code string cannot contain null bytes"
 THIS IS HOW YOU WILL AVOID HEADACHES:
 YOU MUST ENCODE THE FILE in UTF-8.
 THEN SAVE IT.
 THEN 'PYTHON MANAGE.PY RUNSERVER' WILL WORK.
 I USED NOTEPAD++ TO ENCODE THIS FILE USING UTF-8.
 You'll have to do the following manually to clean this up:
   * Rearrange models' order
   * Make sure each model has one field
        with primary_key=True
   * Make sure each ForeignKey and OneToOneField has
    `on_delete` set to the desired behavior
   * Remove `managed = False` lines if you wish
    to allow Django to create, modify, and delete the table data
Feel free to rename the models,
but don't rename db_table values or field names. """
import os
from django.db import models

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class Categories(models.Model):
    """ORM attributes and functions of Category"""
    idcategories = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "categories"


class Favorites(models.Model):
    """ORM attributes and functions of Favorites"""
    favoriteid = models.AutoField(primary_key=True)
    productid = models.IntegerField(null=False)
    name = models.CharField(max_length=255, null=False)
    nutrigrade = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    replacedid = models.IntegerField(null=False)
    userid = models.CharField(max_length=255, null=False)
    front_img = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "favorites"


class Products(models.Model):
    """ORM attributes and functions of Products"""
    idproduct = models.AutoField(primary_key=True, null=False)
    productname = models.CharField(max_length=500, null=False)
    stores = models.CharField(max_length=500, null=False)
    brands = models.CharField(max_length=500)
    nutrigrade = models.CharField(max_length=500, null=False)
    category = models.CharField(max_length=500, null=False)
    quantity = models.CharField(max_length=500, null=False)
    fat_100g = models.FloatField(null=False)
    sugars_100g = models.FloatField(null=False)
    saturated_fat_100g = models.FloatField(null=False)
    energy_kcal_100g = models.FloatField(null=False)
    nutrition_Score_100g = models.IntegerField(null=False)
    fiber_100g = models.FloatField(null=False)
    salt_100g = models.FloatField(null=False)
    proteins_100g = models.FloatField(null=False)
    carbs_100g = models.FloatField(null=False)
    sodium_100g = models.FloatField(null=False)
    front_img = models.CharField(max_length=500, null=False)
    nutrition_img = models.CharField(max_length=500, null=False)
    ingredients_img = models.CharField(max_length=500, null=False)
    url = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.productname

    class Meta:
        managed = True
        db_table = "products"
