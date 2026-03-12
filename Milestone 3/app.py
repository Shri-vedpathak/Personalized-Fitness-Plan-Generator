import os
import random
import threading
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import database
# --- ADD THESE IMPORTS AT THE VERY TOP OF app.py ---
from prompt_builder import build_prompt
from model_api import query_model

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('JWT_SECRET', 'super-secret-development-key') # Secures user sessions

database.init_db()

otp_storage = {}

def send_async_email(message):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        print("Background email sent successfully!")
    except Exception as e:
        print(f"Background email failed: {e}")

# ==========================================
# PAGE ROUTES (Serving HTML)
# ==========================================

@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/forgot-password-page')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', email=session['user_email'])

# ==========================================
# API ROUTES (Handling Logic)
# ==========================================

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if database.verify_user(email, password):
        session['user_email'] = email
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if database.check_user_exists(email):
        return jsonify({"error": "Email is already registered. Please log in."}), 400

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    message = Mail(
        from_email=os.environ.get('EMAIL_FROM'),
        to_emails=email,
        subject='Your Registration OTP',
        html_content=f'<strong>Your OTP for registration is: {otp}</strong>')
    
    threading.Thread(target=send_async_email, args=(message,)).start()
    return jsonify({"message": "OTP is on its way!"}), 200

@app.route('/send-reset-otp', methods=['POST'])
def send_reset_otp():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not database.check_user_exists(email):
        return jsonify({"error": "Email not found. Please register."}), 404

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    message = Mail(
        from_email=os.environ.get('EMAIL_FROM'),
        to_emails=email,
        subject='Your Password Reset OTP',
        html_content=f'<strong>Your OTP to reset your password is: {otp}</strong>')
    
    threading.Thread(target=send_async_email, args=(message,)).start()
    return jsonify({"message": "Reset OTP sent to your email!"}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    user_otp = data.get('otp')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([name, email, user_otp, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    stored_otp = otp_storage.get(email)
    if not stored_otp or stored_otp != user_otp:
        return jsonify({"error": "Invalid or expired OTP"}), 400

    success = database.add_user(name, email, password)
    if success:
        del otp_storage[email]
        return jsonify({"message": "Registration successful!"}), 201
    else:
        return jsonify({"error": "Email already registered."}), 400

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')
    new_password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([email, user_otp, new_password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400
    if new_password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    stored_otp = otp_storage.get(email)
    if not stored_otp or stored_otp != user_otp:
        return jsonify({"error": "Invalid or expired OTP"}), 400

    database.update_password(email, new_password)
    del otp_storage[email]
    
    return jsonify({"message": "Password updated successfully!"}), 200

# ... (Keep all your existing routes for login, register, etc.) ...

# --- PASTE THIS NEW ROUTE AT THE BOTTOM ---
@app.route('/generate-workout', methods=['POST'])
def generate_workout():
    if 'user_email' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    
    # Extract data from the frontend form
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    date = data.get('date')
    height = float(data.get('height'))
    weight = float(data.get('weight'))
    goal = data.get('goal')
    equipment = data.get('equipment') # This will be a list
    fitness_level = data.get('level')

    # Build the prompt and get BMI info
    prompt, bmi, category, color = build_prompt(
        name, age, gender, date, height, weight, goal, fitness_level, equipment
    )

    # Call Hugging Face API
    workout_plan = query_model(prompt)

    # Return the results to the frontend
    return jsonify({
        "bmi": round(bmi, 2),
        "category": category,
        "color": color,
        "workout_plan": workout_plan
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
