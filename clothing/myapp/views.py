from django.shortcuts import render , redirect
from .models import UserProfile, Contact, Blog, Clothes, Like, Comment, Cart, Order, OrderItem
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.

def login_view(request):
    if "user_id" in request.session:      # User not logged in → Login page opens. User already logged in → Automatically redirected to Dashboard.
        return redirect("dashboard") 
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session["user_id"] = user.id
                return redirect("dashboard")
        except:
            return render(
                request,
                "accounts/login.html",{
                    "error": "Invalid Email or Password"
                })
    return render(request, "accounts/login.html")




def register(request):
    if request.method == "POST":
        user = UserProfile.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            dob=request.POST["dob"],
            password=make_password(request.POST["password"])
        )
        request.session["user_id"] = user.id
        return redirect("dashboard")
    return render(request, "accounts/register.html")



def logout(request):
    request.session.flush()
    return redirect("login")




def dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    context = {
        "user": user,
        "blog_count": Blog.objects.filter(user=user).count(),
        "contact_count": Contact.objects.filter(user=user).count(),
        "category_count": Clothes.objects.count()
    }
    return render(request,"dashboard/dashboard.html",context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = UserProfile.objects.get(email=email)
            return redirect("forgotchange_pass", user.id)
        except:
            return render(request,
                          "accounts/forgot_password.html",
                          {"error": "Email not found"})
    return render(request, "accounts/forgot_password.html")



def forgotchange_pass(request, id):
    user = UserProfile.objects.get(id=id)
    if request.method == "POST":
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]
        if password == confirm:
            user.password = make_password(password)
            user.save()
            return redirect("login")
        else:
            return render(request,
                          "accounts/change_password.html",
                          {"error": "Password doesn't match"})
    return render(request, "accounts/forgotchange_pass.html")






