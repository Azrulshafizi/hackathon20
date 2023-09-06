from flask import Flask, render_template, request, redirect, url_for,session, flash
from form import CreateMemberForm, getphone_number,resetpassword,CreateContactForm, getemail
from login import loginpage
import shelve
from address import addressform,Updateprofileforstaff,paymentform
from members import member, Address,Payment,Product
from staff_login import Staff_Login
import staff,Customer


from twilio.rest import Client

import os



# from check import member_login



app = Flask(__name__)
app.secret_key = "any-string-12345"
memberlogin = None
StaffLogin = None



account_sid = 'ACf9b4b88a7f93c743ee05e26ea74363ad'
auth_token = 'a9169f73d55799bd2771cc7e3cb3d321'
client = Client(account_sid, auth_token)

import random
import string

def generate_otp(length=6):
    # Generate a random sequence of digits
    otp = ''.join(random.choices(string.digits, k=length))
    return otp

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone_number = request.form.get('phone_number')
    otp = generate_otp()
    recipient_phone_number = request.form.get('phonenumber')

    message = client.messages.create(
        from_='+14782497143',
        body=f'hi, your OTP is {otp}',
        to='+6582054349'
    )

    return otp
# pwlewkkjjwpmonln
#CFD02BF436E630DC4794E32AD3CC7DBC25EB
# app.config['MAIL_SERVER'] = 'smtp.elasticemail.com'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = 'azrulshafizi25@gmail.com'
# app.config['MAIL_SENDER'] = 'azrulshafizi25@gmail.com'
# app.config['MAIL_PASSWORD'] = 'CFD02BF436E630DC4794E32AD3CC7DBC25EB'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# mail = Mail(app)



@app.route('/', methods=['GET','POST'])
def home():

    # member_dict = {}
    # db = shelve.open('storage.db', 'r')
    # member_dict = db['member']
    # db.close()
    # member_list = []
    # for key in member_dict:
    #     member = member_dict.get(key)
    #     member_list.append(member)

    return render_template("home.html",member=memberlogin)
#



@app.route('/Azrul/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    getphonenumber = getphone_number(request.form)
    getemails = getemail(request.form)
    reset = resetpassword(request.form)
    if request.method == 'POST':
        action = request.form.get('action')
        get_email = request.form.get('email')
        phone_number = request.form.get('phonenumber')
        g = request.args.get('phone')

        print(g)
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        db.close()
        member_list = []

        for key in member_dict:
            member = member_dict.get(key)
            member_list.append(member)
        for member in member_list:
            if member.get_gender() == getemail:
                return render_template('azrul/reset.html')
            else:
                flash('incorrect','error')



        for member in member_list:
            if phone_number == member.get_phone_number():
                # otp = send_otp()
                return redirect(url_for('reset',id=member.get_user_id()))

            if get_email == member.get_email():
                return redirect(url_for('reset',id=member.get_user_id()))
    return render_template('Azrul/forgotpassword.html',form=getphonenumber,email=getemails)





@app.route('/Azrul/reset/<int:id>/', methods=['GET','POST'])
def reset(id):
    reset = resetpassword(request.form)


    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()

    if request.method == 'POST':
        member_dict = {}
        db = shelve.open('storage.db', 'w')
        member_dict = db['member']
        member = member_dict.get(id)
        member.set_password(reset.confirm_password.data)
        db['member'] = member_dict
        db.close()
        print('hell')
        return render_template('Azrul/send.html')
    else:
        return render_template('Azrul/reset.html',member=member_dict.get(id),reset=reset)


@app.route('/Azrul/send',methods=['GET','POST'])
def send():
    return render_template('Azrul/send.html')

@app.route('/Azrul/login', methods=['GET','POST'])
def login():
    form = loginpage(request.form)
    if request.method == "POST" and form.validate():
        phonenumber = request.form["phonenumber"]
        password = request.form["password"]
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        db.close()
        member_list = []
        for key in member_dict:
            member = member_dict.get(key)
            member_list.append(member)
        for member in member_list:
            if member.get_phone_number() == phonenumber:
                if member.get_password() == password:
                    memberlogin = member
                    return render_template('home.html', member=memberlogin)
                else:
                    flash('Password incorrect!', 'error')
                    return render_template('Azrul/login.html', login=form)
            else:
                flash('Phone number not register!', 'error')
    return render_template('Azrul/login.html',login=form)



# @app.route('/successful', methods=['GET','POST'])
# def successful():
#
#     member_dict = {}
#     db = shelve.open('storage.db', 'r')
#     member_dict = db['member']
#     db.close()
#     member_list = []
#     for key in member_dict:
#         member = member_dict.get(key)
#         member_list.append(member)
#
#     return render_template('azrul/successful.html',member = memberlogin)



@app.route('/Azrul/profile/<int:id>/', methods=['GET','POST'])
def profile(id):

    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()
    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)

    member = member_dict.get(id)
    if member.get_user_id() == id:
        memberlogin = member
        return render_template('Azrul/profile.html', member_list=member_list, member_id=id, member=memberlogin)
    else:
        return render_template('Azrul/login.html')

