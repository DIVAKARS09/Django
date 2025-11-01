from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, LoginForm, CategoryForm, ItemForm, SalesForm, SaleItemForm, SaleItemFormSetCleanBlank
from .models import UserProfile, Category, Item, Sales, SaleItem
from django.forms import modelformset_factory




# ==================== LOGIN VIEW ====================
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = UserProfile.objects.get(email=email)
                if check_password(password, user.password):
                    # ✅ Store session data
                    request.session['user_id'] = user.id
                    request.session['username'] = user.name
                    request.session['is_admin'] = user.is_admin  # Optional: useful for quick access

                    messages.success(request, f"✅ Welcome back, {user.name}!")
                    return redirect('home_view')
                else:
                    messages.error(request, '❌ Incorrect password.')
            except UserProfile.DoesNotExist:
                messages.error(request, '❌ Email not registered.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})




def admin_register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.is_admin = True  # ✅ Mark as admin
            user.save()
            messages.success(request, "✅ Admin registered successfully!")
            return redirect('login_view')
    else:
        form = RegistrationForm()
    return render(request, 'admin_register.html', {'form': form})


def normal_register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.is_admin = False  # ✅ Mark as normal user
            user.save()
            messages.success(request, "✅ User registered successfully!")
            return redirect('login_view')
    else:
        form = RegistrationForm()
    return render(request, 'normal_register.html', {'form': form})



# ==================== REGISTER VIEW ====================

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])

            # ✅ Detect "admin" in email (case-insensitive)
            if 'admin' in user.email.lower():
                user.is_admin = True

                # Optional: auto-assign full permissions
                user.can_add_category = True
                user.can_edit_category = True
                user.can_delete_category = True
                user.can_add_item = True
                user.can_edit_item = True
                user.can_delete_item = True
                user.can_add_sale = True
                user.can_edit_sale = True
                user.can_delete_sale = True
                user.can_access_category_page = True
                user.can_access_item_page = True
                user.can_access_sales_page = True

            user.save()
            messages.success(request, "✅ Registered successfully! Please log in.")
            return redirect('login_view')
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



# ------------------- HOME VIEW -------------------

def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in to access the home page.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    return render(request, 'home.html', {
        'username': user.name,
        'is_admin': user.is_admin,
        'user': user
    })

def category_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in to access categories.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if user.is_customized_by_admin and not user.can_access_category_page:
        messages.error(request, "🚫 You do not have access to the Category page.")
        return redirect('home_view')

    categories = Category.objects.all().order_by('name')

    return render(request, 'category.html', {
        'categories': categories,
        'user': user,
        'can_add': user.can_add_category,
        'can_edit': user.can_edit_category,
        'can_delete': user.can_delete_category,
    })

def add_category(request, category_id=None):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in to continue.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if category_id:
        if not user.can_edit_category:
            messages.error(request, "🚫 You do not have permission to edit categories.")
            return redirect('category_view')
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        edit_mode = True
    else:
        if not user.can_add_category:
            messages.error(request, "🚫 You do not have permission to add categories.")
            return redirect('category_view')
        category = None
        form = CategoryForm()
        edit_mode = False

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.status = int(form.cleaned_data.get('status'))
            category.save()
            messages.success(request, "✅ Category saved successfully!" if not edit_mode else "✏️ Category updated successfully!")
            return redirect('category_view')

    return render(request, 'add_category.html', {
        'form': form,
        'edit_mode': edit_mode
    })

def delete_category(request, category_id):
    if 'user_id' not in request.session:
        messages.warning(request, "⚠️ Please log in first.")
        return redirect('login_view')

    category = get_object_or_404(Category, id=category_id)
    name = category.name

    if Item.objects.filter(category=category).exists():
        messages.error(request, f"❌ Cannot delete — Category '{name}' is used in items.")
    else:
        category.delete()
        messages.success(request, f"🗑️ Category '{name}' deleted successfully!")

    return redirect('category_view')

def item_list_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in to access the items page.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if user.is_customized_by_admin and not user.can_access_item_page:
        messages.error(request, "🚫 You do not have access to the Item page.")
        return redirect('home_view')

    items = Item.objects.all().order_by('name')

    return render(request, 'item_list.html', {
        'items': items,
        'user': user,
        'can_add': user.can_add_item,
        'can_edit': user.can_edit_item,
        'can_delete': user.can_delete_item,
    })

