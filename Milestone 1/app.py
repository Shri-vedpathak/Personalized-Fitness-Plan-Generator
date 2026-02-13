import streamlit as st

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="FitPlan AI 💪",
    page_icon="🏋️",
    layout="wide"
)

# ---------------- INTERACTIVE BACKGROUND CSS ---------------- #
st.markdown("""
<style>
/* Animated Gradient Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #1e3a8a, #065f46, #0f172a);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
/* Glassmorphism Main Card */
.main-card {
    background: rgba(0, 0, 0, 0.65);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 25px rgba(0, 255, 100, 0.3);
}
/* Headings */
h1, h2, h3 {
    color: #22c55e;
}
/* Button Styling */
.stButton>button {
    background-color: #22c55e;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: #0f172a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("📌 About FitPlan AI")

st.sidebar.info("""
FitPlan AI helps users:
✔ Calculate BMI  
✔ Understand health category  
✔ Track fitness goals  
✔ Improve lifestyle  
""")

st.sidebar.subheader("📊 BMI Categories")

st.sidebar.write("""
- **Underweight** : BMI < 18.5  
- **Normal** : 18.5 – 24.9  
- **Overweight** : 25 – 29.9  
- **Obese** : BMI ≥ 30  
""")

st.sidebar.subheader("💡 Fitness Tips")

st.sidebar.write("""
- Stay hydrated 💧  
- Exercise regularly 🏋️  
- Eat balanced meals 🥗  
- Sleep 7–8 hours 😴  
- Track progress weekly 📈  
""")

# ---------------- MAIN CARD ---------------- #
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.title("💪 FitPlan AI – Personalized Fitness Plan Generator")

st.write("Fill your fitness profile below:")

# ---------------- FORM ---------------- #
with st.form("fitness_form"):

    st.header("1️⃣ Personal Information")

    name = st.text_input("Name *")
    height_cm = st.number_input("Height (cm) *", min_value=0.0, step=0.1)
    weight_kg = st.number_input("Weight (kg) *", min_value=0.0, step=0.1)

    st.header("2️⃣ Fitness Details")

    goal = st.selectbox(
        "Fitness Goal",
        ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"]
    )

    equipment = st.multiselect(
        "Available Equipment",
        ["Dumbbells", "Resistance Band", "Yoga Mat", "No Equipment"]
    )

    level = st.selectbox(
        "Fitness Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    submit = st.form_submit_button("🚀 Generate BMI Report")

# ---------------- VALIDATION & LOGIC ---------------- #

if submit:

    if name.strip() == "":
        st.error("⚠ Name is required.")
    elif height_cm <= 0:
        st.error("⚠ Height must be greater than 0.")
    elif weight_kg <= 0:
        st.error("⚠ Weight must be greater than 0.")
    else:

        # Convert cm to meters
        height_m = height_cm / 100

        # BMI Calculation
        bmi = weight_kg / (height_m ** 2)
        bmi = round(bmi, 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
            color = "green"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        # Display Results
        st.success(f"Hello {name} 👋")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Your BMI", bmi)

        with col2:
            st.markdown(f"### BMI Category: :{color}[{category}]")

        st.write("---")
        st.write("🎯 **Fitness Goal:**", goal)
        st.write("🏋️ **Fitness Level:**", level)
        st.write("🛠 **Equipment Selected:**", ", ".join(equipment) if equipment else "None")

st.markdown('</div>', unsafe_allow_html=True)