@app.route('/Azrul/logout', methods=['GET'])
def logout():
    memberlogin = None
    return redirect(url_for('home',member=memberlogin))

@app.route('/Azrul/CreateMember', methods=['GET','POST'])
def create_member():
    create_member_form = CreateMemberForm(request.form)

    if request.method == 'POST' and create_member_form.validate():
        member_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            member_dict = db['member']
        except:
            print("Error in retrieving Users from storage.db.")

        # eList = []
        # iList = []
        # for key in member_dict:
        #     email = member_dict.get(key)
        #     eList.append(key)
        #     for i in member_dict:
        #         nid = member_dict[i].get_user_id()
        #         iList.append(nid)
        #         if str(email) == str(member_dict[i].get_email()):
        #              global typo
        #              typo = "Email already in use"
        #              return render_template('CreateMember.html', typo=typo, form=create_user_form)
        #         break
        print(create_member_form.first_name.data)
        addressObject = Address("","","","","")
        paymentobject = Payment("", "", "")
        historyobject = Product()

        members = member(create_member_form.first_name.data,
                         create_member_form.last_name.data, create_member_form.email.data,
                         create_member_form.new_password.data,
                         create_member_form.dob.data, create_member_form.phonenumber.data,
                         create_member_form.gender.data,
                         create_member_form.image.data, addressObject, paymentobject,historyobject)
        member_dict[members.get_user_id()] = members
        db['member'] = member_dict
        # Test codes
        member_dict = db['member']
        members = member_dict[members.get_user_id()]
        print(members.get_first_name(), members.get_last_name(), "was stored in storage.db successfully with user_id == ", members.get_user_id())
        db.close()
        return redirect(url_for('login'))
    return render_template('Azrul/CreateMember.html', form=create_member_form)


@app.route('/Azrul/UpdateMemberProfile/<int:id>/', methods=['GET','POST'])
def UpdateMemberProfile(id):
    global memberlogin
    UpdateMember = CreateMemberForm(request.form)
    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()
    if request.method == 'POST' and UpdateMember.validate():
        member_dict = {}
        db = shelve.open('storage.db', 'w')
        member_dict = db['member']
        member = member_dict.get(id)
        member.set_first_name(UpdateMember.first_name.data)
        member.set_last_name(UpdateMember.last_name.data)
        member.set_phone_number(UpdateMember.phonenumber.data)
        member.set_password(member.get_password())
        member.set_email(UpdateMember.email.data)
        member.set_date_of_birth(member.get_date_of_birth())
        member.set_gender(UpdateMember.gender.data)
        member.set_image(UpdateMember.image.data)
        db['member'] = member_dict
        db.close()
        print('successful')
        return render_template('Azrul/Profile.html',member=member)
    else:
        member = member_dict.get(id)
        UpdateMember.first_name.data = member.get_first_name()
        UpdateMember.last_name.data = member.get_last_name()
        UpdateMember.phonenumber.data = member.get_phone_number()
        UpdateMember.confirm_password.data = member.get_password()
        UpdateMember.dob.data = member.get_date_of_birth()
        UpdateMember.email.data = member.get_email()
        UpdateMember.gender.data = member.get_gender()
        UpdateMember.image.data = member.get_image()
        memberlogin = member
        return render_template('Azrul/UpdateMemberProfile.html',form=UpdateMember, member_id=id, member= memberlogin)



@app.route('/Azrul/UpdateAddress/<int:id>/', methods=['GET','POST'])
def Update_Address(id):
    address = addressform(request.form)

    if request.method == 'POST' and address.validate():
        member_dict = {}
        db = shelve.open('storage.db', 'w')
        member_dict = db['member']
        member = member_dict.get(id)
        member.address.set_country(address.country.data)
        member.address.set_company(address.company.data)
        member.address.set_address(address.address.data)
        member.address.set_house(address.house.data)
        member.address.set_postal_code(address.postal_code.data)
        db['member'] = member_dict
        db.close()
        print('success')
        return render_template('Azrul/Profile.html',member=member)
    else:
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        db.close()
        member = member_dict.get(id)

        address.country.data = member.address.get_country()
        address.address.data = member.address.get_address()
        address.postal_code.data = member.address.get_postal_code()
        address.company.data = member.address.get_company()
        address.house.data = member.address.get_house()
        memberlogin = member
        return render_template('Azrul/UpdateAddress.html',forms=address,member=memberlogin,member_id=id)


