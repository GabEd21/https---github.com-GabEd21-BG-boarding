from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from DBConnections import add_text, add_payment


app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rsd253896@'
app.config['MYSQL_DB'] = 'bgdorm'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = 'Error'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE Admin_UserName = %s AND Admin_Password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['AdminId'] = account['AdminId']
            session['Admin_UserName'] = account['Admin_UserName']
            return redirect(url_for('test'))
        else:
            msg = 'Incorrect username/password!'
        return render_template('login.html', msg=msg)
    

@app.route('/test')
def test():
    return render_template('Test.html')

@app.route('/add_boarder', methods=["GET", "POST"])
def add_boarder():
    if 'loggedin' in session:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            firstName = request.form['firstName']
            middleName = request.form['middleName']
            lastName = request.form['lastName']
            address = request.form['address']
            email = request.form['email']
            mobile = request.form['mobile']
            school = request.form['school']
            course = request.form['course']
            schoolYear = request.form['schoolYear']
            emergencyName = request.form['emergencyName']
            emergencyNumber = request.form['emergencyNumber']
            emergencyRelationship = request.form['emergencyRelationship']
            add_new = add_text(username, password, firstName, middleName, lastName, address, email, mobile, school, course, schoolYear, emergencyName, emergencyNumber, emergencyRelationship)
            return redirect(url_for('test'))
    return render_template('Addboarder.html')

@app.route('/view_boarder')
def view_boarder():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT Customer_UserName, Customer_FirstName, Customer_MiddleName, Customer_LastName FROM customer')
        customers = cursor.fetchall()
        
        cursor.close()
        
        return render_template('ViewBoarder.html', customers=customers)
    return redirect(url_for('index'))

@app.route('/account_student', methods=['GET'])
def account_student():
    if 'loggedin' in session:
        username = request.args.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT * FROM customer WHERE Customer_UserName LIKE %s", [username])
        customer = cursor.fetchone()

        if customer:
            cursor.execute('''
                SELECT c.*, p.AmountPaid, p.DatePaid, p.Status, p.Remarks
                FROM customer AS c
                LEFT JOIN contract AS p ON c.CustomerID = p.CustomerID
                WHERE c.Customer_UserName = %s
            ''', [username])
            payment = cursor.fetchone()

            cursor.close()

            if payment:
                customer.update(payment)

            return render_template('Account_Student.html', customer=customer)


@app.route('/add_payment', methods=['GET', 'POST'])
def create_payment():
    if 'loggedin' in session:
        if request.method == 'POST':
            customer_name = request.form['CustomerName']
            room_id = request.form['RoomID']
            date = request.form['Date']
            date_paid = request.form['DatePaid']
            amount_paid = request.form['AmountPaid']
            status = request.form['Status']
            remarks = request.form['Remarks']
            add_new = add_payment(customer_name, room_id, date, date_paid, amount_paid, status, remarks)     
        return render_template('AddPayment.html')
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)