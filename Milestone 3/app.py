import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from dotenv import load_dotenv
import database
from auth import auth_bp  # Import your new authentication module

# Optional: If you want to keep the Hugging Face generation in this file
# from prompt_builder import build_prompt
# from model_api import query_model

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('JWT_SECRET', 'super-secret-development-key')

# Initialize SQLite database
database.init_db()

# Plug in all the routes from auth.py!
app.register_blueprint(auth_bp)

@app.route('/dashboard')
def dashboard():
    # Strict route protection: Only allow users who passed the OTP verification
    if 'user_email' not in session:
        return redirect(url_for('auth.index'))
    return render_template('dashboard.html', email=session['user_email'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
