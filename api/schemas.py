from wtforms import Form, StringField, PasswordField, EmailField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email(message='Invalid email address')])
    password = PasswordField('New Password', [validators.DataRequired()])