# ------------------- ADD / EDIT ITEM -------------------
def add_item_view(request, item_id=None):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in first.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if item_id:
        if not user.can_edit_item:
            messages.error(request, "🚫 You do not have permission to edit items.")
            return redirect('item_list')
        item = get_object_or_404(Item, id=item_id)
        form = ItemForm(instance=item)
        edit_mode = True
    else:
        if not user.can_add_item:
            messages.error(request, "🚫 You do not have permission to add items.")
            return redirect('item_list')
        item = None
        form = ItemForm()
        edit_mode = False

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            saved_item = form.save()
            if edit_mode:
                messages.info(request, f"✏️ '{saved_item}' Item updated successfully!")
            else:
                messages.success(request, f"✅ Item added successfully!")
            return redirect('item_list')

    return render(request, 'add_item.html', {
        'form': form,
        'edit_mode': edit_mode
    })

# ------------------- DELETE ITEM -------------------

def delete_item_view(request, item_id):
    if 'user_id' not in request.session:
        messages.warning(request, "⚠️ Please log in first.")
        return redirect('login_view')

    item = get_object_or_404(Item, id=item_id)
    name = item.name

    # ✅ Use the actual Item instance
    if SaleItem.objects.filter(item=item).exists():
        messages.error(request, f"❌ Cannot delete — Item '{name}' is already used in sales records.")
    else:
        item.delete()
        messages.success(request, f"🗑️ Item '{name}' deleted successfully!")

    return redirect('item_list')



# ==================== SALES LIST VIEW ====================

def sales_list_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in to access sales.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if user.is_customized_by_admin and not user.can_access_sales_page:
        messages.error(request, "🚫 You do not have access to the Sales page.")
        return redirect('home_view')

    sales = Sales.objects.prefetch_related('items__item__category').all()

    return render(request, 'sales_list.html', {
        'sales': sales,
        'user': user,
        'can_add': user.can_add_sale,
        'can_edit': user.can_edit_sale,
        'can_delete': user.can_delete_sale,
    })

# ------------------- ADD / EDIT SALE -------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from datetime import date
from .models import Sales, SaleItem, Item, UserProfile
from .forms import SalesForm, SaleItemForm, SaleItemFormSetCleanBlank

def add_sales_view(request, sale_id=None):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in first.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    SaleItemFormSet = inlineformset_factory(
        Sales, SaleItem,
        form=SaleItemForm,
        formset=SaleItemFormSetCleanBlank,
        extra=0,
        can_delete=True
    )

    sale = None
    edit_mode = False
    bill_date = date.today().strftime("%d/%m/%Y")

    if sale_id:
        if not user.can_edit_sale:
            messages.error(request, "🚫 You do not have permission to edit sales.")
            return redirect('sales_list')

        sale = get_object_or_404(Sales, id=sale_id)
        edit_mode = True
        bill_number = sale.bill_number
        bill_date = sale.date.strftime("%d/%m/%Y")
    else:
        if not user.can_add_sale:
            messages.error(request, "🚫 You do not have permission to add sales.")
            return redirect('sales_list')

        last_sale = Sales.objects.order_by('-id').first()
        next_id = (last_sale.id + 1) if last_sale else 1
        bill_number = f'BILL-{next_id:04d}'

    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale, prefix='form')

        if form.is_valid() and formset.is_valid():
            saved_sale = form.save(commit=False)
            saved_sale.created_by = request.user if request.user.is_authenticated else None
            saved_sale.date = date.today()
            saved_sale.bill_number = bill_number
            saved_sale.save()

            total = 0
            items = formset.save(commit=False)
            for item in items:
                if item.item:
                    item.sales = saved_sale
                    item.rate = item.rate or item.item.price
                    subtotal = item.quantity * item.rate
                    discount_amount = subtotal * (item.discount / 100)
                    item.total_price = subtotal - discount_amount
                    item.save()
                    total += item.total_price

            for obj in formset.deleted_objects:
                obj.delete()

            saved_sale.total_price = total
            saved_sale.save()

            messages.success(request, f"✅ Sale {'updated' if edit_mode else 'added'}! Bill Number: {saved_sale.bill_number}")
            return redirect('sales_list')
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
            messages.error(request, "❌ Please fix the errors in the form.")
    else:
        form = SalesForm(instance=sale)
        formset = SaleItemFormSet(instance=sale, prefix='form')

    items = Item.objects.all()

    return render(request, 'add_sales.html', {
        'form': form,
        'formset': formset,
        'edit_mode': edit_mode,
        'items': items,
        'bill_number': bill_number,
        'bill_date': bill_date,
    })





