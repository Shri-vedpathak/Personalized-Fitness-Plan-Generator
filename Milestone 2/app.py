import streamlit as st
from model_api import query_model

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="FitPlan AI 💪",
    page_icon="🏋️",
    layout="wide"
)

# ---------------- SESSION STATE INIT ---------------- #
# This manages the "pages" in our single-page app
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- INTERACTIVE BACKGROUND CSS ---------------- #
st.markdown("""
<style>
/* Background Image Setup */
[data-testid="stAppViewContainer"] {
    background-image: url("https://t3.ftcdn.net/jpg/01/19/59/74/360_F_119597487_SnvLBdheEGOxu05rMQ5tCzo250cRrTz9.jpg"); /* Replace with your image link */
    background-size: cover;          /* Makes sure the image covers the whole screen */
    background-position: center;     /* Centers the image */
    background-repeat: no-repeat;    /* Prevents the image from tiling */
    background-attachment: fixed;    /* Keeps the background still when scrolling */
}
/* Glassmorphism Main Card (Keeping your existing card style!) */
.main-card {
    background: rgba(0, 0, 0, 0.75); /* Slightly darker so text is readable over the image */
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 25px rgba(0, 255, 100, 0.3);
    color: white;
}
/* ... rest of your CSS ... */
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

# ==========================================
#                 PAGE 1: FORM
# ==========================================
if st.session_state.page == "form":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("💪 FitPlan AI – Personalized Fitness Plan Generator")
    st.write("Fill your fitness profile below:")

    with st.form("fitness_form"):
        st.header("1️⃣ Personal Information")
        
        # Adding columns for better layout
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            age = st.number_input("Age (15-70) *", min_value=15, max_value=70, step=1, value=25)
            height_cm = st.number_input("Height (cm) *", min_value=0.0, step=0.1)
        with col2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
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

        submit = st.form_submit_button("🚀 Submit")

    # Form Validation & Logic
    if submit:
        if name.strip() == "":
            st.error("⚠ Name is required.")
        elif height_cm <= 0 or weight_kg <= 0:
            st.error("⚠ Valid height and weight are required.")
        else:
            # BMI Logic
            height_m = height_cm / 100
            bmi = round(weight_kg / (height_m ** 2), 2)
            
            # Determine Category
            if bmi < 18.5: category, color = "Underweight", "blue"
            elif 18.5 <= bmi < 24.9: category, color = "Normal", "green"
            elif 25 <= bmi < 29.9: category, color = "Overweight", "orange"
            else: category, color = "Obese", "red"

            # 1. Construct the AI Prompt (now includes age and gender)
            equipment_str = ", ".join(equipment) if equipment else "No equipment (bodyweight only)"
            
            ai_prompt = f"""
            Generate a professional 5-day workout routine for {name}.
            
            USER PROFILE:
            - Age: {age}, Gender: {gender}
            - Goal: {goal}
            - Fitness Level: {level}
            - BMI: {bmi} ({category})
            - Available Equipment: {equipment_str}
            
            REQUIREMENTS:
            1. Provide a table or clear list for each day.
            2. Include Warm-up and Cool-down for every session.
            3. Specify Exercises, Sets, Reps, and Rest Times.
            4. Adjust the intensity specifically for a {level} level and {category} BMI.
            5. Add 3 brief nutrition tips to help with the {goal} goal.
            """

            # 2. Call the Model
            with st.spinner("🏋️ AI Trainer is crafting your plan..."):
                workout_plan = query_model(ai_prompt)

            # 3. Save everything to session state to show on the next page
            st.session_state.name = name
            st.session_state.bmi = bmi
            st.session_state.category = category
            st.session_state.color = color
            st.session_state.workout_plan = workout_plan
            
            # 4. Change page state and trigger a rerun
            st.session_state.page = "results"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
#               PAGE 2: RESULTS
# ==========================================
elif st.session_state.page == "results":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Back button to return to the form
    if st.button("⬅️ Back to Form"):
        st.session_state.page = "form"
        st.rerun()

    st.success(f"Hello {st.session_state.name}! Your profile is ready.")
    
    col1, col2 = st.columns(2)
    col1.metric("Your BMI", st.session_state.bmi)
    col2.markdown(f"### Category: :{st.session_state.color}[{st.session_state.category}]")
    
    st.divider()

    st.subheader("🗓 Your Personalized 5-Day Workout Plan")
    st.markdown(st.session_state.workout_plan)

    st.markdown('</div>', unsafe_allow_html=True)
