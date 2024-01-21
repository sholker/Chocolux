from flask import Flask, request, render_template, abort
from database_com import DatabaseConnection
from datetime import datetime

DB = DatabaseConnection()
app = Flask(__name__,static_folder='static')
current_time = datetime.now()




###### GET ######
@app.route("/")
def welcome():
    return render_template("index.html", userId=request.args.get('userId', None),
                           fullname=request.args.get('fullname', None), current_time=current_time)

@app.route("/header")
def header():
    return render_template("header.html", userId=request.args.get('userId', None), fullname=request.args.get('fullname', None))

@app.route("/footer")
def footer():
    return render_template("footer.html")

@app.route('/userDetails')
def user_details():
    user_details = DB.search_in_table_by_id("users", id=request.args.get('userId'))
    print(f"user_details = > {user_details}")
    # (17, 'admin', 'admin', 'admin@gmail.com', 'admin', 'admin', 1)
    user_id,firstname,lastname,email,username,passwd,is_admiin = user_details


    return render_template('userDetails.html', userId=user_id, firstname=firstname,lastname=lastname,
                           email=email,username=username,passwd=passwd,fullname=request.args.get('fullname',f"{firstname} {lastname}"),current_time=current_time)

@app.route('/about')
def about():
    return render_template("about.html", userId=request.args.get('userId', None), fullname=request.args.get('fullname', None),current_time=current_time)


@app.route('/logout')
def logout():
    return render_template("login.html")


###### GET ######

### GET & POST ###
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        message = request.args.get('message', None)
        return render_template('login.html', message=message)

    else:
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Received login request with username: {username}, password: {password}")
        is_exist,result = DB.search_in_table_by_fields("users",username=username,password=password)
        print(f"login checking user: {is_exist} {result}")

        if is_exist:
            print(f"login successful for user {username} id = {result[0]}")

            return render_template("index.html", userId=result[0], fullname=f"{result[1].title()} {result[2].title()}",
                                   is_admin=(False if result[6] == 0 else True), current_time=current_time)

        return render_template("login.html", message=result)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        message = request.args.get('message', None)
        return render_template('register.html', message=message)

    else:# POST
        firstname = request.form.get('firstname').lower().strip()
        lastname = request.form.get('lastname').lower().strip()
        email = request.form.get('email').lower().strip()
        username = request.form.get('username').lower().strip()
        password = request.form.get('password')
        type = False
        table_name = "users"
        print(
            f"New user registration request with firstname: {firstname}, lastname: {lastname}, email: {email}, username: {username}, password: {password}")

        if not DB.table_exists(f"{table_name}"):
            print(f"creating table {table_name}")
            DB.create_table(
                table_name='users',
                firstname={'type': 'VARCHAR(255)'},
                lastname={'type': 'VARCHAR(255)'},
                email={'type': 'VARCHAR(255)', 'unique': True},
                username={'type': 'VARCHAR(255)', 'unique': True},
                password={'type': 'VARCHAR(255)'},
                userType={'type': 'BOOLEAN'},
            )

        print(f"checking if username {username} already exists")
        if DB.search_in_table_by_fields(table_name, username=username, email=email)[0]:
            print(f"User already exists")
            message = "User already exists"

            return render_template("register.html", message=message)
            # return message
        else:
            print(f"Adding new record to {table_name} table")
            result, message = DB.insert_into_table(table_name, firstname=firstname, lastname=lastname, email=email,
                                                   username=username, password=password, UserType=type)
            if result:
                message = "New user created"

        return render_template("register.html", message=message)

