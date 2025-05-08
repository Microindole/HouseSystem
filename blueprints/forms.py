import wtforms
from wtforms import Form, StringField, PasswordField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired, ValidationError # Keep DataRequired for basic check, ValidationError for custom server checks
from models import LoginModel

class LoginForm(Form): # Keep as is or simplify if login also moves to JS validation
    username = StringField('用户名', validators=[DataRequired(message="用户名不能为空")])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空")])
    submit = SubmitField('登录')

class RegisterForm(Form):
    # Fields are defined to easily grab them in the backend, but most validators are removed
    username = StringField('用户名')
    password = PasswordField('密码')
    confirm_password = PasswordField('确认密码')
    email = StringField('邮箱')
    phone = StringField('联系方式')
    address = HiddenField('完整地址')
    user_type = SelectField('用户类型', choices=[('1', '租客'), ('2', '房东')])
    def validate_username_on_server(self, username_value): # Renamed to avoid conflict if WTForms auto-calls
        if LoginModel.query.filter_by(username=username_value).first():
            return '用户名已存在，请换一个。'
        return None


