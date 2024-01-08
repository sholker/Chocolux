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

@app.route('/login')
def show_login_form():
    message = request.args.get('message', None)
    return render_template('login.html', message=message)

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

@app.route('/addItem')
def add_item():

    if request.args.get('userId'):

        user_details = DB.search_in_table_by_id("users",id=request.args.get('userId'))
        print(f"user_details = > {user_details}")
        if user_details:
            if user_details[-1] == 1:
                return "addItem"
    print("Warning! User is not Admin try to access!!")
    abort(403)

@app.route('/logout')
def logout():
    return render_template("login.html")


###### GET ######

###### POST #####
@app.route('/register')
def show_register_form():
    message = request.args.get('message', None)
    return render_template('register.html', message=message)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Received login request with username: {username}, password: {password}")
        is_exist,result = DB.search_in_table_by_fields("users",username=username,password=password)
        print(f"login checking user: {is_exist} {result}")

        if is_exist:
            print(f"login successful for user {username} id = {result[0]}")

            return render_template("index.html", userId=result[0], fullname=f"{result[1].title()} {result[2].title()}", current_time=current_time)

        return render_template("login.html", message=result)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname').lower().strip()
        lastname = request.form.get('lastname').lower().strip()
        email = request.form.get('email').lower().strip()
        username = request.form.get('username').lower().strip()
        password = request.form.get('password')
        type = False
        table_name = "users"
        print(f"New user registration request with firstname: {firstname}, lastname: {lastname}, email: {email}, username: {username}, password: {password}")

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
        if DB.search_in_table_by_fields(table_name,username=username,email=email)[0]:
            print(f"User already exists")
            message = "User already exists"

            return render_template("register.html", message=message)
            # return message
        else:
            print(f"Adding new record to {table_name} table")
            result, message = DB.insert_into_table(table_name, firstname=firstname, lastname=lastname, email=email,
                                                   username=username, password=password,UserType=type)
            if result:
                message = "New user created"

        return render_template("register.html", message=message)

###### POST #####

#### ERRORS ####

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)