@app.route('/shop',methods=['GET','POST'])
def shop():
    try:
        message = None

        table_name = 'items'  # Replace with your actual table name
        headers, rows = DB.select_all_from_table(table_name)
        print(f"items = {rows}")

        if not headers:
            message = "Error retrieving data from the database"

        if request.method == 'POST':
            item = request.form.get('item_id')
            quantity = request.form.get('quantity')
            print(f"adding item {item} to shopping cart x{quantity}")
            message = f"Adding to shopping cart x{quantity}"
            print(message)

        return render_template('chocolate.html', userId=request.args.get('userId'), fullname=request.args.get('fullname'),
                           current_time=current_time, headers=headers, rows=rows, message=message)

    except Exception as e:
        return render_template('chocolate.html', userId=request.args.get('userId'),
                               fullname=request.args.get('fullname'), current_time=current_time, message=e)


### GET & POST ###

### FOR ADMIN ###


@app.route('/addItem',methods=['GET','POST'])
def add_item():
    global current_time
    is_admin = request.form.get('is_admin') if request.method == 'POST' else request.args.get('is_admin')
    print(f"is_admin = {is_admin}")

    if is_admin:
        print("is admin")
        if request.method == 'GET':
            return render_template("addNewItem.html", userId=request.args.get('userId'),fullname=request.args.get('fullname'),current_time=current_time)
        else:
            userId = request.form.get('userId')
            fullname = request.form.get('fullname')
            is_admin = request.form.get('is_admin')
            current_time = request.form.get('current_time')

            ItemName = request.form.get('ItemName').title().strip()
            price = str(request.form.get('price'))
            quantity = str(request.form.get('quantity'))
            description = request.form.get('description').title().strip()
            out_of_stock = 'outOfStock' in request.form  # Checkbox value

            if out_of_stock and quantity != '0':
                message = "Quantity cannot be 0 if out of stock"
                return render_template("addNewItem.html", message=message,userId = userId, fullname=fullname,is_admin=is_admin,current_time=current_time)

            image_path = None
            print(f"request.files = {request.form.get('imageInput')}")
            if 'image' in request.files:
                image = request.files['image']
                # Save the image to a specific location or process it as needed
                image.save('static/images/' + image.filename)
                print('Image uploaded successfully!')
            # image_path = 'static/images/' + request.form.get('image')
            image_path = request.form.get('imageInput')
            print(f'image_path = {image_path}')

            table_name = "items"
            print(
                f"Adding new item to the database with ItemName: {ItemName}, price: {price}, quantity: {quantity}, description: {description}, image: {image_path}, outOfStock: {out_of_stock}")

            if not DB.table_exists(f"{table_name}"):
                print(f"creating table {table_name}")
                DB.create_table(
                    table_name=table_name,
                    ItemName={'type': 'VARCHAR(255)', 'unique': True},
                    desciption={'type': 'LONGTEXT'},
                    price={'type': 'INT'},
                    image_path={'type': 'VARCHAR(255)', 'unique': True},
                    quantity={'type': 'VARCHAR(255)'},
                    outOfStock={'type': 'BOOLEAN'},
                    lastUpdate={'type': 'DATETIME'},
                )

            print(f"checking if item {ItemName} already exists")
            if DB.search_in_table_by_fields(table_name, ItemName=ItemName)[0]:
                print(f"Item already exists")
                message = "Item already exists"
                common_params = {
                    'message': message,
                    'fullname': fullname,
                    'is_admin': is_admin,
                    'current_time': current_time
                }
                return render_template("addNewItem.html", **common_params)
            else:
                print(f"Adding new record to {table_name} table")
                current_time = datetime.now()
                result, message = DB.insert_into_table(table_name, ItemName=ItemName, desciption=description,
                                                       price=price,
                                                       image_path=image_path, quantity=quantity,
                                                       outOfStock=out_of_stock,
                                                       lastUpdate=current_time.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"Added new Item to the database: {result}")

                if result:
                    message = "New Item Added"


            return render_template("addNewItem.html", message=message,userId=userId, fullname=fullname, is_admin=is_admin,
                                   current_time=current_time)
    else:
        print("Warning! User is not Admin try to access!!")
        abort(403)
### FOR ADMIN ###

#### ERRORS ####

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)