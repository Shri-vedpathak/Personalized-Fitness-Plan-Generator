import random
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import database
from email_utils import send_otp_email

# Create the blueprint
auth_bp = Blueprint('auth', __name__)

# Temporary storage for OTPs
login_otp_storage = {}
reset_otp_storage = {} # --- NEW: Added storage for password resets ---

# ==========================================
# PAGE ROUTES (HTML)
# ==========================================
@auth_bp.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@auth_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@auth_bp.route('/verify-page')
def verify_page():
    # If they haven't started logging in, kick them back to the login page
    if 'pending_email' not in session:
        return redirect(url_for('auth.index'))
    return render_template('verify_otp.html', email=session['pending_email'])

# --- RESTORED: Forgot Password Page Route ---
@auth_bp.route('/forgot-password-page')
def forgot_password_page():
    return render_template('forgot_password.html')

# ==========================================
# API ROUTES (Logic)
# ==========================================
@auth_bp.route('/register', methods=['POST'])
def register():
    """Milestone 3: Register using just Email and Password."""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    if database.add_user(name, email, password):
        return jsonify({"message": "Registration successful!"}), 201
    else:
        return jsonify({"error": "Email already registered."}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Step 1 of 2FA: Verify password, send OTP, set pending state."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if database.verify_user(email, password):
        # 1. Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        login_otp_storage[email] = otp
        
        # 2. Send the OTP email
        send_otp_email(email, otp, subject="FitPlan AI - Login Verification")
        
        # 3. Put user in a "pending" session state
        session['pending_email'] = email
        
        return jsonify({"message": "OTP sent to email", "redirect": "/verify-page"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route('/verify-login-otp', methods=['POST'])
def verify_login_otp():
    """Step 2 of 2FA: Check the OTP and grant full dashboard access."""
    data = request.json
    user_otp = data.get('otp')
    email = session.get('pending_email')

    if not email:
        return jsonify({"error": "Session expired. Please log in again."}), 400

    stored_otp = login_otp_storage.get(email)

    if stored_otp and stored_otp == user_otp:
        # Success! Clear pending state, set actual logged-in state
        session.pop('pending_email', None)
        session['user_email'] = email
        
        # Clean up storage
        del login_otp_storage[email]
        
        return jsonify({"message": "Verification successful!", "redirect": "/dashboard"}), 200
    else:
        return jsonify({"error": "Invalid or expired OTP"}), 401

@auth_bp.route('/logout')
def logout():
    session.clear() # Clears everything
    return redirect(url_for('auth.index'))

# --- RESTORED: Forgot Password Logic Routes ---
@auth_bp.route('/send-reset-otp', methods=['POST'])
def send_reset_otp():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not database.check_user_exists(email):
        return jsonify({"error": "Email not found. Please register."}), 404

    otp = str(random.randint(100000, 999999))
    reset_otp_storage[email] = otp

    # Reusing your new email_utils function!
    send_otp_email(email, otp, subject="FitPlan AI - Password Reset")
    
    return jsonify({"message": "Reset OTP sent to your email!"}), 200

@auth_bp.route('/reset-password', methods=['POST'])
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

    stored_otp = reset_otp_storage.get(email)
    if not stored_otp or stored_otp != user_otp:
        return jsonify({"error": "Invalid or expired OTP"}), 400

    database.update_password(email, new_password)
    del reset_otp_storage[email]
    
    return jsonify({"message": "Password updated successfully!"}), 200