@app.route('/Azrul/UpdatePayment/<int:id>/', methods=['GET','POST'])
def Update_Payment(id):
    Payment_form = paymentform(request.form)

    if request.method == 'POST' and Payment_form.validate():
        member_dict = {}
        db = shelve.open('storage.db', 'w')
        member_dict = db['member']
        member = member_dict.get(id)
        member.payment.set_card_number(Payment_form.card_number.data)
        member.payment.set_card_name(Payment_form.card_name.data)
        member.payment.set_expiry_date(Payment_form.expiry_date.data)

        db['member'] = member_dict
        db.close()
        print('success')
        return render_template('home.html',member=member)
    else:
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        db.close()
        member = member_dict.get(id)

        Payment_form.card_number.data = member.payment.get_card_number()
        Payment_form.card_name.data = member.payment.get_card_name()
        Payment_form.expiry_date.data = member.payment.get_expiry_date()

        memberlogin = member
        return render_template('Azrul/UpdatePayment.html',forms=Payment_form,member=memberlogin,member_id=id)



@app.route('/Azrul/UpdateMemberforstaff/<int:id>/', methods=['GET','POST'])
def UpdateMemberforstaff(id):
    UpdateProfile = Updateprofileforstaff(request.form)
    if request.method == 'POST' and UpdateProfile.validate():
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        member = member_dict.get(id)
        member.set_first_name(UpdateProfile.first_name.data)
        member.set_last_name(UpdateProfile.last_name.data)
        member.set_phone_number(UpdateProfile.phonenumber.data)
        member.set_email(UpdateProfile.email.data)
        member.set_date_of_birth(member.get_date_of_birth())
        member.set_gender(UpdateProfile.gender.data)
        member.set_password(member.get_password())
        member.set_image(UpdateProfile.image.data)
        member.address.set_country(UpdateProfile.country.data)
        member.address.set_company(UpdateProfile)
        member.address.set_address(UpdateProfile.address.data)
        member.address.set_postal_code(UpdateProfile.postal_code.data)
        member.address.set_address(UpdateProfile.house.data)
        db['member'] = member_dict
        db.close()
        print('success')
        return redirect(url_for('Azrul/retrieveMember'))
    else:
        member_dict = {}
        db = shelve.open('storage.db', 'r')
        member_dict = db['member']
        db.close()
        member = member_dict.get(id)
        UpdateProfile.first_name.data = member.get_first_name()
        UpdateProfile.last_name.data = member.get_last_name()
        UpdateProfile.phonenumber.data = member.get_phone_number()
        UpdateProfile.dob.data = member.get_date_of_birth()
        UpdateProfile.email.data = member.get_email()
        UpdateProfile.gender.data = member.get_gender()
        UpdateProfile.image.data = member.get_image()
        UpdateProfile.country.data = member.address.get_country()
        UpdateProfile.address.data = member.address.get_address()
        UpdateProfile.postal_code.data = member.address.get_postal_code()
        UpdateProfile.company.data = member.address.get_company()
        UpdateProfile.house.data = member.address.get_house()
        StaffLogin = staff
        return render_template('azrul/UpdateMemberforstaff.html',form=UpdateProfile,staff=StaffLogin)

@app.route('/Azrul/deleteUser/<int:id>/', methods=['POST'])
def deleteuser(id):
    member_dict = {}
    db = shelve.open('storage.db', 'w')
    member_dict = db['member']
    member_dict.pop(id)
    db['member'] = member_dict
    db.close()

    return redirect(url_for('retrieveMember'))




@app.route('/Azrul/StaffLogin', methods=['GET','POST'])
def StaffLogin():
    stafflogin = Staff_Login(request.form)
    print(staff.staff['STAFF_ID'])
    print(staff.staff['password'])
    if request.method == 'POST':
        admin_staff = request.form['Admin']
        passwordstaff = request.form['password']
        print(admin_staff)
        print(passwordstaff)

        if admin_staff == staff.staff['STAFF_ID']:
            if passwordstaff == staff.staff['password']:
                StaffLogin = staff
                return render_template('Azrul/admin.html',staff= StaffLogin)
            else:
                return render_template('Azrul/StaffLogin.html', stafflogin=stafflogin)
    return render_template('Azrul/StaffLogin.html',stafflogin=stafflogin)



