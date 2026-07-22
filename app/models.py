from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime, UTC


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    customers = db.relationship(
        "Customer",
        backref="owner",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    
    customer_code = db.Column(
    db.String(20),
    nullable=True
    )
    
    is_archived = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(20))

    email = db.Column(db.String(120))

    company = db.Column(db.String(100))

    address = db.Column(db.String(200))

    notes = db.Column(db.Text)
    
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

    def __repr__(self):
        return f"<Customer {self.name}>"


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
    
    completed = db.Column(
    db.Boolean,
    default=False
)

    completed_at = db.Column(
    db.DateTime,
    nullable=True
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