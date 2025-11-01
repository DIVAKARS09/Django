from django.urls import path
from project import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('home/', views.home_view, name='home_view'),

    # ---------------category card-------------------

    path('category/', views.category_view, name='category_view'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.add_category, name='edit_category'),
    path('add-category/<int:category_id>/', views.add_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),

    # ---------------Item Master Card-------------------

    path('items/', views.item_list_view, name='item_list'),
    path('add-item/', views.add_item_view, name='add_item'),
    path('edit-item/<int:item_id>/', views.add_item_view, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item_view, name='delete_item'),

    # ---------------Sales form Card-------------------

    # path('sales/', views.save_sales, name='save_sales'),
    path('sales/', views.sales_list_view, name='sales_list'),        # List all sales
    path('add-sales/', views.add_sales_view, name='add_sales'),      # Add new sale
    path('edit-sales/<int:sale_id>/', views.add_sales_view, name='edit_sales'),  # Edit sale
    path('delete-sales/<int:sale_id>/', views.delete_sales_view, name='delete_sales'),  # Delete sale

    # ---------------Export-------------------
    path('export-sales/', views.export_sales, name='export_sales'),



    # ---------------Admin Page-------------------
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('user-list/', views.user_list_view, name='user_list'),
    path('admin/export/', views.export_data, name='export_data'),



    # ---------------User Rights-------------------
    path('user/<int:user_id>/rights/', views.update_user_rights, name='update_user_rights'),




    # ---------------Logut-------------------

    path('logout/', views.logout_view, name='logout'),

    path('register/admin/', views.admin_register_view, name='admin_register'),
    path('register/normal/', views.normal_register_view, name='normal_register'),

]
