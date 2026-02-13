Milestone 1: Fitness Profile & BMI Generator
🎯 Objective

The primary goal of this milestone was to design and develop a user-friendly fitness profile application using Streamlit.

The application allows users to:

Enter their personal health details

Automatically calculate their Body Mass Index (BMI)

Understand their health classification based on standard BMI ranges

This milestone focuses on front-end development, mathematical logic implementation, and cloud deployment.

🧮 Understanding the BMI Formula

Body Mass Index (BMI) is a widely accepted metric used to assess whether an individual’s weight is appropriate for their height.

Step 1: Height Conversion

Since the height input is collected in centimeters, it must first be converted into meters:

Height (m) = Height (cm) ÷ 100

Step 2: BMI Calculation

BMI is calculated using the formula:

BMI = Weight (kg) ÷ (Height (m))²

Step 3: Rounding

To ensure clarity and better readability, the calculated BMI value is rounded to two decimal places.

🛠 Implementation Process
1️⃣ Form Development

A structured fitness profile form was created using Streamlit’s st.form feature.

The form collects:

Personal details (Name, Height, Weight)

Fitness goals

Equipment availability

Fitness level

This ensures organized data collection in a clean and professional layout.

2️⃣ Input Validation

To maintain data accuracy and prevent errors, validation rules were implemented:

The Name field cannot be empty.

Height and Weight must be greater than zero.

Negative or invalid values are restricted.

This improves user experience and ensures correct BMI calculation.

3️⃣ BMI Calculation Logic

Custom Python logic was written to:

Convert height from centimeters to meters

Apply the BMI formula

Round the result to two decimal places

Classify BMI into standard health categories:

Underweight

Normal

Overweight

Obese

The result is displayed clearly along with the user’s name.

4️⃣ Deployment Process

The project was prepared for cloud hosting by:

Creating a requirements.txt file

Uploading the project to GitHub

Connecting the repository to Hugging Face Spaces

Deploying the Streamlit application online

This ensures the application is publicly accessible and professionally hosted.

💻 Technologies Used
🔹 Python

Used for implementing BMI logic, validation, and overall application functionality.

🔹 Streamlit

Used to create the interactive front-end interface and handle form submission.

🔹 Hugging Face Spaces

Used as the cloud deployment platform for hosting the application.

🔹 GitHub

Used for version control, code management, and integration with Hugging Face Spaces.

📌 Outcome of Milestone 1

By completing this milestone, we successfully:

Built a functional fitness profile interface

Implemented accurate BMI calculation logic

Applied proper input validation

Classified BMI into standard categories

Deployed a working web application

This milestone establishes a strong foundation for adding advanced features such as workout recommendations, diet plans, calorie tracking, and AI-based suggestions in future phases.

Live interface:
https://huggingface.co/spaces/Shriniwas1234/fit
