

from flask import Flask, request, render_template, abort,redirect # import Flask package for web app
from database_com import DatabaseConnection # import DatabaseConnection class from database_com.py
from datetime import datetime # import datetime package for time
import random # import random package for random number generation
import string # import string package for random string generation

DB = DatabaseConnection() # create a new instance of DatabaseConnection class
app = Flask(__name__, static_folder='static') # create a new instance of Flask class

# globals variables
glob_var = {
    'current_time': datetime.now(),  # now time
    'client_ID': None,  # the client ID of the user
    'is_admin': False,  # if the user is admin or not
    'fullname': None  # the full name of the user
}


###### GET ######
@app.route("/") # define the route for the home page
def welcome():
    '''
    This function is the home page of the web app.
    :return: the home page of the web app
    '''
    return render_template("index.html",  userId=glob_var.get('client_ID',None), fullname=glob_var.get('fullname',None),
                           is_admin=glob_var.get('is_admin',False),
                           current_time=glob_var.get('current_time',datetime.now()))


@app.route("/header") # define the route for the header page
def header():
    '''
    This function is the header page of the web app.
    we include the header and footer of the web app in all other pages in our website
    :return: the header page of the web app
    '''
    return render_template("header.html",  userId=glob_var.get('client_ID',None), fullname=glob_var.get('fullname',None),
                           is_admin=glob_var.get('is_admin',None), current_time=glob_var.get('current_time',datetime.now()))


@app.route("/footer") # define the route for the footer page
def footer():
    '''
    This function is the header page of the web app.
    we include the header and footer of the web app. in all other pages in our website
    :return: the footer page of the web app
    '''
    return render_template("footer.html")


@app.route('/userDetails') # define the route for the user details page
def user_details():
    user_details = DB.search_in_table_by_fields("users", id=glob_var.get('client_ID',None)) # get the user details from the database
    print(f"user_details = > {user_details}") # print the user details to console for debugging
    # the user details from the database look like this:
    # (17, 'admin', 'admin', 'admin@gmail.com', 'admin', 'admin', 1)
    # ( 16,'matthew', 'murdock', 'daredevil@gmail.com', 'daredevil', '123', 0)

    user_id, firstname, lastname, email, username, passwd, is_admiin = user_details # unpack the user details

    # return the user details page with the user details
    return render_template('userDetails.html', userId=user_id, firstname=firstname, lastname=lastname,
                           email=email, username=username, passwd=passwd,
                           fullname=request.args.get('fullname', f"{firstname} {lastname}"), current_time=glob_var.get('current_time',datetime.now()))


@app.route('/about') # define the route for the about page
def about():
    # return the about page
    return render_template("about.html", userId=glob_var.get('client_ID',None), fullname=glob_var.get('fullname',None),
                           current_time=glob_var.get('current_time',datetime.now()))


@app.route('/logout') # define the route for the logout page
def logout():
    # reset the global variables, remove the user ID from the session
    for key in glob_var:
        glob_var[key] = None

    # set the current time to now
    glob_var['current_time'] = datetime.now()
    # send to login page
    return render_template("login.html")

###### GET ######

### GET & POST ###
@app.route('/login', methods=['GET', 'POST']) # define the route for the login page
def login():
    # login function

    if request.method == 'GET': # when the request is GET
        message = request.args.get('message', None) # get the message from the query string
        return render_template('login.html', message=message) # return the login page with the message

    else: # when the request is POST
        username = request.form.get('username') # get the username from the form data
        password = request.form.get('password') # get the password from the form data

        print(f"Received login request with username: {username}, password: {password}")
        # check if the username and password exist in the database
        # returned True/False and the result of the search
        is_exist, result = DB.search_in_table_by_fields("users", username=username, password=password)
        print(f"login checking user: {is_exist} {result}")

        if is_exist: # if the username and password exist in the database
            print(f"login successful for user {username} id = {result[0]}")
            global glob_var # set the global variables
            glob_var['client_ID'] = result[0] # set the client ID of the user
            glob_var['fullname'] = f"{result[1].title()} {result[2].title()}" # set the full name of the user
            glob_var['is_admin'] = (False if result[6] == 0 else True) # set the is_admin variable of the user

            # call to the '/shop' route with 'GET' method to show the products list
            return redirect('/shop', code=302)
        else:
            # return the login page with the message
            abort(401) # if the username and password do not exist in the database

        # return the login page with the message
        return render_template("login.html", message=result) # return the login page with the message


