from flask import Flask, render_template, request, redirect, session, url_for, send_file, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# =======================
# Homepage
# =======================
@app.route('/')
def home():
    return render_template('index.html')


# =======================
# Service Registration
# =======================
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    service = request.form['service']

    # Save to CSV
    with open('customers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, phone, service])

    return render_template('success.html', name=name)


# =======================
# About and Contact
# =======================
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# =======================
# Admin Login
# =======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin_user = request.form['username']
        admin_pass = request.form['password']
        if admin_user == 'admin' and admin_pass == 'admin':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            flash('Invalid login credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/login')


# =======================
# Admin Dashboard
# =======================
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    customers = []
    service_counts = {}

    if os.path.exists('customers.csv'):
        with open('customers.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    customers.append(row)
                    service = row[3]
                    service_counts[service] = service_counts.get(service, 0) + 1

    total_customers = len(customers)

    return render_template(
        'admin.html',
        customers=customers,
        total=total_customers,
        counts=service_counts,
        total_customers=total_customers,
        service_counts=service_counts
    )


# =======================
# Download CSV
# =======================
@app.route('/download')
def download_csv():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    return send_file('customers.csv', as_attachment=True)


# =======================
# Run the app
# =======================
if __name__ == '__main__':
    app.run(debug=True)
