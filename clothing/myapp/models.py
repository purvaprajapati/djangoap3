from django.db import models

# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    

class Blog(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=200
    )
    description = models.TextField()
    def __str__(self):
        return self.title

    

class Contact(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100
    )
    contact_no = models.CharField(
        max_length=15
    )
    def __str__(self):
        return self.name



class Clothes(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    image = models.FileField(upload_to="product/")  
    gender = models.CharField(max_length=10, default="Men")
    type = models.CharField(max_length=10, default="Upper")
    
    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if not self.image:
            return "https://images.unsplash.com/photo-1523381294911-8d3cead13475?w=500&q=80"
        
        try:
            import urllib.parse
            name_str = str(self.image.name) if self.image else ""
            url_str = str(self.image.url) if hasattr(self.image, 'url') else name_str
            
            for s in [name_str, url_str]:
                if not s:
                    continue
                unquoted = urllib.parse.unquote(str(s))
                for proto in ["https://", "http://", "https:/", "http:/"]:
                    idx = unquoted.find(proto)
                    if idx != -1:
                        clean = unquoted[idx:]
                        if clean.startswith("https:/") and not clean.startswith("https://"):
                            clean = clean.replace("https:/", "https://", 1)
                        elif clean.startswith("http:/") and not clean.startswith("http://"):
                            clean = clean.replace("http:/", "http://", 1)
                        return clean
            return url_str
        except Exception:
            return "https://images.unsplash.com/photo-1523381294911-8d3cead13475?w=500&q=80"





class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} likes {self.blog.title}"


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.comment_text[:20]}"


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Paid")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"