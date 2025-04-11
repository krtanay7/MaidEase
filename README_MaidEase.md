
# MaidEase

**MaidEase** is a web-based maid booking application that connects customers with domestic help. It aims to empower women by improving access to employment opportunities through a simple, efficient, and secure digital platform.

## GitHub Repository
**Project Title:** `MAIDEASE`

## Features

- Customer and Maid registration with role-based login
- View available maids and book services
- Booking history and dashboard for customers and maids
- Secure password handling using bcrypt
- Admin panel to manage users and bookings
- Payment integration with Razorpay
- Email notifications using SMTP (Flask-Mail)
- Multilingual support (Hindi, Bengali, Gujarati)
- Review and feedback system
- Contact form with email alerts
- Admin-to-user chat messaging and notification system

## Tech Stack

**Frontend:**  
- HTML  
- CSS  
- JavaScript  
- Bootstrap  

**Backend:**  
- Python  
- Flask  

**Database:**  
- MySQL  

**Other Tools:**  
- Flask-Mail (SMTP for email alerts)  
- Razorpay (Payment Integration)  
- bcrypt (Secure password hashing)

## Installation

1. Clone the Repository
   ```bash
   git clone https://github.com/krtanay7/MaidEase
   cd maidApp
   ```

2. Set up Python environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux/macOS
   venv\Scripts\activate   # for Windows
   pip install -r requirements.txt
   ```

3. Configure MySQL and Flask-Mail
   - Update `app.config` in `app.py` with your MySQL credentials and email settings.

4. Run the Application
   ```bash
   python app.py
   ```

5. Access in Browser
   - Visit: `http://127.0.0.1:5000/`

## Folder Structure (Sample)

```
maidApp/
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── customer.html
│   ├── maid.html
│   ├── adminDashboard.html
│   └── ...other HTML templates
│
├── static/
│   └── ...CSS, JS, Images
│
├── app.py
└── README.md
```

## Project Purpose

This project serves both as a social initiative and a technical learning exercise. It focuses on applying full-stack development skills to solve a real-world problem, promoting women employment and service accessibility in urban areas.