@app.route('/register', methods=['GET', 'POST']) # define the route for the register page
def register():
    try:
        if request.method == 'GET':  # if the request is GET
            message = request.args.get('message', None)  # get the message from the query string
            return render_template('register.html', message=message)  # return the register page with the message

        else:  # POST
            # get the firstname from the form data, lowercase and strip( remove leading and trailing spaces)
            firstname = request.form.get('firstname').lower().strip()
            # get the lastname from the form data, lowercase and strip( remove leading and trailing spaces)
            lastname = request.form.get('lastname').lower().strip()
            # get the email from the form data, lowercase and strip( remove leading and trailing spaces)
            email = request.form.get('email').lower().strip()  # get the email from the form data
            username = request.form.get('username').lower().strip()
            password = request.form.get('password')  # get the password from the form data
            type = False  # set the user type to False, by default
            table_name = "users"  # set the table name to users, whoes we working with in this function
            print(
                f"New user registration request with firstname: {firstname}, lastname: {lastname}, email: {email}, username: {username}, password: {password}")

            # check if the username and email exist in the database
            if not DB.table_exists(f"{table_name}"):
                print(f"creating table {table_name}")
                # if the table does not exist, create it
                # create the table with the fields, defined in the dictionary below and set primery key/ foreign key and the tupe of the field
                DB.create_table(
                    table_name=table_name,  # set the table name to users
                    firstname={'type': 'VARCHAR(255)'},  # set the firstname field to VARCHAR(255)
                    lastname={'type': 'VARCHAR(255)'},  # set the lastname field to VARCHAR(255)
                    email={'type': 'VARCHAR(255)', 'unique': True},
                    # set the email field to VARCHAR(255) and set it as unique
                    username={'type': 'VARCHAR(255)', 'unique': True},
                    # set the username field to VARCHAR(255) and set it as unique
                    password={'type': 'VARCHAR(255)'},  # set the password field to VARCHAR(255)
                    userType={'type': 'BOOLEAN'},  # set the userType field to BOOLEAN, 1 for admin, 0 for client
                )

            print(f"checking if username {username} already exists")
            # check if the username already exists in the database
            if DB.search_in_table_by_fields(table_name, username=username, email=email)[0]:
                print(f"User already exists")
                # if the username already exists, return the register page with the message
                message = "User already exists, please login"
                # return the register page with the error message
                return render_template("register.html", message=message)
            else:
                print(f"Adding new record to {table_name} table")
                # if the username does not exist, insert the new user to the database
                # insert the new user to the database, by fields defined in the dictionary below
                result, user_id = DB.insert_into_table(table_name, firstname=firstname, lastname=lastname, email=email,
                                                       username=username, password=password, UserType=type)
                print(f"result of the insert: {user_id}")
                # check if the user was created successfully
                if result:
                    global glob_var  # set the global variables
                    glob_var['client_ID'] = user_id  # set the client ID of the user
                    result, user_details = DB.search_in_table_by_fields(table_name, id=user_id)
                    glob_var[
                        'fullname'] = f"{user_details[1].title()} {user_details[2].title()}"  # set the full name of the user
                    glob_var['is_admin'] = (
                        False if user_details[6] == 0 else True)  # set the is_admin variable of the user

                    # call to the '/chocolate' route with 'GET' method to show the chocolate list
                    print("Registered user successfully, redirecting to chocolate page")
                    return redirect('/shop', code=302)

                else:
                    # if the user was not created successfully, return the register page with the error message
                    message = user_id
            # if the user was not created successfully, return the register page with the error message
            return render_template("register.html", message=message)
    except Exception as e:
        print(e) # if there was an error, print it and return the register page with the error message
        return render_template("register.html", message=e)


