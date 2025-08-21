from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from email_utils import send_estimate_email
from tracking_utils import log_submission

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Change this in production

# In-memory treatment data
treatments = {
    'Consultation': {
        'Front Tooth': {'description': 'Consultation for front tooth.', 'price': 100},
        'Premolar': {'description': 'Consultation for premolar.', 'price': 120},
        'Molar': {'description': 'Consultation for molar.', 'price': 140},
    },
    'Root Canal': {
        'Front Tooth': {'description': 'Root canal for front tooth.', 'price': 900},
        'Premolar': {'description': 'Root canal for premolar.', 'price': 1100},
        'Molar': {'description': 'Root canal for molar.', 'price': 1300},
    },
    'Retreatment/Surgery': {
        'Front Tooth': {'description': 'Retreatment/Surgery for front tooth.', 'price': 1200},
        'Premolar': {'description': 'Retreatment/Surgery for premolar.', 'price': 1400},
        'Molar': {'description': 'Retreatment/Surgery for molar.', 'price': 1600},
    },
}

ADMIN_ID = 'DoctorEC'
ADMIN_PASSWORD = 'apexsecure2024'

# Simple login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    if request.method == 'POST':
        data = request.form.to_dict()
        treatment = data.get('treatment')
        tooth = data.get('tooth')

        estimate_value = 0
        if treatment in treatments and tooth in treatments[treatment]:
            estimate_value = treatments[treatment][tooth]['price']

        # Optional Email Sending
        if data.get('send_email') == 'yes':
            send_estimate_email(data, estimate_value)

        # Always log
        log_submission(data, estimate_value)

        return render_template('success.html', name=data.get('full_name'))
    
    return render_template('estimate.html', treatments=treatments)


@app.route('/get_estimate', methods=['POST'])
def get_estimate():
    data = request.get_json()
    treatment = data.get('treatment')
    tooth = data.get('tooth')
    if treatment in treatments and tooth in treatments[treatment]:
        info = treatments[treatment][tooth]
        return jsonify({
            'treatment': treatment,
            'tooth': tooth,
            'description': info['description'],
            'price': info['price']
        })
    return jsonify({'error': 'Invalid selection'}), 400

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        # Update treatment prices
        for t_type in treatments:
            for tooth in treatments[t_type]:
                price_field = f"{t_type}_{tooth}_price"
                desc_field = f"{t_type}_{tooth}_desc"
                new_price = request.form.get(price_field)
                new_desc = request.form.get(desc_field)
                if new_price:
                    try:
                        treatments[t_type][tooth]['price'] = int(new_price)
                    except ValueError:
                        pass
                if new_desc:
                    treatments[t_type][tooth]['description'] = new_desc
        flash('Treatment prices updated!', 'success')
    return render_template('admin_dashboard.html', treatments=treatments)

@app.route('/admin/logout')
@login_required
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 