def change_password(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["new_password"]
        confirm = request.POST["confirm_password"]
        # if user.password != old:
        if not check_password(old, user.password):
            return render(request,"accounts/change_password.html",{"error":"Old password is incorrect."})
        if new != confirm:
            return render(request,"accounts/change_password.html",{"error":"Passwords do not match."})
        user.password = make_password(new)
        user.save()
        request.session.flush()
        return redirect("login")
    return render(request,"accounts/change_password.html")




# def profile(request):
#     if "user_id" not in request.session:
#         return redirect("login")
#     user = UserProfile.objects.get(id=request.session["user_id"])
#     return render(request, "accounts/profile.html", {
#         "user": user
#     })



def edit_profile(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        user.name = name
        user.phone = phone
        user.dob = dob
        user.save()
        return redirect("dashboard")
    context = {"user": user}
    return render(request,"dashboard/edit_profile.html", context)





def contacts(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    contacts = Contact.objects.filter(
        user=user
    )
     # Search
    search = request.GET.get("q")
    if search:
        contacts = contacts.filter(
            name__icontains=search
        )
    context = {"contacts":contacts }
    return render(request,"contacts/contacts.html",context)



def add_contact(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    if request.method=="POST":
        name=request.POST["name"]
        contact_no=request.POST["contact_no"]
        Contact.objects.create(
            user=user,
            name=name,
            contact_no=contact_no
        )
        return redirect("contacts")
    return render(request, "contacts/add_contact.html")




def view_contact(request,id):
    contact = Contact.objects.get(id=id)
    return render(request,"contacts/view_contact.html",{"contact":contact})




def update_contact(request,id):
    contact = Contact.objects.get(id=id)
    if request.method=="POST":
        contact.name=request.POST["name"]
        contact.contact_no=request.POST["contact_no"]
        contact.save()
        return redirect("contacts")
    return render(request,"contacts/update_contact.html",{"contact":contact})




def delete_contact(request,id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect("contacts")









def add_blog(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        Blog.objects.create(
            user=user,
            title=title,
            description=description
        )
        return redirect("blog_list")
    return render(request,"blogs/add_blog.html")



def blog_list(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"]
    )
    blogs = Blog.objects.filter(
        user=user
    )
    search = request.GET.get("q")
    if search:
        blogs = blogs.filter(
            title__icontains=search
        )
    context = {"blogs": blogs}
    return render(request,"blogs/blog_list.html",context)



def view_blog(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
        id=request.session["user_id"])
    blog = Blog.objects.get(id=id,user=user)
    context = {"blog": blog}
    return render(request,"blogs/view_blog.html",context)



def edit_blog(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
           id=request.session["user_id"])
    blog = Blog.objects.get(id=id,user=user)
    if request.method == "POST":
        blog.title = request.POST["title"]
        blog.description = request.POST["description"]
        blog.save()
        return redirect("blog_list")
    context = {"blog": blog}
    return render(request,"blogs/edit_blog.html",context)



def delete_blog(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    user = UserProfile.objects.get(
            id=request.session["user_id"]) 
    blog = Blog.objects.get(id=id,user=user)
    blog.delete()
    return redirect("blog_list")


def all_blogs(request):
    if "user_id" not in request.session:
        return redirect("login")
    
    user = UserProfile.objects.get(id=request.session["user_id"])
    blogs = Blog.objects.all().order_by("-id")
    
    search = request.GET.get("q")
    if search:
        blogs = blogs.filter(title__icontains=search)

    liked_blog_ids = Like.objects.filter(user=user).values_list("blog_id", flat=True)

    context = {
        "blogs": blogs,
        "liked_blog_ids": liked_blog_ids,
        "current_user": user
    }
    return render(request, "blogs/all_blogs.html", context)


def like_blog(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    
    user = UserProfile.objects.get(id=request.session["user_id"])
    blog = Blog.objects.get(id=id)
    
    existing_like = Like.objects.filter(user=user, blog=blog)
    if existing_like.exists():
        existing_like.delete()
    else:
        Like.objects.create(user=user, blog=blog)
        
    return redirect("all_blogs")


def add_comment(request, id):
    if "user_id" not in request.session:
        return redirect("login")
        
    if request.method == "POST":
        comment_text = request.POST["comment_text"]
        user = UserProfile.objects.get(id=request.session["user_id"])
        blog = Blog.objects.get(id=id)
        
        Comment.objects.create(
            user=user,
            blog=blog,
            comment_text=comment_text
        )
        return redirect("all_blogs")
    return redirect("all_blogs")




# user = UserProfile.objects.get(
#             id=request.session["user_id"]) 
# blog = Blog.objects.get(id=id,user=user)
# Django will only find a blog where:
# id matches the URL and
# user is the currently logged-in user.
# So User 1 cannot access User 2's blogs.
# jo aa 3 line ni jagya e khali aatlu lakhyu hot blog = Blog.objects.get(id=id) to Imagine there are two users: User 1 Blog ID 1 Blog ID 2 User 2 Blog ID 3 If you use: Blog.objects.get(id=id)...then User 1 could type this URL: http://127.0.0.1:8000/view-blog/3/ and can see User 2's blog.







def category_dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")
        
    if Clothes.objects.count() == 0:
        Clothes.objects.create(
            name="Jockey Microfiber Men's T-shirt -MV16",
            desc="Premium breathable microfiber active t-shirt for maximum comfort.",
            price=799,
            image="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
            gender="Men",
            type="Upper"
        )
        Clothes.objects.create(
            name="Men's Slim Fit Cotton Polo Shirt",
            desc="Classic polo shirt made from 100% combed cotton.",
            price=999,
            image="https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500",
            gender="Men",
            type="Upper"
        )
        Clothes.objects.create(
            name="Men's Cotton Track Pants",
            desc="Comfortable athletic track pants for workout and leisure.",
            price=1299,
            image="https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=500",
            gender="Men",
            type="Lower"
        )
        Clothes.objects.create(
            name="Women's Floral Printed Casual Top",
            desc="Lightweight floral print top for everyday casual wear.",
            price=699,
            image="https://images.unsplash.com/photo-1564584217132-2271feaeb3c5?w=500",
            gender="Women",
            type="Upper"
        )
        Clothes.objects.create(
            name="Women's High-Waist Denim Jeans",
            desc="Stylish high-rise stretch denim jeans for modern look.",
            price=1499,
            image="https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
            gender="Women",
            type="Lower"
        )

    gender = request.GET.get("gender")
    item_type = request.GET.get("type")

    if gender and item_type:
        clothes = Clothes.objects.filter(gender=gender, type=item_type)
        category_title = f"{gender}'s {item_type} Clothing"
    elif gender:
        clothes = Clothes.objects.filter(gender=gender)
        category_title = f"{gender}'s Collection"
    else:
        clothes = Clothes.objects.all()
        category_title = "All Products"

    user = UserProfile.objects.get(id=request.session["user_id"])
    cart_count = Cart.objects.filter(user=user).count()

    context = {
        "clothes": clothes,
        "category_title": category_title,
        "selected_gender": gender,
        "selected_type": item_type,
        "cart_count": cart_count,
    }
    return render(request, "categories/dashboard.html", context)


# ==========================================
# CUSTOM ADMIN PANEL VIEWS
# ==========================================

def admin_login(request):
    if not UserProfile.objects.filter(email="admin@gmail.com").exists():
        UserProfile.objects.create(
            name="Admin",
            email="admin@gmail.com",
            phone="9999999999",
            dob="2000-01-01",
            password="admin",
            is_admin=True
        )

    if "admin_id" in request.session:
        return redirect("admin_dashboard")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = UserProfile.objects.get(email=email, password=password)
            if user.is_admin or email == "admin@gmail.com":
                request.session["admin_id"] = user.id
                return redirect("admin_dashboard")
            else:
                return render(request, "customadmin/admin_login.html", {"error": "Access Denied. You are not an Admin."})
        except:
            return render(request, "customadmin/admin_login.html", {"error": "Invalid Admin Email or Password"})

    return render(request, "customadmin/admin_login.html")


def admin_dashboard(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    admin_user = UserProfile.objects.get(id=request.session["admin_id"])
    context = {
        "admin_user": admin_user,
        "users_count": UserProfile.objects.filter(is_admin=False).count(),
        "blogs_count": Blog.objects.count(),
        "contacts_count": Contact.objects.count(),
        "clothes_count": Clothes.objects.count(),
        "likes_count": Like.objects.count(),
        "comments_count": Comment.objects.count(),
        "orders_count": Order.objects.count()
    }
    return render(request, "customadmin/admin_dashboard.html", context)


# ==========================================
# USERS CRUD (Custom Admin)
# ==========================================
def admin_users(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    users = UserProfile.objects.filter(is_admin=False)
    search = request.GET.get("q")
    if search:
        users = users.filter(name__icontains=search)
    context = {"users": users}
    return render(request, "customadmin/admin_users.html", context)


def admin_add_user(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        password = request.POST["password"]
        UserProfile.objects.create(
            name=name,
            email=email,
            phone=phone,
            dob=dob,
            password=password
        )
        return redirect("admin_users")
    return render(request, "customadmin/admin_add_user.html")


def admin_edit_user(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    user_item = UserProfile.objects.get(id=id)
    if request.method == "POST":
        user_item.name = request.POST["name"]
        user_item.email = request.POST["email"]
        user_item.phone = request.POST["phone"]
        user_item.dob = request.POST["dob"]
        user_item.password = request.POST["password"]
        user_item.save()
        return redirect("admin_users")
    context = {"user_item": user_item}
    return render(request, "customadmin/admin_edit_user.html", context)


def admin_delete_user(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    user = UserProfile.objects.get(id=id)
    user.delete()
    return redirect("admin_users")


# ==========================================
# CLOTHES CRUD (Custom Admin)
# ==========================================
def admin_clothes(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    clothes = Clothes.objects.all()
    search = request.GET.get("q")
    if search:
        clothes = clothes.filter(name__icontains=search)
    context = {"clothes": clothes}
    return render(request, "customadmin/admin_clothes.html", context)


def admin_add_clothes(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST["name"]
        desc = request.POST["desc"]
        price = request.POST["price"]
        image = request.FILES["image"]
        gender = request.POST["gender"]
        type = request.POST["type"]
        Clothes.objects.create(
            name=name,
            desc=desc,
            price=price,
            image=image,
            gender=gender,
            type=type
        )
        return redirect("admin_clothes")
    return render(request, "customadmin/admin_add_clothes.html")


def admin_edit_clothes(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    item = Clothes.objects.get(id=id)
    if request.method == "POST":
        item.name = request.POST["name"]
        item.desc = request.POST["desc"]
        if "image" in request.FILES: # "If the admin selected a new image, replace the old image." Otherwise,"Keep the existing image." and the admin edits only the price without choosing a new file, Django will give: MultiValueDictKeyError: 'image' So the if statement avoids that error.
            item.image = request.FILES["image"]
        item.image = request.FILES["image"]
        item.gender = request.POST["gender"]
        item.type = request.POST["type"]
        item.save()
        return redirect("admin_clothes")
    context = {"item": item}
    return render(request, "customadmin/admin_edit_clothes.html", context)


def admin_delete_clothes(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    item = Clothes.objects.get(id=id)
    item.delete()
    return redirect("admin_clothes")


# ==========================================
# BLOGS CRUD (Custom Admin)
# ==========================================
def admin_blogs(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    blogs = Blog.objects.all().order_by("-id")
    search = request.GET.get("q")
    if search:
        blogs = blogs.filter(title__icontains=search)
    context = {"blogs": blogs}
    return render(request, "customadmin/admin_blogs.html", context)


def admin_add_blog(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        user_id = request.POST["user_id"]
        title = request.POST["title"]
        description = request.POST["description"]
        user = UserProfile.objects.get(id=user_id)
        Blog.objects.create(
            user=user,
            title=title,
            description=description
        )
        return redirect("admin_blogs")
    users = UserProfile.objects.all()
    return render(request, "customadmin/admin_add_blog.html", {"users": users})


def admin_edit_blog(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        user_id = request.POST["user_id"]
        blog.user = UserProfile.objects.get(id=user_id)
        blog.title = request.POST["title"]
        blog.description = request.POST["description"]
        blog.save()
        return redirect("admin_blogs")
    users = UserProfile.objects.all()
    context = {"blog": blog, "users": users}
    return render(request, "customadmin/admin_edit_blog.html", context)


def admin_delete_blog(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("admin_blogs")


# ==========================================
# CONTACTS CRUD (Custom Admin)
# ==========================================
def admin_contacts(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    contacts = Contact.objects.all().order_by("-id")
    search = request.GET.get("q")
    if search:
        contacts = contacts.filter(name__icontains=search)
    context = {"contacts": contacts}
    return render(request, "customadmin/admin_contacts.html", context)


def admin_add_contact(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        user_id = request.POST["user_id"]
        name = request.POST["name"]
        contact_no = request.POST["contact_no"]
        user = UserProfile.objects.get(id=user_id)
        Contact.objects.create(
            user=user,
            name=name,
            contact_no=contact_no
        )
        return redirect("admin_contacts")
    users = UserProfile.objects.all()
    return render(request, "customadmin/admin_add_contact.html", {"users": users})


def admin_edit_contact(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    contact = Contact.objects.get(id=id)
    if request.method == "POST":
        user_id = request.POST["user_id"]
        contact.user = UserProfile.objects.get(id=user_id)
        contact.name = request.POST["name"]
        contact.contact_no = request.POST["contact_no"]
        contact.save()
        return redirect("admin_contacts")
    users = UserProfile.objects.all()
    context = {"contact": contact, "users": users}
    return render(request, "customadmin/admin_edit_contact.html", context)


def admin_delete_contact(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect("admin_contacts")


# ==========================================
# LIKES CRUD (Custom Admin)
# ==========================================
def admin_likes(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    likes = Like.objects.all().order_by("-id")
    context = {"likes": likes}
    return render(request, "customadmin/admin_likes.html", context)


def admin_add_like(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        user_id = request.POST["user_id"]
        blog_id = request.POST["blog_id"]
        user = UserProfile.objects.get(id=user_id)
        blog = Blog.objects.get(id=blog_id)
        if not Like.objects.filter(user=user, blog=blog).exists():
            Like.objects.create(user=user, blog=blog)
        return redirect("admin_likes")
    users = UserProfile.objects.all()
    blogs = Blog.objects.all()
    return render(request, "customadmin/admin_add_like.html", {"users": users, "blogs": blogs})


def admin_delete_like(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    like = Like.objects.get(id=id)
    like.delete()
    return redirect("admin_likes")


# ==========================================
# COMMENTS CRUD (Custom Admin)
# ==========================================
def admin_comments(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    comments = Comment.objects.all().order_by("-id")
    search = request.GET.get("q")
    if search:
        comments = comments.filter(comment_text__icontains=search)
    context = {"comments": comments}
    return render(request, "customadmin/admin_comments.html", context)


def admin_add_comment(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        user_id = request.POST["user_id"]
        blog_id = request.POST["blog_id"]
        comment_text = request.POST["comment_text"]
        user = UserProfile.objects.get(id=user_id)
        blog = Blog.objects.get(id=blog_id)
        Comment.objects.create(
            user=user,
            blog=blog,
            comment_text=comment_text
        )
        return redirect("admin_comments")
    users = UserProfile.objects.all()
    blogs = Blog.objects.all()
    return render(request, "customadmin/admin_add_comment.html", {"users": users, "blogs": blogs})


def admin_edit_comment(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    comment = Comment.objects.get(id=id)
    if request.method == "POST":
        user_id = request.POST["user_id"]
        blog_id = request.POST["blog_id"]
        comment.user = UserProfile.objects.get(id=user_id)
        comment.blog = Blog.objects.get(id=blog_id)
        comment.comment_text = request.POST["comment_text"]
        comment.save()
        return redirect("admin_comments")
    users = UserProfile.objects.all()
    blogs = Blog.objects.all()
    context = {"comment": comment, "users": users, "blogs": blogs}
    return render(request, "customadmin/admin_edit_comment.html", context)


def admin_delete_comment(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect("admin_comments")


def admin_logout(request):
    if "admin_id" in request.session:
        del request.session["admin_id"]
    return redirect("admin_login")


# ==========================================
# CART & PAYMENT VIEWS
# ==========================================

def add_to_cart(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    
    user = UserProfile.objects.get(id=request.session["user_id"])
    product = Clothes.objects.get(id=id)

    existing_item = Cart.objects.filter(user=user, product=product).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        Cart.objects.create(user=user, product=product, quantity=1)

    return redirect("payment_page")


def update_cart_qty(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    cart_item = Cart.objects.get(id=id)
    action = request.GET.get("action")
    
    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("payment_page")


def remove_from_cart(request, id):
    if "user_id" not in request.session:
        return redirect("login")
    
    cart_item = Cart.objects.get(id=id)
    cart_item.delete()
    return redirect("payment_page")


def payment_page(request):
    if "user_id" not in request.session:
        return redirect("login")
    
    user = UserProfile.objects.get(id=request.session["user_id"])
    cart_items = Cart.objects.filter(user=user)

    subtotal = 0
    for item in cart_items:
        subtotal += item.product.price * item.quantity

    shipping_fee = 50 if subtotal > 0 else 0
    total_amount = subtotal + shipping_fee

    context = {
        "user": user,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total_amount": total_amount,
    }
    return render(request, "payment/payment.html", context)


def place_order(request):
    if "user_id" not in request.session:
        return redirect("login")
    
    if request.method == "POST":
        user = UserProfile.objects.get(id=request.session["user_id"])
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return redirect("category_dashboard")

        name = request.POST["name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        city = request.POST["city"]
        pincode = request.POST["pincode"]
        payment_method = request.POST.get("payment_method", "Cash on Delivery")

        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_fee = 50 if subtotal > 0 else 0
        total_amount = subtotal + shipping_fee

        order = Order.objects.create(
            user=user,
            name=name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=total_amount,
            status="Paid"
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        cart_items.delete()

        return redirect(f"/order-success/?order_id={order.id}")

    return redirect("payment_page")


def order_success(request):
    if "user_id" not in request.session:
        return redirect("login")
    
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        "order": order,
        "order_items": order_items
    }
    return render(request, "payment/order_success.html", context)


# ==========================================
# ORDERS CRUD (Custom Admin)
# ==========================================

def admin_orders(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    orders = Order.objects.all().order_by("-id")
    search = request.GET.get("q")
    if search:
        orders = orders.filter(name__icontains=search)
    context = {"orders": orders}
    return render(request, "customadmin/admin_orders.html", context)


def admin_delete_order(request, id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    order = Order.objects.get(id=id)
    order.delete()
    return redirect("admin_orders")