@app.route('/shop', methods=['GET', 'POST'])  # This is the route for the shop page
def shop():
    try:
        message = request.args.get('message', None) # Get the message from request args
        print(f'shop message = {message}')
        table_name = 'items'  # Replace with your actual table name
        # get all the items from the database
        # found is true if the table is not empty, false otherwise
        found, rows = DB.select_all_from_table(table_name)
        print(f"items = {rows}")

        if not found: # if the table is empty
            message = "Error retrieving data from the database" # set the message to the error message

        if request.method == 'POST': # when the form is submitted
            item = request.form.get('item_id') # Get the item from the form data
            quantity = request.form.get('quantity') # Get the quantity from the form data
            message = f"Adding to shopping cart x{quantity}" # Set the message to the quantity

            print(f"adding to shopping cart item {item} x{quantity}")
            message = add_2_shopping_cart(item, quantity ) # Add the item to the shopping cart
            print(message)


        print(type(message))
        message = None if message == 'None' else message # Fixing the message type

        # return the shop page with the items, the message and the user details
        return render_template('chocolate.html', userId=glob_var.get('client_ID',None),
                               fullname=glob_var.get('fullname',None), is_admin=glob_var.get('is_admin',None),
                               current_time=glob_var.get('current_time',datetime.now()), found=found, rows=rows, message=message)

    except Exception as e:
        # if there was an error, print it and return the shop page with the error message
        return render_template('chocolate.html', userId=glob_var.get('client_ID', None),
                        fullname=glob_var.get('fullname', None), is_admin=glob_var.get('is_admin', None),
                        current_time=glob_var.get('current_time', datetime.now()), found=found, rows=rows,
                        message=message)