def delete_sales_view(request, sale_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "⚠️ Please log in first.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "❌ Invalid user session.")
        return redirect('login_view')

    if not user.can_delete_sale:
        messages.error(request, "🚫 You do not have permission to delete sales.")
        return redirect('sales_list')

    sale = get_object_or_404(Sales, id=sale_id)
    sale.delete()
    messages.success(request, f"🗑 Sale {sale.bill_number} deleted successfully.")
    return redirect('sales_list')


# ==================== Admin Check ====================
def user_list_view(request):
    current_user = UserProfile.objects.get(id=request.session.get('user_id'))
    if not current_user.is_admin:
        messages.error(request, "❌ Access denied.")
        return redirect('home_view')

    admin_users = UserProfile.objects.filter(is_admin=True)
    normal_users = UserProfile.objects.filter(is_admin=False)

    return render(request, 'user_list.html', {
        'admin_users': admin_users,
        'normal_users': normal_users,
        'is_admin': current_user.is_admin
    })



# ==================== Admin Page ====================
def admin_dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please log in.")
        return redirect('login_view')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid session.")
        return redirect('login_view')

    if not user.is_admin:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home_view')

    # ✅ Fetch dashboard data
    total_categories = Category.objects.count()
    total_items = Item.objects.count()
    total_sales = Sales.objects.count()
    recent_sales = Sales.objects.order_by('-date')[:5]

    return render(request, 'admin_dashboard.html', {
        'user': user,
        'total_categories': total_categories,
        'total_items': total_items,
        'total_sales': total_sales,
        'recent_sales': recent_sales,
    })



# ==================== Export ====================

import io
from django.http import HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook

from .models import Sales, SaleItem

def export_sales(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_sales')
        export_type = request.POST.get('export_type')

        sales = Sales.objects.filter(id__in=selected_ids) if selected_ids else Sales.objects.all()

        if not sales.exists():
            messages.warning(request, "⚠️ No sales data available to export.")
            return redirect('sales_list')

        if export_type == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            x = 50
            y = height - 50
            p.setFont("Helvetica-Bold", 14)
            p.drawString(x, y, "Sales Report")
            y -= 30
            p.setFont("Helvetica", 10)

            for sale in sales:
                items = SaleItem.objects.filter(sales=sale)
                for item in items:
                    line = [
                        str(sale.bill_number),
                        sale.customer_name,
                        item.item.name,
                        str(item.quantity),
                        f"₹{item.rate}",
                        f"{item.item.price} → ₹{item.rate}",
                        f"₹{item.total_price}",
                        str(sale.date),
                        sale.payment_mode
                    ]
                    p.drawString(x, y, "    ".join(line))
                    y -= 15
                    if y < 50:
                        p.showPage()
                        y = height - 50
                        p.setFont("Helvetica", 10)

            p.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
            return response

        elif export_type == 'excel':
            wb = Workbook()
            ws = wb.active
            ws.title = "Sales Report"

            headers = ["Bill No", "Customer Name", "Item", "Quantity", "Rate", "Discount", "Total", "Date", "Payment"]
            ws.append(headers)

            for sale in sales:
                items = SaleItem.objects.filter(sales=sale)
                for item in items:
                    row = [
                        sale.bill_number,
                        sale.customer_name,
                        item.item.name,
                        item.quantity,
                        item.rate,
                        f"{item.item.price} → {item.rate}",
                        item.total_price,
                        str(sale.date),
                        sale.payment_mode
                    ]
                    ws.append(row)

            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
            return response

        else:
            messages.error(request, "❌ Invalid export type.")
            return redirect('sales_list')

    return redirect('sales_list')


import csv
from django.http import HttpResponse
from .models import Category  # or Item, Sale, etc.

def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categories.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Status'])

    for category in Category.objects.all():
        writer.writerow([category.name, category.description, category.get_status_display()])

    return response

# ==================== User Rights ====================
from project.forms import UserRightsForm

def update_user_rights(request, user_id):
    current_user = UserProfile.objects.get(id=request.session.get('user_id'))
    if not current_user.is_admin:
        messages.error(request, "❌ Access denied.")
        return redirect('home_view')

    target_user = get_object_or_404(UserProfile, id=user_id)
    form = UserRightsForm(request.POST or None, instance=target_user)

    if request.method == 'POST' and form.is_valid():
        user_profile = form.save(commit=False)
        user_profile.is_customized_by_admin = True
        user_profile.save()
        messages.success(request, "✅ Permissions updated successfully!")
        return redirect('user_list')

    return render(request, 'user_rights_form.html', {
        'form': form,
        'user': target_user
    })








# ==================== LOGOUT ====================
def logout_view(request):
    request.session.flush()
    messages.info(request, "ℹ️ You have been logged out.")
    return redirect('login_view')
