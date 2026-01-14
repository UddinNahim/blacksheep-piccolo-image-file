from piccolo.table import Table
from piccolo.columns import Varchar ,Text,ForeignKey , Decimal

class Product(Table):
    name = Varchar(length=255)
    description = Text()

class ProductVariations(Table) :
    product_id = ForeignKey(references=Product)
    sku = Varchar(length=100, unique=True)
    price = Decimal(precision=(10, 2))

class ProductAttributeName(Table):
    name = Varchar(length=100)

class ProductAttributeValue(Table):
    variation_id = ForeignKey(references=ProductVariations)
    attribute_id = ForeignKey(references=ProductAttributeName)
    attribute_value = Varchar(length=255)


class Product(Table):
    name = Varchar(length=255)
    description = Text()


class ProductVariations(Table) :
    sku = Varchar(length=100, unique=True)
    price = Decimal(precision=(10, 2))
    p_attribute = ForeignKey(references=ProductAttribute)



class ProductAttribute(Table):
    p_attribute_name = ForeignKey(references=ProductAttributeName)
    p_attribute_value = ForeignKey(references=ProductAttributeValue)

class ProductAttributeName(Table):
    name = Varchar(length=100)

class ProductAttributeValue(Table):
    attribute_value = Varchar(length=255)

