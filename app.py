from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = '1FN4kDmHz1XNGLq2LtQ7jIaNMwapvfihg0CRIBJg9a4'

# Database Connection
def get_db_connection():
    conn = sqlite3.connect('sqlitecloud://ck0ta6vohz.g3.sqlite.cloud:8860/gastos?apikey=1FN4kDmHz1XNGLq2LtQ7jIaNMwapvfihg0CRIBJg9a4')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (this will run only the first time)
init_db()

# Home Route
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Login System
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# User Management
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    phone = request.form['phone']
    cost = request.form['cost']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, age, contact, phone, cost) VALUES (?, ?, ?, ?, ?)',
                 (name, age, contact, phone, cost))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    phone = request.form['phone']
    cost = request.form['cost']
    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ?, age = ?, contact = ?, phone = ?, cost = ? WHERE id = ?',
                 (name, age, contact, phone, cost, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

# Service Management
@app.route('/services')
def services():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    return render_template('services.html', services=services)

@app.route('/add_service', methods=['POST'])
def add_service():
    name = request.form['name']
    cost = request.form['cost']
    conn = get_db_connection()
    conn.execute('INSERT INTO services (name, cost) VALUES (?, ?)', (name, cost))
    conn.commit()
    conn.close()
    return redirect(url_for('services'))

@app.route('/edit_service/<int:service_id>', methods=['POST'])
def edit_service(service_id):
    name = request.form['name']
    cost = request.form['cost']
    conn = get_db_connection()
    conn.execute('UPDATE services SET name = ?, cost = ? WHERE id = ?', (name, cost, service_id))
    conn.commit()
    conn.close()
    return redirect(url_for('services'))

@app.route('/delete_service/<int:service_id>')
def delete_service(service_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM services WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('services'))

# Expense Management
@app.route('/expenses')
def expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    item = request.form['item']
    amount = request.form['amount']
    conn = get_db_connection()
    conn.execute('INSERT INTO expenses (item, amount) VALUES (?, ?)', (item, amount))
    conn.commit()
    conn.close()
    return redirect(url_for('expenses'))

@app.route('/expense_report', methods=['GET'])
def expense_report():
    # Get the report type (month or year) from query parameters
    report_type = request.args.get('report_type', 'monthly')  # default to 'monthly'

    # Generate SQL query based on the report type
    if report_type == 'monthly':
        query = """
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total_expenses
        FROM expenses
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month DESC
        """
    elif report_type == 'yearly':
        query = """
        SELECT strftime('%Y', date) as year, SUM(amount) as total_expenses
        FROM expenses
        GROUP BY strftime('%Y', date)
        ORDER BY year DESC
        """
    else:
        return "Invalid report type", 400

    # Execute query and fetch results
    conn = get_db_connection()
    report_data = conn.execute(query).fetchall()
    conn.close()

    return render_template('expense_report.html', report_data=report_data)


# Income Management
@app.route('/income')
def income():
    conn = get_db_connection()
    income = conn.execute('SELECT * FROM income').fetchall()
    conn.close()
    return render_template('income.html', income=income)

@app.route('/add_income', methods=['POST'])
def add_income():
    user_id = request.form['user_id']
    amount = request.form['amount']
    conn = get_db_connection()
    conn.execute('INSERT INTO income (user_id, amount) VALUES (?, ?)', (user_id, amount))
    conn.commit()
    conn.close()
    return redirect(url_for('income'))

@app.route('/income_report', methods=['GET'])
def income_report():
    # Get the report type (month or year) from query parameters
    report_type = request.args.get('report_type', 'monthly')  # default to 'monthly'

    # Generate SQL query based on the report type
    if report_type == 'monthly':
        query = """
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total_income
        FROM income
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month DESC
        """
    elif report_type == 'yearly':
        query = """
        SELECT strftime('%Y', date) as year, SUM(amount) as total_income
        FROM income
        GROUP BY strftime('%Y', date)
        ORDER BY year DESC
        """
    else:
        return "Invalid report type", 400

    # Execute query and fetch results
    conn = get_db_connection()
    report_data = conn.execute(query).fetchall()
    conn.close()

    return render_template('income_report.html', report_data=report_data)

if __name__ == '__main__':
    app.run(debug=True)
