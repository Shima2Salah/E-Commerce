#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.product import Product

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new Product --")
my_product = Product()
my_product.product_name = "shirt"
my_product.price= 123.5
my_product.description = "fghmnm ghbg fbgfb"
my_product.image_url = "root/images/shirt"
my_product.category_id = 2
my_product.save()
print(my_product)

print("-- Create a new Product 2 --")
my_product2 = Product()
my_product2.product_name = "shirt"
my_product2.price= 123.5
my_product2.description = "fghmnm ghbg fbgfb"
my_product2.image_url = "root/images/shirt"
my_product2.category_id = 2
my_product2.save()
print(my_product2)
