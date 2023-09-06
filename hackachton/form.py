from wtforms import Form, StringField, SelectField, validators, EmailField,TelField, DateField,FileField,IntegerField,TextAreaField
import wtforms.fields as fld

class CreateContactForm(Form):
    first_name = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    last_name = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    email = StringField('', [validators.Length(min=6, max=35), validators.DataRequired()])
    phone_number = IntegerField('', [validators.NumberRange(min=60000000,max=99999999), validators.DataRequired()])
    subject = SelectField('', [validators.DataRequired()],choices=[('', 'Select'), ('Order Status Enquiry', 'Order Status Enquiry'), ('Product Exchange and Returns', 'Product Exchange and Returns'), ('Others', 'Others')], default='')
    questions = TextAreaField('', [validators.Length(min=1,max=1500), validators.DataRequired()])


class CreateMemberForm(Form):
    first_name = StringField("First Name",[validators.Length(min=1,max=30),validators.data_required()])
    last_name = StringField("Last Name", [validators.Length(min=1, max=30), validators.data_required()])
    email = EmailField("Email",[validators.data_required()])
    new_password = fld.PasswordField('password')
    confirm_password = fld.PasswordField(validators=[validators.EqualTo("new_password")])
    dob = DateField('Date of Birth',format='%Y-%m-%d')
    gender = SelectField('Gender', [validators.DataRequired()],choices=[('','Select'),('F','Female'),('M','Male')],default='')
    phonenumber = TelField("Phone Number",[validators.Length(min=8,max=8), validators.data_required()])
    image = FileField("Avatar")


#

class getphone_number(Form):
    phonenumber = TelField("Phone Number", [validators.Length(min=8, max=8), validators.data_required()])
    otp = TelField("Phone Number", [validators.Length(min=6, max=6), validators.data_required()])


class getemail(Form):
    email = EmailField("Email",[validators.data_required()])

class resetpassword(Form):
    new_password = fld.PasswordField('password')
    confirm_password = fld.PasswordField(validators=[validators.EqualTo("new_password")])




