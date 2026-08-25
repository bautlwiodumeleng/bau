from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime, UTC
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    organisation_name = db.Column(
        db.String(150),
        nullable=True
    )

    business_phone = db.Column(
        db.String(30),
        nullable=True
    )

    business_email = db.Column(
        db.String(120),
        nullable=True
    )

    business_address = db.Column(
        db.String(250),
        nullable=True
    )

    website = db.Column(
        db.String(150),
        nullable=True
    )

    organisation_logo = db.Column(
        db.String(255),
        nullable=True
    )

    customers = db.relationship(
        "Customer",
        backref="owner",
        lazy=True
    )

    reset_token = db.Column(
        db.String(100),
        nullable=True
    )

    reset_token_expiry = db.Column(
        db.DateTime,
        nullable=True
    )

    def get_reset_token(self):
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        return serializer.dumps(
            self.email,
            salt="password-reset"
        )

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        try:
            email = serializer.loads(
                token,
                salt="password-reset",
                max_age=expires_sec
            )
        except Exception:
            return None

        return User.query.filter_by(
            email=email
        ).first()

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    is_archived = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(120)
    )

    organisation_name = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.String(200)
    )

    notes = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    tasks = db.relationship(
        "Task",
        backref="customer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    documents = db.relationship(
        "CustomerDocument",
        backref="customer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Customer {self.name}>"

class CustomerDocument(db.Model):
    __tablename__ = "customer_documents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    stored_filename = db.Column(
        db.String(255),
        nullable=False
    )

    cloudinary_public_id = db.Column(
        db.String(500),
        nullable=True
    )

    cloudinary_resource_type = db.Column(
        db.String(50),
        nullable=True
    )

    file_type = db.Column(
        db.String(100),
        nullable=True
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    def __repr__(self):
        return f"<CustomerDocument {self.filename}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )

    priority = db.Column(
        db.String(10),
        default="Medium",
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Task {self.title}>"