@app.route('/Azrul/addressform/<int:id>/', methods=['GET','POST'])
def address(id):
    address =addressform(request.form)
    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()
    member_list = []
    if request.method == "POST":
        addressO = Address(
                      address.country.data,address.address.data,address.house.data,address.postal_code.data
        )
        member_dict[id].address = addressO

        # Test codes

        db = shelve.open('storage.db', 'c')
        db['member'] = member_dict
        db.close()
        return redirect(url_for('home'))

    # for member in member_list:
    #     if member.get_user_id == id:
    #         member = member
    return render_template('Azrul/addressform.html',form=address)

@app.route('/Azrul/admin')
def admin():
    return render_template('Azrul/admin.html',staff=staff)

@app.route('/Azrul/retrieveMember')
def retrieveMember():
    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()

    member_list = []
    for key in member_dict:
        members = member_dict.get(key)
        member_list.append(members)
        print(members)
    StaffLogin = staff
    return render_template('Azrul/retrieveMember.html', count=len(member_list), member_list=member_list,staff=StaffLogin)

# @app.route('/viewMember/<int:id>')
# def ViewMember(id):
#     member_dict = {}
#     db = shelve.open('storage.db', 'r')
#     member_dict = db['member']
#     db.close()
#
#     member_list = []
#     for key in member_dict:
#         member = member_dict.get(key)
#         member_list.append(member)
#     return render_template('viewMember.html',member_list=member_list,member_id=id)

@app.route("/Azrul/viewmemberforstaff/<int:id>/",methods=['GET','POST'])
def viewmemberforstaff(id):
    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()

    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)
    return render_template('Azrul/viewmemberforstaff.html', member_list=member_list, member_id=id)




#Transaction code
#shinghak

# Sample product data (two products)
# Sample product data (two products)
product1 = {"name": "Shiftwalk Air Max 90",
            "price": 10.99,
            "colors": "White",
            "sizes": "Medium"
            }

product2 = {"name": "Shiftwalk SB Dunk ",
            "price": 24.99,
            "colors": "Blue",
            "sizes": "Medium"
            }

product3= {"name": "Shiftwalk Air Force 1",
            "price": 32.50,
            "colors": "Blue",
            "sizes": "Medium"
           }

# Initialize the cart data
cart_data = shelve.open("cart_data", writeback=True)
if not cart_data.get("cart"):
    cart_data["cart"] = {}



@app.route("/Shinghak/form", methods=['GET', 'POST'])
def add_to_cart():
    global memberlogin
    product_name = request.form["product_name"]
    quantity = int(request.form["product_quantity"])

    if product_name == product1["name"]:
        cart_data["cart"].setdefault(product_name, 0)
        cart_data["cart"][product_name] += quantity
        cart_data.sync()  # Save the cart data to the Shelve database
    return redirect(url_for('catalogue'))


@app.route("/Shinghak/form1", methods=['GET', 'POST'])
def add_to_cart1():
    product_name = request.form["product_name"]
    quantity = int(request.form["product_quantity"])

    if product_name == product2["name"]:
        cart_data["cart"].setdefault(product_name, 0)
        cart_data["cart"][product_name] += quantity
        cart_data.sync()  # Save the cart data to the Shelve database
    return redirect(url_for('catalogue',member=memberlogin))

@app.route("/Shinghak/form2", methods=['GET', 'POST'])
def add_to_cart2():
    global memberlogin
    product_name = request.form["product_name"]
    quantity = int(request.form["product_quantity"])

    if product_name == product3["name"]:
        cart_data["cart"].setdefault(product_name, 0)
        cart_data["cart"][product_name] += quantity
        cart_data.sync()  # Save the cart data to the Shelve database
    return redirect(url_for('catalogue',member=memberlogin))


@app.route('/Shinghak/Product',methods=['GET','POST'])
def Product():
    global memberlogin
    cart_items = {}
    total_amount = 0.0
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3
        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
    return render_template('Shinghak/Product.html', product1=product1, cart_items=cart_items, total_amount=total_amount,member=memberlogin)

@app.route('/Shinghak/Product2', methods=['GET', 'POST'])
def Product2():
    global memberlogin
    cart_items = {}
    total_amount = 0.0
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
    return render_template('Shinghak/Product2.html', product2=product2, cart_items=cart_items, total_amount=total_amount,member=memberlogin)



@app.route('/Shinghak/Product3', methods=['GET', 'POST'])
def Product3():
    global memberlogin
    cart_items = {}
    total_amount = 0.0
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
    return render_template('Shinghak/Product3.html', product3=product3, cart_items=cart_items, total_amount=total_amount,member=memberlogin)

