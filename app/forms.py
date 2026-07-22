from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    DateField,
    SelectField
    )
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm): 
    

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    remember = BooleanField("Remember Me")
    
    submit = SubmitField("Login")


class CustomerForm(FlaskForm):

    name = StringField(
        "Customer Name",
        validators=[DataRequired()]
    )

    phone = StringField("Phone")

    email = StringField(
        "Email",
        validators=[Email()]
    )

    company = StringField("Company")

    address = StringField("Address")

    notes = TextAreaField("Notes")

    submit = SubmitField("Save Customer")
    
class SearchForm(FlaskForm):

    search = StringField("Search")

    submit = SubmitField("Search")
    
class ProfileForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "New Password"
    )

    confirm = PasswordField(
        "Confirm New Password",
        validators=[
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Update Profile")    

class TaskForm(FlaskForm):

    title = StringField(
        "Task",
        validators=[DataRequired(), Length(max=200)]
    )
    
    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d"
    )
    
    priority = SelectField(
    "Priority",
    choices=[
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low")
    ],
    default="Medium"
    )


    submit = SubmitField("Save Task")
        