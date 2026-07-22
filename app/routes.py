from flask import Blueprint, render_template, redirect, url_for, flash,request, Response, abort
import csv
from io import StringIO

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from openpyxl import Workbook

from .forms import RegisterForm, LoginForm, CustomerForm, SearchForm, ProfileForm, TaskForm
from .models import User, Customer, Task
from . import db
from flask import abort
from datetime import datetime, UTC, date, timedelta

from openpyxl.styles import PatternFill
main = Blueprint("main", __name__)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from openpyxl.utils import get_column_letter
from io import BytesIO
from openpyxl.styles import Border, Side

@main.route("/")
def home():
    return render_template("home.html")


@main.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("main.register"))
        existing_email = User.query.filter_by(email=form.email.data).first()

        if existing_email:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("main.register"))    

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")

        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            flash("Logged in successfully!", "success")

            return redirect(url_for("main.home"))

        flash("Invalid username or password. Please try again.", "danger")

    return render_template("login.html", form=form)

@main.route("/dashboard")
@login_required
def dashboard():

    total_customers = Customer.query.filter_by(
        created_by=current_user.id
    ).count()

    total_companies = db.session.query(Customer.company)\
        .filter(
            Customer.created_by == current_user.id,
            Customer.company != "",
            Customer.company != None
        )\
        .distinct()\
        .count()

    total_tasks = Task.query.join(Customer).filter(
        Customer.created_by == current_user.id
    ).count()
    
    now = datetime.now(UTC)

    new_this_month = Customer.query.filter(
        Customer.created_by == current_user.id,
        Customer.created_at >= datetime(now.year, now.month, 1, tzinfo=UTC)
    ).count()

    recent_customers = Customer.query.filter_by(
        created_by=current_user.id
    ).order_by(Customer.id.desc()).limit(5).all()
    
    today = date.today()

    upcoming_tasks = (
        Task.query
        .join(Customer)
        .filter(
            Customer.created_by == current_user.id,
            Task.completed == False,
            Task.due_date != None,
            Task.due_date >= today
        )
        .order_by(Task.due_date)
        .limit(5)
        .all()
        )
    
    overdue_tasks = (
    Task.query
    .join(Customer)
    .filter(
        Customer.created_by == current_user.id,
        Task.completed == False,
        Task.due_date != None,
        Task.due_date < today
    )
    .order_by(Task.due_date)
    .all()
    )
    
    print("Total tasks =", total_tasks)

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_companies=total_companies,
        total_tasks=total_tasks,
        new_this_month=new_this_month,
        recent_customers=recent_customers,
        upcoming_tasks=upcoming_tasks,
        overdue_tasks=overdue_tasks
        )

@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.home"))

@main.route("/add_customer", methods=["GET", "POST"])
@login_required
def add_customer():

    form = CustomerForm()

    if form.validate_on_submit():

        existing_customer = Customer.query.filter(
            db.func.lower(Customer.name) == form.name.data.lower(),
            Customer.created_by == current_user.id
        ).first()

        if existing_customer:
            flash("Customer already exists.", "danger")
            return redirect(url_for("main.add_customer"))

        customer = Customer(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            company=form.company.data,
            address=form.address.data,
            notes=form.notes.data,
            created_by=current_user.id
        )

        db.session.add(customer)
        db.session.commit()

        # Generate Customer Code
        customer.customer_code = f"CUST-{customer.id:06d}"
        db.session.commit()

        flash("Customer added successfully!", "success")

        return redirect(url_for("main.customers"))

    return render_template(
        "add_customer.html",
        form=form
    )

# ⬇️ PUT THE NEW ROUTE HERE

@main.route("/add_task/<int:customer_id>", methods=["GET", "POST"])
@login_required
def add_task(customer_id):

    customer = Customer.query.filter_by(
        id=customer_id,
        created_by=current_user.id
    ).first_or_404()

    form = TaskForm()

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            customer_id=customer.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully!", "success")

        return redirect(
            url_for(
                "main.customer_details",
                customer_id=customer.id
            )
        )

    return render_template(
        "add_task.html",
        form=form,
        customer=customer
    )

    return render_template(
        "add_task.html",
        form=form,
        customer=customer
    )

@main.route("/complete_task/<int:task_id>")
@login_required
def complete_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.customer.created_by != current_user.id:
        abort(403)

    task.completed = True
    task.completed_at = datetime.now(UTC)

    db.session.commit()

    flash("Task completed!", "success")

    return redirect(
        url_for(
            "main.customer_details",
            customer_id=task.customer_id
        )
    )

    return render_template(
        "add_task.html",
        form=form,
        customer=customer
    )

@main.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.customer.created_by != current_user.id:
        abort(403)

    form = TaskForm(obj=task)

    if form.validate_on_submit():

        task.title = form.title.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data

        db.session.commit()

        flash("Task updated successfully!", "success")

        return redirect(
            url_for(
                "main.customer_details",
                customer_id=task.customer_id
            )
        )

    return render_template(
        "edit_task.html",
        form=form,
        task=task
    )
    