@app.route('/Shinghak/Catalogue',methods=['GET', 'POST'])
def catalogue():

    cart_items = {}
    total_amount = 0.0
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
    return render_template('Shinghak/Catalogue.html', cart_items=cart_items, total_amount=total_amount, member=memberlogin)

@app.route('/Shinghak/Catalogues/<int:id>',methods=['GET', 'POST'])
def catalogues(id):
    global memberlogin
    print(memberlogin)
    cart_items = {}
    total_amount = 0.0
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }
    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()
    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)
    for member in member_list:
        if member.get_user_id() == id:
            memberlogin = member
            break
    return render_template('Shinghak/Catalogue.html', cart_items=cart_items, total_amount=total_amount, member=memberlogin)

@app.route("/Shinghak/cart")
def cart():
    cart_items = {}
    total_amount = 0.0
    address = addressform(request.form)
    payment = paymentform(request.form)
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal,
            }

    return render_template("Shinghak/CArt.html", cart_items=cart_items, total_amount=total_amount, member=memberlogin,form= address, form1=payment)


@app.route("/Shinghak/cart/<int:id>", methods=['GET','POST'])
def carts(id):
    cart_items = {}
    total_amount = 0.0
    address = addressform(request.form)
    payment = paymentform(request.form)
    # name =  request.form.get("product_name")
    # price

    member_dict = {}
    db = shelve.open('storage.db', 'r')
    member_dict = db['member']
    db.close()
    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)
    memberlogin = None
    for member in member_list:
        if member.get_user_id() == id:
            memberlogin = member
            break
    for product_name, quantity in cart_data["cart"].items():
        product = None
        if product_name == product1["name"]:
            product = product1
        elif product_name == product2["name"]:
            product = product2
        elif product_name == product3["name"]:
            product = product3

        if product is not None:
            subtotal = product["price"] * quantity
            total_amount += subtotal
            cart_items[product_name] = {
                "name": product["name"],
                "price": product["price"],
                "sizes": product["sizes"],
                "colors": product["colors"],
                "quantity": quantity,
                "subtotal": subtotal,
            }



    if request.method == "POST":
        id = request.form.get('id')

        # for member in member_list:
        #     if member.get_user_id() == id:
        address = Address(
                      address.country.data,address.address.data,address.house.data,address.postal_code.data
        )

        payment = Payment( payment.card_number.data, payment.card_name.data, payment.expiry_date.data)

        member_dict[id].address = address
        member_dict[id].payment = payment
       #member_dict[member.get_user_id()] = members

        # Test codes

        db = shelve.open('storage.db', 'c')
        db['member'] = member_dict
        db.close()


        return redirect(url_for('home', member=memberlogin))




    return render_template("home.html", cart_items=cart_items, total_amount=total_amount,member=memberlogin, form= address, form1=payment)

@app.route('/Shinghak/address2')
def add():
    return render_template('shinghak/addressform.html')

@app.route('/Shinghak/delete_from_cart', methods=['POST'])
def delete_from_cart():
    global memberlogin
    product_name = request.form["product_name"]
    print(f"Product Name to Delete: {product_name}")

    if product_name in cart_data["cart"]:
        del cart_data["cart"][product_name]
        cart_data.sync()  # Save the updated cart data to the Shelve database

    return redirect(url_for('catalogue', member=memberlogin))

# @app.route('/Shinghak/addressform/<int:id>/', methods=['GET','POST'])
# def address(id):
#     address =addressform(request.form)
#     payment= paymentform(request.form)
#     member_dict = {}
#     db = shelve.open('storage.db', 'r')
#     member_dict = db['member']
#     db.close()
#     member_list = []
#     for key in member_dict:
#         member = member_dict.get(key)
#         member_list.append(member)
#     member_check = None
#     for member in member_list:
#         if member.get_user_id() ==id:
#             member_check = member
#             break
#
#
#     if request.method == "POST":
#
#         # for member in member_list:
#         #     if member.get_user_id() == id:
#         address = Address(
#                       address.country.data,address.address.data,address.house.data,address.postal_code.data
#         )
#
#         payment = Payment( payment.card_number.data, payment.card_name.data, payment.expiry_date.data)
#
#         member_dict[id].address = address
#         member_dict[id].payment = payment
#        #member_dict[member.get_user_id()] = members
#
#         # Test codes
#
#         db = shelve.open('storage.db', 'c')
#         db['member'] = member_dict
#         db.close()
#
#         cart_data["cart"] = {}
#         cart_data.sync()  # Save the empty cart data to the Shelve database
#
#         return redirect(url_for('home',member=memberlogin))
#
#     # for member in member_list:
#     #     if member.get_user_id == id:
#     #         member = member
#     return render_template('home.html',form=address, member=memberlogin, form1=payment)







