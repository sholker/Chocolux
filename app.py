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

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Received login request with username: {username}, password: {password}")
        is_exist,result = DB.search_in_table_by_fields("users",username=username,password=password)
        print(f"login checking user: {is_exist} {result}")

        if is_exist:
            print(f"login successful for user {username} id = {result[0]}")

            return render_template("index.html", userId=result[0], fullname=f"{result[1].title()} {result[2].title()}",is_admin={result[6]}, current_time=current_time)

        return render_template("login.html", message=result)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        message = request.args.get('message', None)
        return render_template('register.html', message=message)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Received login request with username: {username}, password: {password}")
        is_exist,result = DB.search_in_table_by_fields("users",username=username,password=password)
        print(f"login checking user: {is_exist} {result}")

        if is_exist:
            print(f"login successful for user {username} id = {result[0]}")

            return render_template("index.html", userId=result[0], fullname=f"{result[1].title()} {result[2].title()}",is_admin={result[6]}, current_time=current_time)

        return render_template("login.html", message=result)

### GET & POST ###

### FOR ADMIN ###
@app.route('/addItem',methods=['GET','POST']))
def add_item():
    if request.args.get('userId'):
        if request.method == 'GET':
            return render_template('addItem.html')
        if request.method == 'POST':
            pass

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