@main.route("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.customer.created_by != current_user.id:
        abort(403)

    customer_id = task.customer_id

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")

    return redirect(
        url_for(
            "main.customer_details",
            customer_id=customer_id
        )
    )

# ⬇️ THEN YOUR NEXT ROUTE CONTINUES

@main.route("/customers")
@login_required
def customers():

    search = request.args.get("search", "")

    query = Customer.query.filter_by(
        created_by=current_user.id,
        is_archived=False
    )

    if search:

        query = query.filter(
            (Customer.name.ilike(f"%{search}%")) |
            (Customer.phone.ilike(f"%{search}%")) |
            (Customer.email.ilike(f"%{search}%")) |
            (Customer.company.ilike(f"%{search}%"))
        )

    customer_list = query.all()

    return render_template(
        "customers.html",
        customers=customer_list
    )
    
@main.route("/edit_customer/<int:customer_id>", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):

    customer = Customer.query.get_or_404(customer_id)

    form = CustomerForm(obj=customer)

    if form.validate_on_submit():

        customer.name = form.name.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        customer.company = form.company.data
        customer.address = form.address.data
        customer.notes = form.notes.data

        db.session.commit()

        flash("Customer updated successfully!", "success")

        return redirect(url_for("main.customers"))

    return render_template(
        "edit_customer.html",
        form=form
    )
    
@main.route("/live_search")
@login_required
def live_search():

    query = request.args.get("q", "")

    customers = Customer.query.filter(
        Customer.created_by == current_user.id,
        Customer.name.ilike(f"%{query}%")
    ).all()

    return jsonify([
        {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "company": customer.company,
            "address": customer.address
        }
        for customer in customers
    ])

@main.route("/export/csv")
@login_required
def export_csv():

    customers = Customer.query.filter_by(
        created_by=current_user.id,
        is_archived=False
    ).all()

    output = StringIO()
    writer = csv.writer(output)

    # Column headers
    writer.writerow([
        "Customer ID",
        "Name",
        "Phone",
        "Email",
        "Company",
        "Address",
        "Notes"
    ])

    # Customer data
    for customer in customers:
        writer.writerow([
            customer.customer_code,
            customer.name,
            customer.phone,
            customer.email,
            customer.company,
            customer.address,
            customer.notes
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=customers.csv"
        }
    )
    
    
@main.route("/export/xlsx")
@login_required
def export_xlsx():

    customers = Customer.query.filter_by(
        created_by=current_user.id,
        is_archived=False
    ).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Customers"

    # Header row
    headers = [
        "Customer ID",
        "Name",
        "Phone",
        "Email",
        "Company",
        "Address",
        "Notes"
    ]

    ws.append(headers)

    # Header formatting
    header_fill = PatternFill(
        fill_type="solid",
        start_color="1F4E78",
        end_color="1F4E78"
    )

    for cell in ws[1]:
        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )
        cell.fill = header_fill

    # Customer data
    for customer in customers:
        ws.append([
            customer.customer_code,
            customer.name,
            customer.phone,
            customer.email,
            customer.company,
            customer.address,
            customer.notes
        ])

    # Auto-size columns
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)

        for cell in column:
            if cell.value:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        ws.column_dimensions[column_letter].width = max_length + 3

        # Freeze the header row
        # Freeze the header row
    ws.freeze_panes = "A2"

    # Thin borders for all cells
    thin = Side(
        border_style="thin",
        color="000000"
    )

    for row in ws.iter_rows():
        for cell in row:
            cell.border = Border(
                left=thin,
                right=thin,
                top=thin,
                bottom=thin
            )

    # Save workbook to memory
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Return Excel file
    return Response(
        output.getvalue(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=customers.xlsx"
        }
    ) 
        
@main.route("/customer/<int:customer_id>")
@login_required
def customer_details(customer_id):


    customer = Customer.query.filter_by(
        id=customer_id,
        created_by=current_user.id
    ).first_or_404()

    return render_template(
        "customer_details.html",
        customer=customer
    )    

@main.route("/archive_customer/<int:customer_id>")
@login_required
def archive_customer(customer_id):

    customer = Customer.query.filter_by(
        id=customer_id,
        created_by=current_user.id
    ).first_or_404()

    customer.is_archived = True
    db.session.commit()

    flash("Customer archived successfully!", "success")

    return redirect(url_for("main.customers"))


@main.route("/archived_customers")
@login_required
def archived_customers():

    customers = Customer.query.filter_by(
        created_by=current_user.id,
        is_archived=True
    ).all()

    return render_template(
        "archived_customers.html",
        customers=customers
    )


@main.route("/restore_customer/<int:customer_id>")
@login_required
def restore_customer(customer_id):

    customer = Customer.query.filter_by(
        id=customer_id,
        created_by=current_user.id,
        is_archived=True
    ).first_or_404()

    customer.is_archived = False
    db.session.commit()

    flash("Customer restored successfully!", "success")

    return redirect(url_for("main.archived_customers"))


@main.route("/delete_customer/<int:customer_id>")
@login_required
def delete_customer(customer_id):

    customer = Customer.query.filter_by(
        id=customer_id,
        created_by=current_user.id,
        is_archived=True
    ).first_or_404()

    db.session.delete(customer)
    db.session.commit()

    flash("Customer permanently deleted.", "success")

    return redirect(url_for("main.archived_customers"))


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.password = generate_password_hash(
                form.password.data
            )

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("main.profile"))

    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template(
        "profile.html",
        form=form
    )
    