def save_deduction_data(data):
    with shelve.open('deductions.db') as shelf:
        shelf['deduction'] = data

# Function to load deduction data using shelve
def load_deduction_data():
    with shelve.open('deductions.db') as shelf:
        return shelf.get('deduction', 0)

# Function to save inventory data using shelve
def save_inventory_data(data):
    with shelve.open('inventory.db') as shelf:
        shelf['stock'] = data


# Function to load inventory data using shelve
def load_inventory_data():
    with shelve.open('inventory.db') as shelf:
        return shelf.get('stock', [])


@app.route('/Shinghak/Inventory')
def inventory():
    stock = load_inventory_data()

    return render_template('Shinghak/Inventory.html', stock=stock)


product_stock = [
        {'name': 'Nike Air Max 90', 'price': 25.99, 'Quantity': 10},
        {'name': 'Adidas Ultraboost', 'price': 19.99, 'Quantity': 30},
        {'name': 'Puma Cali ', 'price': 32.50, 'Quantity': 40},
        # Add more products here
    ]



    # Save the product stock to shelve
save_inventory_data(product_stock)


@app.route('/Shinghak/update_quantity', methods=['POST'])
def update_quantity():
    new_quantities = {}
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            index = int(key.split('_')[1])
            new_quantities[index] = int(value)

    stock = load_inventory_data()

    for index, quantity in new_quantities.items():
        stock[index]['Quantity'] = quantity

    save_inventory_data(stock)

    return redirect(url_for('inventory'))

@app.route('/Shinghak/delete_product/<int:index>', methods=['GET'])
def delete_product(index):
    stock = load_inventory_data()

    if 0 <= index < len(stock):
        del stock[index]
        save_inventory_data(stock)

    return redirect(url_for('inventory'))

