from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("forgotchange_pass/<int:id>/", views.forgotchange_pass, name="forgotchange_pass"),
    # path("profile/", views.profile, name="profile"),
    path("change-password/",views.change_password,name="change_password"),
    path('edit-profile/',views.edit_profile,name='edit_profile'),
    path('contacts/',views.contacts,name='contacts'),
    path('add-contact/',views.add_contact,name='add_contact'),
    path('view-contact/<int:id>/',views.view_contact,name='view_contact'),
    path('update-contact/<int:id>/',views.update_contact,name='update_contact'),
    path('delete-contact/<int:id>/',views.delete_contact,name='delete_contact'),
    path("blogs/",views.blog_list,name="blog_list"),
    path("all-blogs/", views.all_blogs, name="all_blogs"),
    path("like-blog/<int:id>/", views.like_blog, name="like_blog"),
    path("add-comment/<int:id>/", views.add_comment, name="add_comment"),
    path("add-blog/",views.add_blog,name="add_blog"),
    path("view-blog/<int:id>/",views.view_blog,name="view_blog"),
    path("edit-blog/<int:id>/",views.edit_blog,name="edit_blog"),
    path("delete-blog/<int:id>/",views.delete_blog,name="delete_blog"),




    path("category-dashboard/",views.category_dashboard,name="category_dashboard"),

    # Custom Admin Routes
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Admin Users
    path("admin-users/", views.admin_users, name="admin_users"),
    path("admin-add-user/", views.admin_add_user, name="admin_add_user"),
    path("admin-edit-user/<int:id>/", views.admin_edit_user, name="admin_edit_user"),
    path("admin-delete-user/<int:id>/", views.admin_delete_user, name="admin_delete_user"),

    # Admin Clothes
    path("admin-clothes/", views.admin_clothes, name="admin_clothes"),
    path("admin-add-clothes/", views.admin_add_clothes, name="admin_add_clothes"),
    path("admin-edit-clothes/<int:id>/", views.admin_edit_clothes, name="admin_edit_clothes"),
    path("admin-delete-clothes/<int:id>/", views.admin_delete_clothes, name="admin_delete_clothes"),

    # Admin Blogs
    path("admin-blogs/", views.admin_blogs, name="admin_blogs"),
    path("admin-add-blog/", views.admin_add_blog, name="admin_add_blog"),
    path("admin-edit-blog/<int:id>/", views.admin_edit_blog, name="admin_edit_blog"),
    path("admin-delete-blog/<int:id>/", views.admin_delete_blog, name="admin_delete_blog"),

    # Admin Contacts
    path("admin-contacts/", views.admin_contacts, name="admin_contacts"),
    path("admin-add-contact/", views.admin_add_contact, name="admin_add_contact"),
    path("admin-edit-contact/<int:id>/", views.admin_edit_contact, name="admin_edit_contact"),
    path("admin-delete-contact/<int:id>/", views.admin_delete_contact, name="admin_delete_contact"),

    # Admin Likes
    path("admin-likes/", views.admin_likes, name="admin_likes"),
    path("admin-add-like/", views.admin_add_like, name="admin_add_like"),
    path("admin-delete-like/<int:id>/", views.admin_delete_like, name="admin_delete_like"),

    # Admin Comments
    path("admin-comments/", views.admin_comments, name="admin_comments"),
    path("admin-add-comment/", views.admin_add_comment, name="admin_add_comment"),
    path("admin-edit-comment/<int:id>/", views.admin_edit_comment, name="admin_edit_comment"),
    path("admin-delete-comment/<int:id>/", views.admin_delete_comment, name="admin_delete_comment"),

    # Admin Orders
    path("admin-orders/", views.admin_orders, name="admin_orders"),
    path("admin-delete-order/<int:id>/", views.admin_delete_order, name="admin_delete_order"),

    # Cart & Payment Routes
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/<int:id>/", views.update_cart_qty, name="update_cart_qty"),
    path("remove-cart/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("payment/", views.payment_page, name="payment_page"),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/", views.order_success, name="order_success"),

    path("admin-logout/", views.admin_logout, name="admin_logout"),
]