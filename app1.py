# use tb krna jb email id personal de kr k login kya ho
from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime
from flask_mail import Mail, Message
from functools import wraps

from flask_socketio import SocketIO
import eventlet




app = Flask(__name__)
app.secret_key = 'your_secret_key'

socketio = SocketIO(app, cors_allowed_origins="*")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] =   # MySQL username
app.config['MYSQL_PASSWORD'] =  # MySQL password
app.config['MYSQL_DB'] =   # MySQL database name
mysql = MySQL(app)

# Flask-Mail configuration for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Use 587 for TLS
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = # Default False  # Set to True if using port 587
app.config['MAIL_USERNAME'] =   # Your Gmail address
app.config['MAIL_PASSWORD'] =  # Or App Pass
app.config['MAIL_DEFAULT_SENDER'] =  #Sender Email Address


mail = Mail(app)
# Create tables if they don't exist
def create_tables():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone_no VARCHAR(15),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            location VARCHAR(255),
            registration_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS maids (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone_no VARCHAR(15),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            aadhar VARCHAR(20),
            address TEXT,
            food_preference ENUM('veg', 'nonveg', 'both'),
            skills TEXT,
            gender ENUM('male', 'female', 'other'),
            location VARCHAR(255),
            profile_pic VARCHAR(255),
            registration_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,  
    rating INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

''')

       # Create contact_form table if not exists
        cursor.execute('''
       CREATE TABLE IF NOT EXISTS contact_form (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

        ''')
        cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(15),
    maid_id INT NOT NULL,
    maid_name VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maid_id) REFERENCES maids(id)
);


        ''')
        # Commit the changes
    mysql.connection.commit()
    cursor.close()

@app.route('/try', methods=['GET', 'POST'])
def try1():
    return render_template('try.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')
@app.route('/index.html', methods=['GET', 'POST'])
def home1():
    return render_template('index.html')

@app.route('/indexhindi', methods=['GET', 'POST'])
def homehindi():
    return render_template('indexhindi.html')
@app.route('/indexBengali', methods=['GET', 'POST'])
def homeBengali():
    return render_template('indexBengali.html')

@app.route('/indexgujarati', methods=['GET', 'POST'])
def homegujarati():
    return render_template('indexgujarati.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
@app.route('/customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashpw(password.encode('utf-8'), gensalt())  # Hash the password
        location = request.form['location']
        
        # Get the current date and time for registration
        registration_datetime = datetime.now()
        
        # Create a cursor
        cur = mysql.connection.cursor()
        # Insert data into the customers table
        cur.execute(""" 
        INSERT INTO customers (name, phone_no, email, password, location, registration_datetime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, phone_no, email, hashed_password, location, registration_datetime))  
        # Commit the transaction
        mysql.connection.commit()
        # Close the cursor
        cur.close()
        # Flash success message
        flash('Thank you for registering! Your account has been created.', 'success')
        # Redirect to the registration page again
        return redirect(url_for('register_customer'))
    
    # Send real-time notification to all users

    socketio.emit('notification', {'message': f'📢 New customer {name} has registered!'})  
    flash('Your registration was successful!', 'success')
    return redirect(url_for('register_customer'))
   
    return render_template('customer.html')
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

# WebSocket Event for Sending Notifications Manually
@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    message = data.get('message', 'New notification!')
    socketio.emit('notification', {'message': message})
    return jsonify({"status": "Notification Sent"})
    

@app.route('/maid.html', methods=['GET', 'POST'])
def register_maid():
    if request.method == 'POST':
        name = request.form['name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        password = request.form['password']
        aadhar = request.form['aadhar']
        address = request.form['address']
        food_preference = request.form['food_preference']
        skills = request.form['skills']
        gender = request.form['gender']
        location = request.form['location']
        profile_pic = request.form['profile_pic']

        # Hash the password using bcrypt
        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert data into the 'maids' table
        cur.execute(''' 
            INSERT INTO maids (name, phone_no, email, password, aadhar, address, food_preference, 
                               skills, gender, location, profile_pic, registration_datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, phone_no, email, hashed_password, aadhar, address, food_preference, 
              skills, gender, location, profile_pic, datetime.now()))

        # Commit the transaction
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Flash success message
        flash('Thank you for registering! Your profile has been created.', 'success')

        # Redirect to the registration page again
        return redirect(url_for('register_maid'))

    return render_template('maid.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    show_login = False  # Default: Hide login popup

    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()

        if user_type == 'customer':
            cur.execute('SELECT * FROM customers WHERE email = %s', (email,))
            customer = cur.fetchone()
            if customer and checkpw(password.encode('utf-8'), customer[4].encode('utf-8')):  
                session['user_id'] = customer[0]  
                session['user_name'] = customer[1]  
                session['email'] = customer[3]  
                session['user_role'] = 'Customer'  
                flash(f'Login successful as {session["user_role"]}!', 'success')  
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Wrong password entered for Customer.', 'danger')
                show_login = True  # Keep popup open

        elif user_type == 'maid':
            cur.execute('SELECT * FROM maids WHERE email = %s', (email,))
            maid = cur.fetchone()
            if maid and checkpw(password.encode('utf-8'), maid[4].encode('utf-8')):  
                session['user_id'] = maid[0]  
                session['user_name'] = maid[1]  
                session['email'] = maid[3]  
                session['user_role'] = 'Maid'  
                flash(f'Login successful as {session["user_role"]}!', 'success')  
                return redirect(url_for('maid_dashboard'))
            else:
                flash('Wrong password entered for Maid.', 'danger')
                show_login = True  # Keep popup open

        cur.close()

    return render_template('index.html', show_login=show_login)  # Pass show_login to template

@app.route('/loginHindi', methods=['GET', 'POST'])
def loginhindi():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()

        if user_type == 'customer':
            cur.execute('SELECT * FROM customers WHERE email = %s', (email,))
            customer = cur.fetchone()
            if customer and checkpw(password.encode('utf-8'), customer[4].encode('utf-8')):  # Check hashed password
                session['user_id'] = customer[0]  # Store user id in session
                session['user_name'] = customer[1]  # Store user name in session
                session['phone_no'] = customer[2]
                session['email'] = customer[3]
                session['location'] = customer[5]
                
                session['user_role'] = 'Customer'  # Store role in session
                flash(f'Login successful as {session["user_role"]}!', 'success')  # Flash message
                return redirect(url_for('customer_dashboard'))  # Redirect to customer dashboard
            else:
                flash('Wrong password entered for Customer.', 'danger')
                return redirect(url_for('login'))

        elif user_type == 'maid':
            cur.execute('SELECT * FROM maids WHERE email = %s', (email,))
            maid = cur.fetchone()
            if maid and checkpw(password.encode('utf-8'), maid[4].encode('utf-8')):  # Check hashed password
                session['user_id'] = maid[0]  # Store maid id in session
                session['user_name'] = maid[1]  # Store maid name in session
                session['phone_no'] = maid[2]  # Store maid phone in session
                session['email'] = maid[3]  # Store maid email in session
                session['aadhar'] = maid[5]  # Store maid aadhar in session
                session['address'] = maid[6]  # Store maid address in session
                session['food_preference'] = maid[7]  # Store food_preference  in session
                session['skills'] = maid[8]  
                session['gender'] = maid[9]  
                session['location'] = maid[10] 
                session['registration_datetime'] = maid[12] 

                session['user_role'] = 'Maid'  # Store role in session
                flash(f'Login successful as {session["user_role"]}!', 'success')  # Flash message
                return redirect(url_for('maid_dashboard'))  # Redirect to maid dashboard
            else:
                flash('Wrong password entered for Maid.', 'danger')
                return redirect(url_for('login'))

        cur.close()
    return render_template('loginHindi.html')

@app.route('/customers_dashboard')
def customer_dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_name = session.get('user_name')  # Get user name from session
    phone_no = session.get('phone_no')
    email = session.get('email')
    location = session.get('location')

    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name, food_preference, skills, location, gender FROM maids')
    maids = cur.fetchall()

     # Fetch booking history based on the logged-in user's phone number
    cur.execute('''
     SELECT maid_name, booking_date, address, address, phone
        FROM bookings
        WHERE phone = %s

    ''', (phone_no,))
    bookings = cur.fetchall()

    
    return render_template('customers_dashboard.html', user_name=user_name,phone_no=phone_no,email = email,location = location,maids=maids, bookings=bookings)

@app.route('/maid_dashboard')
def maid_dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    user_name = session.get('user_name')  # Get user name from session
    phone_no = session.get('phone_no')
    email = session.get('email')
    aadhar = session.get('aadhar')
    address = session.get('address')
    food_preference = session.get('food_preference')
    skills = session.get('skills')
    gender = session.get('gender')
    location = session.get('location')
    registration_datetime = session.get('registration_datetime')
    
    cur = mysql.connection.cursor()
    cur.execute('''
     SELECT id,customer_name , address , phone , maid_id , maid_name , user_name , booking_date
        FROM bookings
        WHERE maid_name = %s
                
    ''', (phone_no,))
    bookings = cur.fetchall()

     

    return render_template('maids_dashboard.html',user_id= user_id ,user_name=user_name,phone_no=phone_no,email=email,aadhar=aadhar,address=address,
food_preference=food_preference,skills=skills,gender=gender,location=location,registration_datetime=registration_datetime,bookings=bookings)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/about_us.html')
def about_us():
    # You can add additional data here if needed
    return render_template('about_us.html')

@app.route('/reviews.html', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        rating = request.form['rating']
        comment = request.form['comment']
        
        # Validate data (optional)
        if not rating or not comment:
            flash('Please provide both a rating and a comment.', 'danger')
            return redirect(url_for('review'))
        
        # Optional: Convert rating to an integer and validate range
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash('Rating should be between 1 and 5.', 'danger')
                return redirect(url_for('review'))
        except ValueError:
            flash('Invalid rating. Please provide a valid number.', 'danger')
            return redirect(url_for('review'))

        # Connect to the database and insert the review
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO reviews (name,rating, comment) VALUES (%s,%s, %s)", (name,rating, comment))
        mysql.connection.commit()
        cursor.close()
        
        # Flash the success message
        flash('Review Submitted. Thank you for your feedback!', 'success')
        return redirect(url_for('review'))  # Redirect to the same review page to see the result

    # If it's a GET request, render the review form
    return render_template('reviews.html')


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Basic validation for required fields
        if not name or not email or not phone or not message:
            flash("Please fill in all fields.", 'danger')
            return redirect(url_for('contact'))

        # Insert the contact form data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''
        INSERT INTO contact_form (name, email, phone, message)
        VALUES (%s, %s, %s, %s)
        ''', (name, email, phone, message))

        # Commit the transaction
        mysql.connection.commit()

        # Send the form data via email (optional)
        try:
            msg = Message(
                'New Contact Form Submission',
                sender=email,
                recipients=['rajkumar777788889999000@gmail.com']  # Replace with the recipient email
            )
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            mail.send(msg)

            # Show success flash message
            flash("Your message has been received. We will get back to you as soon as possible.", 'success')
        except Exception as e:
            flash(f"An error occurred while sending your message. Please try again later. Error: {str(e)}", 'danger')

        # Redirect to the contact page after form submission
        return redirect(url_for('contact'))

    # If GET request, render the contact form page
    return render_template('contact.html')

maids = [
    {'maid_id': 1, 'maid_name': 'Priyanka Sharma', 'maid_skills': 'Cleaning, Cooking, Child Care'},
    {'maid_id': 2, 'maid_name': 'Anita Desai', 'maid_skills': 'Cleaning, Elder Care'},
    # Add other maids as needed
]
# Route to display the booking form
@app.route('/book_maid/<int:maid_id>', methods=['GET'])
def book_maid(maid_id):
    maid = next((maid for maid in maids if maid['maid_id'] == maid_id), None)
    if maid:
        return render_template('booking_form.html', maid_id=maid['maid_id'], maid_name=maid['maid_name'])
    return "Maid not found", 404
'''
# Route to handle the form submission
@app.route('/booking_form', methods=['POST'])
def booking_form():
    customer_name = request.form['customer_name']
    address = request.form['address']
    phone = request.form['phone']
    maid_id = request.form['maid_id']
    maid_name = request.form['maid_name']

    # Save booking to the database (simulated here with a flash message)
    flash(f"Booking confirmed for {customer_name}. Maid {maid_name} will assist you soon!")

    return redirect(url_for('confirm_booking', customer_name=customer_name, maid_name=maid_name))

'''
@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    customer_name = request.form['customer_name']
    address = request.form['address']
    phone = request.form['phone']
    maid_id = request.form['maid_id']
    maid_name = request.form['maid_name']
    user_name = session.get('user_name')  # Get user name from session
    
    # OTP generation (fixed OTP in this case)
    otp = "1234"  # Fixed OTP

    # Save booking to the database (simulated here with a flash message)
    cursor = mysql.connection.cursor()
    cursor.execute( 
        """
        INSERT INTO bookings (customer_name, address, phone, maid_id, maid_name, user_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_name, address, phone, maid_id, maid_name, user_name)
    )
    mysql.connection.commit()

    # Send OTP email to the user
    message = Message(
        subject="Booking Confirmation with OTP via MaidEase ",
        sender="rajkumar777788889999000@gmail.com",  
        recipients=[session.get('email')],  # Assuming the user's email is stored in session
        body=f"Thank you for booking with MaidEase. Your booking is confirmed. Your OTP is: {otp}"
    )
    
    try:
        mail.send(message)
        flash("Booking confirmed! An OTP has been sent to your email.")
    except Exception as e:
        flash(f"Error sending OTP email: {e}")

    # Redirect to a confirmation page
    return redirect(url_for('confirm_booking', user_name=user_name, customer_name=customer_name, maid_name=maid_name))


# Route to show booking confirmation
@app.route('/confirm_booking.html')
def confirm_booking():
    user_name = session.get('user_name')
    customer_name = request.args.get('customer_name')
    maid_name = request.args.get('maid_name')
    return render_template('confirm_booking.html',user_name=user_name,customer_name=customer_name, maid_name=maid_name)

@app.route('/privacyPolicy.html')
def privacyPolicy():
    return render_template('privacyPolicy.html')

@app.route('/TermsOfServices.html')
def TermsOfServices():
    return render_template('TermsOfServices.html')

@app.route('/tearmsAndConditionCustomer.html')
def tearmsAndConditionCustomer():
    return render_template('tearmsAndConditionCustomer.html')

@app.route('/tearmsAndConditionMaid.html')
def tearmsAndConditionMaid():
    return render_template('tearmsAndConditionMaid.html')

@app.route('/services.html')
def Services():
    return render_template('services.html')


@app.route('/adminDashboard')
def adminDashboard():
    # Fetch admin details from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, designation, dob, phone, email FROM admins WHERE id = 1")
    admin_data = cur.fetchone()  # Assuming there's only one admin with id = 1
    
    # Extract the data
    admin_name = admin_data[0]
    admin_designation = admin_data[1]
    admin_dob = admin_data[2]
    admin_phone = admin_data[3]
    admin_email = admin_data[4]
    
    # Fetching customer and maid data
    cur.execute("SELECT id, name, email, phone_no, location FROM customers")
    customers = cur.fetchall()

    cur.execute("SELECT id, name, email, phone_no, location, skills FROM maids")
    maids = cur.fetchall()
    
    # Query to get booking details (add your actual table name and structure)
    cur.execute('''SELECT id, customer_name , address, phone , maid_id, maid_name, user_name, booking_date FROM bookings''')
    bookings = cur.fetchall()

    # Fetching the count of customers, maids, and bookings for the pie chart
    cur.execute("SELECT COUNT(*) FROM customers")
    customer_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM maids")
    maid_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM bookings")
    booking_count = cur.fetchone()[0]
    
    # Pass the data to the template
    return render_template('adminDashboard.html', 
                           admin_name=admin_name,
                           admin_designation=admin_designation,
                           admin_dob=admin_dob,
                           admin_phone=admin_phone,
                           admin_email=admin_email,
                           customers=customers,
                           maids=maids,
                           bookings=bookings,
                           customer_count=customer_count,
                           maid_count=maid_count,
                           booking_count=booking_count)




# WebSocket event for real-time notifications (done by tanay )
@socketio.on('booking_confirmed')
def handle_booking(data):
    """Emit real-time booking notification."""
    SocketIO.emit('notification', {'message': f"Booking confirmed for {data['customer_name']} with {data['maid_name']}!"})

@SocketIO.on('booking_canceled')
def handle_cancellation(data):
    """Emit real-time cancellation notification."""
    SocketIO.emit('notification', {'message': f"Booking for {data['customer_name']} with {data['maid_name']} has been canceled."})

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    """Handles booking submission and sends a real-time notification."""
    customer_name = request.form['customer_name']
    address = request.form['address']
    phone = request.form['phone']
    maid_id = request.form['maid_id']
    maid_name = request.form['maid_name']
    user_name = session.get('user_name')

    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO bookings (customer_name, address, phone, maid_id, maid_name, user_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (customer_name, address, phone, maid_id, maid_name, user_name),
    )
    mysql.connection.commit()

    # Send real-time notification via WebSockets
    SocketIO.emit('notification', {'message': f"Booking confirmed for {customer_name} with {maid_name}!"})

    flash(f"Booking confirmed for {customer_name}. Maid {maid_name} will assist you soon!")
    return redirect(url_for('customer_dashboard'))

@app.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    """Handles booking cancellation and sends a real-time notification."""
    booking_id = request.form['booking_id']
    customer_name = request.form['customer_name']
    maid_name = request.form['maid_name']

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    mysql.connection.commit()

    # Send real-time cancellation notification via WebSockets
    SocketIO.emit('notification', {'message': f"Booking for {customer_name} with {maid_name} has been canceled."})

    flash(f"Booking for {customer_name} with {maid_name} has been canceled!")
    return redirect(url_for('customer_dashboard'))

#for receving real time notifications we will use socket-io 

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