@app.route('/Shinghak/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = {
            'name': request.form['name'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'Quantity': int(request.form['quantity'])
        }

        stock = load_inventory_data()
        stock.append(new_product)
        save_inventory_data(stock)

        return redirect(url_for('inventory'))

    return render_template('Shinghak/AddProduct.html')





#Customer Support
#ASHER
# Define the chatbot responses here
responses = {
    "hello": "Hi there!",
    "hi": "Hi there!",
    "color": ["The shoe is available in Blue, Red, and Black."],
    "size": ["The shoe is available in sizes 7, 8, and 9. "],
    "what colors does the shoe come in": "All colors",
    "payment available": "Visa, Credit, Debit.",
    "available payment": "Visa, Credit, Debit.",
    "payment do you have": "Visa, Credit, Debit.",
    "customer support": ["Please contact customer support", ["Customer Support"]],
    "update detail": "Click into your Profile to update.",
    "change detail": "Click into your Profile to update.",
    "view detail": "Click into your Profile.",
    "make payment": "After you have selected a product and checked out u can make the following payment.",
    "agent": ["To speak with a service agent, click the button below.", ["Chat with Agent"]],
    "add to cart": "Go to the product page and click on add to cart.",
    "add products to cart": "Select a product and click add to cart",
    "change delivery": "Go to Order Tracking under Profile. Under the tab 'To Ship', click on the edit button to change your address. ",
    "view delivery": "Go into your Order Tracking under Profile.",
    "check my point": "Navigate to the Profile page.",
    "default": "I'm sorry, but I didn't understand that. Can you please rephrase?"
}



def get_response(user_input):
    user_input = user_input.lower()
    for key in responses.keys():
        if key in user_input:
            if isinstance(responses[key], list) and len(responses[key]) == 2:
                return responses[key]
            else:
                return responses[key]
    return responses["default"]




@app.route("/get_response", methods=["POST"])
def get_chat_response():
    user_input = request.form["user_input"]
    response = get_response(user_input)
    return {"response": response}




@app.route('/asher/ContactUs', methods=['GET', 'POST'])
def create_contact():
    create_contact_form = CreateContactForm(request.form)
    if request.method == 'POST' and create_contact_form.validate():
        customers_dict = {}
        db = shelve.open('storage1.db', 'c')
        try:
            customers_dict = db['Customer']
        except:
            print("Error in retrieving Users from storage.db.")
        customer = Customer.Customer(create_contact_form.first_name.data,
                       create_contact_form.last_name.data, create_contact_form.email.data,
                       create_contact_form.phone_number.data, create_contact_form.subject.data,
                       create_contact_form.questions.data)
        customers_dict[customer.get_customer_id()] = customer
        db['Customer'] = customers_dict
        # Test codes
        customers_dict = db['Customer']
        customer = customers_dict[customer.get_customer_id()]
        print(customer.get_first_name(), customer.get_last_name(), "was stored in storage.db successfully with user_id == ", customer.get_customer_id())
        db.close()
        flash('Form submitted successfully!', 'contact_success')
        return redirect(url_for('create_contact'))
    with shelve.open('reviews.db') as db:
        reviews = db.get('reviews', [])

    # Calculate average rating
    total_ratings = len(reviews)
    average_rating = sum(review['rating'] for review in reviews) / total_ratings if total_ratings > 0 else 1

    average_rating = round(average_rating, 1)
    ratings = {i: 0 for i in range(1, 6)}

    for review in reviews:
        ratings[review['rating']] += 1

    return render_template('asher/ContactUs.html', form=create_contact_form, reviews=reviews, average_rating=average_rating, ratings=ratings, total_ratings=total_ratings)


@app.route('/asher/ContactUs_m/<int:id>', methods=['GET', 'POST'])
def create_contacts(id):
    global memberlogin
    create_contact_form = CreateContactForm(request.form)


    if request.method == 'POST' and create_contact_form.validate():
        customers_dict = {}
        db = shelve.open('storage1.db', 'c')
        try:
            customers_dict = db['Customer']
        except:
            print("Error in retrieving Users from storage.db.")
        customer = Customer.Customer(create_contact_form.first_name.data,
                       create_contact_form.last_name.data, create_contact_form.email.data,
                       create_contact_form.phone_number.data, create_contact_form.subject.data,
                       create_contact_form.questions.data)
        customers_dict[customer.get_customer_id()] = customer
        db['Customer'] = customers_dict
        # Test codes
        customers_dict = db['Customer']
        customer = customers_dict[customer.get_customer_id()]
        print(customer.get_first_name(), customer.get_last_name(), "was stored in storage.db successfully with user_id == ", customer.get_customer_id())
        db.close()
        flash('Form submitted successfully!', 'contact_success')

    with shelve.open('reviews.db') as db:
        reviews = db.get('reviews', [])

    # Calculate average rating
    total_ratings = len(reviews)
    average_rating = sum(review['rating'] for review in reviews) / total_ratings if total_ratings > 0 else 1

    average_rating = round(average_rating, 1)
    ratings = {i: 0 for i in range(1, 6)}

    for review in reviews:
        ratings[review['rating']] += 1

    member_dict = {}
    db = shelve.open('storage1.db', 'r')

    member_dict = db['member']
    db.close()
    member_list = []
    for key in member_dict:
        member = member_dict.get(key)
        member_list.append(member)
    for member in member_list:
        if member.get_user_id() == id:
            memberlogin = member
            break



    return render_template('asher/ContactUs.html', form=create_contact_form, reviews=reviews, average_rating=average_rating, ratings=ratings, total_ratings=total_ratings,member=memberlogin)




@app.route('/asher/submit', methods=['POST'])
def submit_review():
    name = request.form['name']
    rating = int(request.form['rating'])
    review = request.form['review']

    with shelve.open('reviews.db') as db:
        reviews = db.get('reviews', [])
        reviews.append({'name': name, 'rating': rating, 'review': review})
        db['reviews'] = reviews
    flash('Review submitted successfully!', 'review_success')
    return redirect('/asher/ContactUs')




@app.route('/asher/review')
def display_reviews():
    try:
        with shelve.open('reviews.db') as db:
            reviews = db.get('reviews', [])

        # Calculate average rating and ratings distribution
        total_ratings = len(reviews)
        average_rating = sum(review['rating'] for review in reviews) / total_ratings if total_ratings > 0 else 1

        average_rating = round(average_rating, 1)
        ratings = {i: 0 for i in range(1, 6)}

        for review in reviews:
            ratings[review['rating']] += 1

        return render_template('asher/review.html', reviews=reviews, average_rating=average_rating, ratings=ratings,
                               total_ratings=total_ratings)

    except Exception as e:
        print(f"Error while retrieving reviews: {e}")
        return render_template('asher/review.html', reviews=[], average_rating=0, ratings={})



@app.route('/asher/retrieveCustomer')
def retrieve_customer():
 customers_dict = {}
 db = shelve.open('storage1.db', 'r')
 customers_dict = db['Customer']
 db.close()

 customers_list = []
 filter_status = request.args.get('status', default='all')

 for key in customers_dict:
  customer = customers_dict.get(key)
  customers_list.append(customer)

 return render_template('asher/retrieveCustomer.html',
                        count=len(customers_list), customers_list=customers_list,filter_status=filter_status)


@app.route('/asher/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    customer_dict = {}
    db = shelve.open('storage1.db', 'w')
    customer_dict = db.get('Customer', {})
    # customer_dict = db['Customer']
    if id in customer_dict:
        customer = customer_dict[id]
        if customer.get_status() == "completed":
            customer_dict.pop(id)
            db['Customer'] = customer_dict
            db.close()

            if not customer_dict:  # If all customers are deleted, reset last_customer_id to 0
                customer.reset_customer_id()

            return redirect(url_for('retrieve_customer'))
        else:
            db.close()
            return render_template('asher/retrieveCustomer.html', customers_list=customer_dict.values(), show_alert=True)

    else:
        db.close()
        return redirect(url_for('/asher/retrieve_customer'))

@app.route('/asher/update_status/<int:id>', methods=['POST'])
def update_status(id):
    customer_dict = {}
    db = shelve.open('storage1.db', 'w')
    customer_dict = db.get('Customer', {})

    if id in customer_dict:
        customer = customer_dict[id]
        new_status = request.form['status']
        customer.set_status(new_status)
        db['Customer'] = customer_dict

    db.close()
    return redirect(url_for('retrieve_customer'))

faq_data = {
    "General": {
        "The style I want is out of stock.": "We are very sorry that the item you need is out of stock. When you try to select the size you need, if the item is out of stock, the 'add to cart' button will turn grey and above it you will see a link to 'Notify me when available'.This will bring you to our sign-in page where you can sign-in or create an account. As soon as we get more inventory of the item, we will email to let you know!",
        "How can I update account info?": "Register today to enjoy fast and easy checkout. An OnlineShoes account allows you to store payment methods and addresses, check the status of orders, view your order history, select shopping preferences and save items in your shopping bag for up to 30 days.",
        "Forgot password?": "Forgot your Password? No problem. Go to Your Account, there you can view your password hint or have your password emailed to you.",
        "Manage account": "Go to Your Account and sign in to change any of your account information including shipping and billing information, your preferred payment method and your preferences regarding receiving ShiftWalk emails"
    },
    "Payment & Order": {
        "What methods of payment do you accept?": "We currently accept the following methods of payment: Visa, MasterCard, American Express, Discover and PayPal. We do not accept Cash, CODs, checks, credit card gift cards (unless bank issued), or money orders. Due to our US credit card verification service, we are unable to accept credit cards with international billing addresses.",
        "Can I change my order?": "Our goal is to expedite your order as quickly as possible; therefore, once your order is placed it cannot be cancelled or changed. You may always return the item once you receive it and return shipping is free. If you are unsure of what size to order or have any other questions about any of our products, please feel free to call us at (888) 973-6620. We’re happy to help you find the best style for you.",
        "How long does processing and shipping take?": "The time it takes for you to receive your order will depend on your location, the item(s) ordered, and the shipping speed you selected. Processing and packing times are estimated 24-48 hours. This excludes orders placed on the weekend.",
        "How long do refunds take?": "Please allow two weeks for your return to be processed. You will receive an email to confirm a successful return. A credit should appear on your credit card, or original method of payment, within two billing cycles."
    },
    "Customer service": {
        "How can I contact customer service?": "We currently offer the following ways to contact us:<br> Phone: +65 9123 4567 <br>Email: ShiftWlak@onlineshoes.com",
        # Add more questions and answers in category2
    },
    # Add more categories here
}

@app.route("/asher/faq")
def faq_page():
    query = request.args.get('query')
    if query:
        search_results = {}
        for category, faqs in faq_data.items():
            search_results[category] = {question: answer.replace('\n', '<br>') for question, answer in faqs.items() if query.lower() in question.lower()}
    else:
        search_results = None
    return render_template("asher/faq.html", categories=faq_data.keys(), selected_category=None, faq_items=faq_data, search_results=search_results)

@app.route("/category/<category>")
def faq_category(category):
    if category in faq_data:
        return render_template("asher/faq.html", categories=faq_data.keys(), selected_category=category, faq_items=faq_data[category], search_results=None)
    else:
        return "Category not found."

# New search endpoint to handle search functionality
@app.route("/asher/search")
def search():
    query = request.args.get('query')
    if query:
        search_results = {}
        for category, faqs in faq_data.items():
            category_results = {question: answer.replace('\n', '<br>') for question, answer in faqs.items() if
                                query.lower() in question.lower()}
            if category_results:
                search_results[category] = category_results
    else:
        search_results = None
    return render_template("asher/faq.html", categories=faq_data.keys(), selected_category=None, faq_items=faq_data,
                           search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)