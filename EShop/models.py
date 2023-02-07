from django.db import models

# Create your models here.

class Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    DateModified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master'

    def __str__(self) -> str:
        return self.Email


class Customers(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    ProfileImage = models.ImageField(upload_to="profiles/", default='avatar.png')
    Gender = models.CharField(max_length=10)
    BirthDate = models.DateField(default="1990-01-01")
    State = models.CharField(max_length=30, blank=True, default='')
    City =  models.CharField(max_length=30, blank=True, default='')
    HomeAddress = models.CharField(max_length=30, blank=True, default='')
    OfficeAddress = models.CharField(max_length=30, blank=True, default='')
    OtherAddress = models.CharField(max_length=30, blank=True, default='')
    Pincode = models.CharField(max_length=6,blank=True,default='')

    class Meta:
        db_table = 'Customers' 


    def __str__(self) -> str:
        return self.Master.Email

    
class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=50)
    ProductPrice = models.DecimalField(max_digits=7, decimal_places=2)
    ProductQuantity = models.CharField(max_length=50)
    ProductDescription = models.TextField(max_length=250)
    ProductImage = models.ImageField(upload_to="Upload/Products", height_field=None, width_field=None, max_length=None)

    class Meta:
        db_table = "product"

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()

    def __str__(self) -> str:
        return self.ProductName


class Wishlist(models.Model):
    Customers = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'


class Cart(models.Model):
    Customers = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    TotalPrice = models.DecimalField(decimal_places=2, max_digits=7)

    class Meta:
        db_table = 'cart'

    def __str__(self) -> str:
        return self.Product