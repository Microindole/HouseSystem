import wtforms
from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import LoginModel
from wtforms import Form, StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length

# class LoginForm(wtforms.Form):
#     username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误')])
#     password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误')])
class LoginForm(Form):
    username = StringField('用户名', validators=[
        DataRequired(message="用户名不能为空"),
        Length(min=3, max=20, message="用户名长度必须在3到20个字符之间")
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不能为空"),
        Length(min=6, max=20, message="密码长度必须在6到20个字符之间")
    ])

class RegisterForm(Form):
    username = StringField('用户名', validators=[
        DataRequired(message="用户名不能为空"),
        Length(min=3, max=20, message="用户名长度必须在3到20个字符之间"),
        Regexp(r'^[a-zA-Z0-9_]+$', message="用户名只能包含字母、数字和下划线")
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不能为空"),
        Length(min=6, max=20, message="密码长度必须在6到20个字符之间"),
        EqualTo('confirm_password', message="两次输入的密码不一致")
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message="请确认密码")
    ])
    phone = StringField('联系方式', validators=[
        DataRequired(message="联系方式不能为空"),
        Regexp(r'^\d{10,15}$', message="联系方式必须是10到15位数字")
    ])
    address = StringField('地址', validators=[
        DataRequired(message="地址不能为空"),
        Length(min=5, max=200, message="地址长度必须在5到200个字符之间")
    ])
    user_type = SelectField('角色选择', choices=[
        ('1', '租客'), ('2', '房东'), ('0', '管理员')
    ], validators=[DataRequired(message="请选择角色")])

