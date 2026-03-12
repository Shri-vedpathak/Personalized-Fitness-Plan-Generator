# FitPlan AI - Milestone 3: Secure Authentication & OTP Verification

## 📌 Overview
This milestone introduces a robust and secure user authentication system for FitPlan AI. It ensures that users can securely create accounts, log in, and verify their identity using a dynamic One-Time Password (OTP) sent directly to their registered email before accessing their personalized fitness dashboard.

## 🚀 Features Implemented

* **User Registration (Signup):** A seamless UI allowing new users to create an account using their Email ID and a secure password.
* **Database Integration:** User credentials and profile data are securely stored and managed using a lightweight SQLite database.
* **Credential Verification (Login):** A secure login gateway that checks user-provided credentials against the stored database records.
* **Dynamic OTP Generation:** Upon a successful password match during login, the system automatically generates a secure, randomized 6-digit One-Time Password.
* **Email Dispatch:** The 6-digit OTP is instantly dispatched to the user's registered email address using the SendGrid API via background threading for zero UI lag.
* **OTP Verification Gateway:** A dedicated verification checkpoint where users must input the emailed code to proceed.
* **Protected Route Management:** The main application Dashboard is completely locked and inaccessible until the user successfully passes the OTP verification step.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite, Werkzeug (for password hashing)
* **Email Service:** SendGrid API
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (featuring a modern, responsive split-screen UI)

## ⚙️ Environment Setup

To run this authentication system locally, you will need to configure your environment variables. Create a `.env` file in the root directory and include the following:

```env
# Flask Security Key
JWT_SECRET=your_super_secret_key_here

# SendGrid Email Configuration
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
EMAIL_FROM=your_registered_sendgrid_email@example.com

# Hugging Face API (For Dashboard features)
HF_TOKEN=hf_your_hugging_face_token_here