def add_2_shopping_cart(item_id, quantity):
    # add the item to the shopping cart by user ID and item ID
    table_name = "shopping_cart" # set table name is working on it
    message = None # set the message to None
    print(f"checking if table {table_name} exists")
    print(f"datails of adding to shopping cart: {item_id} {quantity}")
    print(f"datails of adding to shopping cart types: {type(item_id)} {type(quantity)}")
    print(f"{table_name} checked if exist")

    if not DB.table_exists(f"{table_name}"): # if the table does not exist, create it
        print(f"{table_name} created")
        # create the table with the following fields, set primery key and foregin key:
        DB.create_table(
            table_name=table_name,
            # set the user ID as foregin key and reference table to users and the foregin key field to id
            user_Id = {'type': 'INT', 'foreign_key': True, 'reference_table': 'users', 'foreign_key_field': 'id'},
            # set the item ID as foregin key and reference table to items and the foregin key field to id
            item_Id = {'type': 'INT', 'foreign_key': True, 'reference_table': 'items', 'foreign_key_field': 'id'},
            quantity={'type': 'INT'},
            lastUpdate={'type': 'DATETIME'},
        )
        print(f"creating table {table_name}")

    print(f"checking if item {item_id} already exists, and update the quantity if it does")

    # check if the item already exists in the shopping cart for the user
    # returned True/False,data
    # if the item exists, update the quantity
    exist_item = DB.search_in_table_by_fields(table_name, user_Id=glob_var.get('client_ID'),item_Id=item_id)
    if exist_item[0]: # if the item exists
        print(f"Item already added to shopping cart")

        # get the quantity of the item is wnat to add and already exists in the shopping cart
        err, item_quentity = DB.search_in_table_by_fields("items", id=item_id,get_one = True)
        item_quentity = item_quentity[5] # get the quantity of the item

        # check if the quantity of the item in the shopping cart is greater than the quantity of the item in the database
        if int(item_quentity) > int(exist_item[1][3]) + int(quantity):
            print(f"Updating the quantity of the item for cartID {exist_item[1][0]} to {exist_item[1][3]} + {quantity}")
            # update the quantity of the item in the shopping cart by item ID
            result, err = DB.update_table_by_fields(table_name,id=exist_item[1][0],  quantity=int(exist_item[1][3]) + int(quantity), lastUpdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            # if the quantity of the item in the shopping cart is less than the quantity of the item in the database
            print("thre not enough stock for this item")
            message = "There not enough stock for this item" # set the message to the error message
            return message

        if result: # if the update was successful
            message = "item quantity updated" # set the message to the success message
            print("Update successful!")
        else: # if the update was not successful
            message = "Something went wrong, please try again" # set the message to the error message
            print(f"Error: {err}")
        # return the message to the user
        return message

    else: # if the item does not exist, add it to the shopping cart
        print(f"Adding new record to {table_name} table")
        # insert the item into the shopping cart by user ID and item ID
        glob_var['current_time'] = datetime.now() # update current time
        # insert the item into the shopping cart
        result, message = DB.insert_into_table(table_name, user_Id=glob_var.get('client_ID'), item_Id=int(item_id),
                                               quantity=int(quantity), lastUpdate=glob_var.get('current_time',datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))

        if result: # if the insert was successful
            print(f"Added new Item to the database: {result}")
            message = "New Item Added" # set the message to the success message

    return message


@app.route('/cart', methods=['GET', 'POST']) # this route will show the shopping cart
def cart():
    try:
        message = request.args.get('message', None) # get the message from request args

        table_name = 'shopping_cart_details'  # Replace with your actual table name
        response = True # set the response to true, so that the view will be created if it does not exist
        if not DB.table_exists(f"{table_name}"): # check if the table exists
            response = DB.create_view_4_cart_details() # create the view if it does not exist
            print(f"creating view {table_name}")
        if not response: # if the view is not created
            return "somtiong went wrong,pls try again" # return an error message

        # get the shopping cart details
        # found is true if the cart is not empty, flase otherwise
        # rows is a list of tuples with the details of the items in the cart
        found, rows = DB.search_in_table_by_fields(table_name,get_one=False, user_ID=glob_var.get('client_ID'))
        print(f"shopping cart details = {rows}")
        print(f'found = {found}')

        # if the cart is empty, show a message
        if not found:
            message = "No items in shopping cart" # set the message to show in the view
            print(message)
            # reload this page with the message
            return render_template('shoppingCart.html', userId=glob_var.get('client_ID', None),
                                   fullname=glob_var.get('fullname', None), is_admin=glob_var.get('is_admin', None),
                                   current_time=glob_var.get('current_time', datetime.now()),found =found, rows=[],
                                   total=0, message=message)
        # if the cart is not empty, show the items in the cart
        # calculate the total of the items in the cart
        total = sum([i[6] for i in rows]) # sum the total of the items in the cart
        glob_var['total'] = total # set the total in the glob_var
        if request.method == 'POST': # when the request is a post request
            # get the cart_ID from the form
            print(f" cart Post request: {request.form}") #
            cart_ID = request.form.get('cart_ID')
            # remove the row from the table, empty the cart
            result, err = DB.delete_row('shopping_cart',id=cart_ID)
            # check if the row was deleted
            if not result:
                message = err # set the message to show in the view
                print(err)
            print("Delete row from shopping cart")
            # reload this page with the message
            return redirect(f'/cart?message={message}', code=302)

        # if the request is a get request, return the shopping cart template
        return  render_template('shoppingCart.html', userId=glob_var.get('client_ID', None),
                                fullname=glob_var.get('fullname', None),current_time=glob_var.get('current_time', datetime.now()),
                                is_admin=glob_var.get('is_admin', None),found=found, rows=rows, total=total, message=message)

    except Exception as e:
        # when an error occurs, return the error message
        return render_template('shoppingCart.html', userId=glob_var.get('client_ID', None),
                               fullname=glob_var.get('fullname', None), is_admin=glob_var.get('is_admin',None),
                               current_time=glob_var.get('current_time', datetime.now()), found=False, rows=[],
                               total=0, message=e)


def update_stock_quantity():
    table_name = 'items'  # table name we're working with in this function

    # get all the items are client has added to cart and bought
    found, shooping_items = DB.search_in_table_by_fields('shopping_cart',get_one=False, user_ID=glob_var.get('client_ID'))
    found, items = DB.select_all_from_table(table_name) # get all the items from the items table
    print(f"shopping cart item = {shooping_items}")
    print(f"items = {items}")

    for cart_item in shooping_items:
        item_id = cart_item[2]  # Assuming item ID is at index 2 in cart_item
        quantity = cart_item[3]  # Assuming quantity is at index 3 in cart_item
        # Find the item in the items list
        for item in items:
            if item[0] == item_id:  # Assuming item ID is at index 0 in items
                print(item)
                current_quantity = int(item[5])  # Assuming current quantity is at index 6 in items
                update_quantity = current_quantity - quantity # calculate the new quantity
                if update_quantity < 0: # if the new quantity is less than 0, set it to 0
                    update_quantity = 0 # set the new quantity to 0
                print(f"old quantity = {current_quantity}, new quantity = {update_quantity}")
                # Update the quantity in the items table
                response = DB.update_table_by_fields("items", id=item_id, quantity=update_quantity,outOfStock=0 if update_quantity==0 else 1)
                break # break out of the loop as we found the item we need to update

@app.route('/tank') # define the tank route
def tank():
    orderID = request.args.get('orderID', None) # get the orderID from the request args
    # return the order details to the user
    return render_template('tankOrder.html', fullname=glob_var.get('fullname', None), order_number=orderID)

@app.route('/order', methods=['GET','POST']) # define the order route
def order():
    # set total to 0, so that we can show an error message if the total is 0
    total = glob_var.get('total', 0)

    address_table_name = 'address_details'  # table name for address details
    payment_table_name = 'payment_details'  # table name for payment details

    print(f"total = {total}")
    message = request.args.get('message', None) # get the message from the request args
    if total == 0: # check if the total is 0, if it is, then we need to show an error message
        message = "the total is 0, please add items to the cart"
    if request.method == "GET": # when the request is a get request
        # get the address and payment details for the user
        # found_* is true/flase - True if the data was found, False if notm the data of this found.
        # address_data and payment_data are the data of the address and payment details
        # address_data is a list of tuples, so we need to convert it to a list of dictionaries
        found_address, address_data = DB.search_in_table_by_fields(address_table_name, user_ID=glob_var.get('client_ID'))
        # payment_data is a list of tuples, so we need to convert it to a list of dictionaries
        found_payment, payment_data = DB.search_in_table_by_fields(payment_table_name, user_ID=glob_var.get('client_ID'))

        # call the order template with the data
        return render_template('order.html', userId=glob_var.get('client_ID', None), total=request.args.get('total', 0),
                               is_admin=glob_var.get('is_admin', None),
                               current_time=glob_var.get('current_time', datetime.now()),found_address=found_address,
                               found_payment=found_payment,address_data=address_data,payment_data=payment_data,message=message)

    else: # when the request is a post request
            # table name we're working with in this function
            table_name = 'orders'  # table name we're working with in this function
            print(f"table name = {table_name}")
            # genarate a random order ID like this: 12345m - 5 random characters
            # and then join them together to one string
            orderID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) # generate a random order ID
            print(f"orderID = {orderID}")

            address_table_name = 'address_details'  # table name for address details
            payment_table_name = 'payment_details'  # table name for payment details

            print(f"{address_table_name} checked if exist")
            if not DB.table_exists(f"{address_table_name}"): # check if the table exists, if not, create it
                print(f"{address_table_name} created")
                # create the table, by passing the table name and the fields as a dictionary
                DB.create_table(
                    table_name=address_table_name, # table name we're working with in this function
                    # user id is a foreign key, so we need to pass the type, reference table and reference field
                    user_ID={'type': 'INT', 'foreign_key': True, 'reference_table': 'users', 'foreign_key_field': 'id'},
                    # address is a varchar(255)
                    address={'type': 'varchar(255)'},
                    # city is a varchar(255)
                    city={'type': 'varchar(255)'},
                    # country is a varchar(255)
                    country={'type': 'varchar(255)'},
                ) # create the table, by passing the table name and the fields as a dictionary
                print(f"creating table {address_table_name}")

            print(f"{payment_table_name} checked if exist")
            if not DB.table_exists(f"{payment_table_name}"): # check if the table exists, if not, create it
                print(f"{payment_table_name} created")
                # create the table, by passing the table name and the fields as a dictionary
                DB.create_table(
                    table_name=payment_table_name, # table name we're working with in this function
                    # user id is a foreign key, so we need to pass the type, reference table and reference field
                    user_ID={'type': 'INT', 'foreign_key': True, 'reference_table': 'users', 'foreign_key_field': 'id'},
                    # card_number is a varchar(255)
                    card_number={'type': 'varchar(255)'},
                    # expride_date is a varchar(255)
                    expride_date={'type': 'varchar(255)'},
                    # security_code is a varchar(255)
                    security_code={'type': 'varchar(255)'},
                )# create the table, by passing the table name and the fields as a dictionary
                print(f"creating table {address_table_name}")

            print(f"{table_name} checked if exist")
            if not DB.table_exists(f"{table_name}"): # check if the table exists, if not, create it
                print(f"{table_name} created")
                DB.create_table(
                    table_name=table_name, # table name we're working with in this function
                    order_ID={'type': 'varchar(255)', 'primery_key': True}, # order id is a varchar(255)
                    # user id is a foreign key, so we need to pass the type, reference table and reference field
                    user_ID={'type': 'INT', 'foreign_key': True, 'reference_table': 'users', 'foreign_key_field': 'id'},
                   # address id is a foreign key, so we need to pass the type, reference table and reference field
                    address_ID={'type': 'INT', 'foreign_key': True, 'reference_table': address_table_name,
                                'foreign_key_field': 'id'},
                    # payment id is a foreign key, so we need to pass the type, reference table and reference field
                    payment_ID={'type': 'INT', 'foreign_key': True, 'reference_table': payment_table_name,
                                'foreign_key_field': 'id'},
                    # total is a INT
                    total={'type': 'INT'},
                    # order date is a DATETIME
                    order_date={'type': 'DATETIME'},
                )# create the table, by passing the table name and the fields as a dictionary
                print(f"creating table {table_name}")

            # add the address details to the address table
            if_success_address,address_ID = DB.insert_into_table(address_table_name,
                                                                 user_ID=glob_var.get('client_ID'), address=request.form.get('address'),
                                                                 city=request.form.get('city'),country=request.form.get('country'))

            # add the payment details to the payment table
            if_success_payment,payment_ID = DB.insert_into_table(payment_table_name,
                                                                user_ID=glob_var.get('client_ID'), card_number=request.form.get('cardNumber'),
                                                                expride_date=request.form.get('expiration'), security_code=request.form.get('securityCode'))

            # add the order details to the order table
            if if_success_address and if_success_payment:
                DB.insert_into_table(table_name,order_ID = orderID,
                                     user_ID=glob_var.get('client_ID'),address_ID=address_ID,payment_ID=payment_ID, total=total, order_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                update_stock_quantity() # update the stock quantity
                # delete the shopping cart
                result, err = DB.delete_row('shopping_cart',user_Id=glob_var.get('client_ID'))
                print(f"order {orderID} added")
                return redirect(f'/tank?orderID={orderID}',code=302) # redirect to the tank page
            else:
                # return the error message to the user
                return ("Somthing went wrong, please try again")


    # return  an empty form to the user (first order)
    return render_template('order.html', userId=glob_var.get('client_ID', None),total=total,
                           fullname=glob_var.get('fullname',None), is_admin=glob_var.get('is_admin',None),
                           current_time=glob_var.get('current_time',datetime.now()), message=message)

### GET & POST ###

### FOR ADMIN ###


@app.route('/addItem', methods=['GET', 'POST']) # define the route for add item
def add_item():
    # this page is only for admin
    # adding new item to the database

    message = request.args.get('message', None) # get the message from request args
    is_admin = glob_var.get('is_admin', False) # get the value of is_admin from the global variable

    print(f"is_admin = {is_admin}")

    if is_admin: # if the user is admin
        print("is admin")
        if request.method == 'GET': # when the request is GET
            # display the add item form page
            return render_template("admin/addNewItem.html", userId=glob_var.get('client_ID', None),
                                   is_admin=glob_var.get('is_admin'),fullname=glob_var.get('fullname',None), current_time=glob_var.get('current_time',datetime.now()), message=message)
        else: # POST
            # get the form data from the request
            # set item name from form data, convert it to title case and strip the whitespaces
            ItemName = request.form.get('ItemName').title().strip()
            # set item price from form data, and convert it to int
            price = int(request.form.get('price'))
            # set item quantity from form data, and convert it to int
            quantity = int(request.form.get('quantity'))
            # set item description from form data, convert it to title case
            description = request.form.get('description').title()
            # set out of stock from form data, and convert it to boolean
            out_of_stock = 'outOfStock' in request.form  # Checkbox value

            # check if the item name already exists in the database
            if out_of_stock and quantity != '0':
                #  if the item is out of stock and the quantity is not 0, then we need to update the quantity
                message = "Quantity cannot be 0 if out of stock"
                # reload this page with the message
                return redirect(f'/addItem?message={message}', code=302)

            # set the out of stock value to True if the quantity is 0
            if quantity == '0':
                out_of_stock = True

            # set the image path to None if the image is not uploaded
            print(f"request.files = {request.form.get('imageInput')}")
            if 'image' in request.files:
                image = request.files['image'] # get the image from the request
                # Save the image to a specific location or process it as needed
                image.save('static/images/' + image.filename)
                print('Image uploaded successfully!')

            # set the image path to the image path if the image is uploaded
            image_path = f"static/images/{request.form.get('imageInput')}"
            print(f'image_path = {image_path}')

            table_name = "items"
            print(
                f"Adding new item to the database with ItemName: {ItemName}, price: {price}, quantity: {quantity}, description: {description}, image: {image_path}, outOfStock: {out_of_stock}")

            # check if the table exists, if not create it
            if not DB.table_exists(f"{table_name}"):
                print(f"creating table {table_name}")
                # create the table, by the fields and their data types, and set the primary key to the ItemName field
                DB.create_table(
                    table_name=table_name,
                    ItemName={'type': 'VARCHAR(255)', 'unique': True},
                    desciption={'type': 'LONGTEXT'},
                    price={'type': 'INT'},
                    image_path={'type': 'VARCHAR(255)'},
                    quantity={'type': 'VARCHAR(255)'},
                    outOfStock={'type': 'BOOLEAN'},
                    lastUpdate={'type': 'DATETIME'},
                )

            # check if the item already exists in the database
            print(f"checking if item {ItemName} already exists")
            if DB.search_in_table_by_fields(table_name, ItemName=ItemName)[0]:
                print(f"Item already exists")
                message = "Item already exists" # set the message
                # reload this page with the message
                return redirect(f'/addItem?message={message}', code=302)


            else: # if the item does not exist in the database
                print(f"Adding new record to {table_name} table")
                current_time = datetime.now() # get the current time
                # insert the item into the database, sending the values of the fields as parameters
                # set the datatime as mysql datetime format
                result, message = DB.insert_into_table(table_name, ItemName=ItemName, desciption=description,
                                                       price=price,
                                                       image_path=image_path, quantity=quantity,
                                                       outOfStock=out_of_stock,
                                                       lastUpdate=current_time.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"Added new Item to the database: {result}")

                if result: # if the item was added successfully
                    message = "New Item Added" # set the message

            # reload this page with the message
            return redirect(f'/addItem?message={message}', code=302)

    else:
        # if the user is not logged in, redirect to the login page
        print("Warning! User is not Admin try to access to add new Item!!")
        abort(403)
@app.route('/report', methods=['GET']) # define the route for the report page
def report():
    '''
    This function is used to render the report page, it will be used to show the report of the items sold by the users.
    '''
    message = None # set the message to None
    if glob_var.get('is_admin', False): # check if the user is an admin

        table_name = "user_order_totals" # set the table name to user_order_totals
        response = True # set the response to True
        if not DB.table_exists(f"{table_name}"): # check if the table exists, if not create it
            # create the table, by the fields and their data types, and set the primary key to the ItemName field
            response = DB.create_view_4_admin_report()
            # check if the table was created successfully
            if not response:
                # if the table was not created successfully, set the response to False and set the message
                message = "Something went wrong, please try again"

        # check if the table exists, if not create it
        # found is true if the table exists, false otherwise
        # rows is a list of all rows in the table
        found, rows = DB.select_all_from_table(table_name)
        print(f"report order = {rows}")
        print(f'found = {found}')

        # check if the table exists, if not create it
        if not found:
            message = "No orders to show" # set the message
            print(message)
            # return the report.html page with the message
            return render_template('admin/report.html', userId=glob_var.get('client_ID', None),
                                   fullname=glob_var.get('fullname', None), is_admin=glob_var.get('is_admin', None),
                                   current_time=glob_var.get('current_time', datetime.now()), found=found, rows=[],
                                   message=message)


        # return all rows from the table and sent it to the report.html page
        return render_template('admin/report.html', userId=glob_var.get('client_ID', None),
                               fullname=glob_var.get('fullname', None), is_admin=glob_var.get('is_admin', None),
                               current_time=glob_var.get('current_time', datetime.now()), found=found, rows=rows,
                               message=message)

    else:
        # if the user is not logged in, redirect to the login page
        print("Warning! User is not Admin try to access to report!!")
        abort(403) # abort the request with a 403 error code

### FOR ADMIN ###

#### ERRORS ####

@app.errorhandler(403) # define the error handler for the 403 error code
def forbidden_error(error):
    # forbidden_error is the function that will be called if the error code is 403
    # its heppends when the user is not logged in, or is not an admin and tries to access to a page that requires admin privileges
    return render_template('errors/403.html'), 403 # return the 403.html page with a 403 error code


@app.errorhandler(404) # define the error handler for the 404 error code
def not_found_error(error):
    # not_found_error is the function that will be called if the error code is 404
    # its heppends when the user tries to access to a page that does not exist
    return render_template('errors/404.html'), 404 # return the 404.html page with a 404 error code

@app.errorhandler(401) # define the error handler for the 401 error code
def Unauthorized(error):
    # Unauthorized is the function that will be called if the error code is 401
    # its heppends when the user tries to access to a page that requires login
    return render_template('errors/401.html'), 401 # return the 401.html page with a 401 error code

if __name__ == '__main__':
    app.run(debug=True)
