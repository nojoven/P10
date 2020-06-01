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

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class Categories(models.Model):
    """ORM attributes and functions of Category"""
    idcategories = models.AutoField(
        db_column="idCategories", primary_key=True
    )  # Field name made lowercase.
    name = models.CharField(
        db_column="Name", max_length=255
    )  # Field name made lowercase.

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = "categories"


class Favorites(models.Model):
    """ORM attributes and functions of Favorites"""
    favoriteid = models.AutoField(
        db_column="FavoriteID", primary_key=True
    )  # Field name made lowercase.
    productid = models.IntegerField(db_column="ProductID")
    # Field name made lowercase.
    name = models.CharField(
        db_column="Name", max_length=255
    )  # Field name made lowercase.
    nutrigrade = models.CharField(
        db_column="Nutrigrade", max_length=255
    )  # Field name made lowercase.
    stores = models.CharField(
        db_column="Stores", max_length=255
    )  # Field name made lowercase.
    brands = models.CharField(
        db_column="Brands", max_length=255
    )  # Field name made lowercase.
    category = models.CharField(
        db_column="Category", max_length=255
    )  # Field name made lowercase.
    quantity = models.CharField(
        db_column="Quantity", max_length=255
    )  # Field name made lowercase.
    replacedid = models.IntegerField(
        db_column="ReplacedID"
    )  # Field name made lowercase.
    replacedarticle = models.CharField(
        db_column="ReplacedArticle", max_length=255
    )  # Field name made lowercase.
    replacednutrigrade = models.CharField(
        db_column="ReplacedNutrigrade", max_length=255
    )  # Field name made lowercase.
    userid = models.CharField(
        db_column="UserID", max_length=255
    )  # Field name made lowercase.
    front_img = models.CharField(
        db_column="Front_img", max_length=500, default=""
    )  # Field name made lowercase.

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = "favorites"


class Products(models.Model):
    """ORM attributes and functions of Products"""
    idproduct = models.AutoField(
        db_column="idProduct", primary_key=True
    )  # Field name made lowercase.
    productname = models.CharField(
        db_column="ProductName", max_length=500
    )  # Field name made lowercase.
    stores = models.CharField(
        db_column="Stores", max_length=500
    )  # Field name made lowercase.
    brands = models.CharField(
        db_column="Brands", max_length=500
    )  # Field name made lowercase.
    nutrigrade = models.CharField(
        db_column="Nutrigrade", max_length=500
    )  # Field name made lowercase.
    category = models.CharField(
        db_column="Category", max_length=500
    )  # Field name made lowercase.
    quantity = models.CharField(
        db_column="Quantity", max_length=500
    )  # Field name made lowercase.
    fat_100g = models.FloatField(db_column="Fat_100g")
    # Field name made lowercase.
    sugars_100g = models.FloatField(
        db_column="Sugars_100g"
    )  # Field name made lowercase.
    saturated_fat_100g = models.FloatField(
        db_column="Saturated_Fat_100g"
    )  # Field name made lowercase.
    energy_kcal_100g = models.FloatField(
        db_column="Energy_Kcal_100g"
    )  # Field name made lowercase.
    nutrition_Score_100g = models.IntegerField(
        db_column="Nutrition_Score_100g"
    )  # Field name lowercase
    fiber_100g = models.FloatField(db_column="Fiber_100g")
    # Field name made lowercase.
    salt_100g = models.FloatField(db_column="Salt_100",)
    # Field name made lowercase.
    proteins_100g = models.FloatField(
        db_column="Proteins_100g"
    )  # Field name made lowercase.
    carbs_100g = models.FloatField(db_column="Carbs_100g")
    # Field name made lowercase.
    sodium_100g = models.FloatField(
        db_column="Sodium_100g"
    )  # Field name made lowercase.
    front_img = models.CharField(
        db_column="Front_img", max_length=500
    )  # Field name made lowercase.
    nutrition_img = models.CharField(
        db_column="Nutrition_img", max_length=500
    )  # Field name made lowercase.
    ingredients_img = models.CharField(
        db_column="Ingredients_img", max_length=500
    )  # Field name made lowercase.
    url = models.CharField(db_column="url", max_length=500)

    objects = models.Manager()

    def __str__(self):
        return f"{self.productname}"

    class Meta:
        managed = True
        db_table = "products"
