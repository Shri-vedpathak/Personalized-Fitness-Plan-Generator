# FitPlan AI 💪 - Milestone 2: Core AI Model Integration

### 🎯 Objective of the Milestone
The primary goal of this milestone was to transform the application from a basic BMI calculator into an intelligent fitness assistant by integrating a Large Language Model (LLM). 
The application now allows users to:
* Connect their health and fitness data to an advanced AI model.
* Receive a highly personalized, 5-day structured workout plan.
* View dynamically generated fitness and nutrition tips tailored to their specific goals.
This milestone focuses on AI model integration, prompt engineering, and secure cloud deployment.

### 🤖 Model Name Used
* **Model:** `mistralai/Mistral-7B-Instruct-v0.2`
* **Provider:** Hugging Face API (`InferenceClient`)
* **Reasoning:** Mistral-7B-Instruct is highly capable of following detailed instructions, structuring data into Markdown formats (like lists and tables), and generating human-like, professional text quickly, making it the perfect choice for acting as an AI Personal Trainer.

### 🧮 Prompt Design Explanation
To generate a highly accurate workout plan, the app communicates with the LLM using a concept called **Prompt Engineering**. The prompt was carefully designed with three core components:
1. **System Persona:** The AI is assigned a role (e.g., "world-class certified personal trainer and nutritionist") so it knows exactly what tone and expertise to apply.
2. **Dynamic Variable Injection:** User inputs collected in the form (Name, Age, Gender, BMI Category, Goal, Level, and Equipment) are dynamically injected into the text using Python `f-strings`. 
3. **Strict Constraints & Requirements:** The prompt explicitly requires the AI to output a 5-day schedule, include warm-ups/cool-downs, specify sets/reps, adjust the intensity for the user's specific BMI category, and provide 3 tailored nutrition tips.

### 🛠 Steps Performed

**1️⃣ Model Loading**
A secure connection to the Hugging Face Inference API was established using the `huggingface_hub` library. 
* The `InferenceClient` was initialized to call the Mistral-7B model.
* Authentication was handled securely using an environment variable (`HF_Token`) to ensure API keys are not hardcoded into the script.

**2️⃣ Prompt Creation**
Custom Python logic was written to format the user's form data into a structured request.
* Lists (like selected equipment) were joined into readable strings.
* The prompt was structured to explicitly tie the user's BMI category and fitness level to the requested workout intensity, ensuring safe and realistic AI generation.

**3️⃣ Inference Testing & Error Handling**
The application was rigorously tested to ensure stable performance:
* **Error Handling:** Wrapped the AI API call in a `try-except` block to gracefully handle network errors, timeouts, or missing tokens using `st.error`.
* **Scenario Testing:** Tested the model with various profiles (e.g., an overweight beginner with no equipment vs. a normal-weight advanced user with a full gym) to verify that the AI dynamically adapted its workout recommendations.
* **UI Integration:** Utilized Streamlit's `st.session_state` and `st.spinner()` to create a seamless loading experience while the model processes the inference.

### 📄 Sample Generated Outputs

**Input Profile:** * **Name:** Sarah | **Age:** 28 | **Gender:** Female 
* **BMI:** 27.5 (Overweight) | **Goal:** Weight Loss | **Level:** Beginner | **Equipment:** No Equipment

**AI Output Extract:**
> ### 🗓 Your 5-Day Workout Plan
> **Warm-up (Daily):** 5 minutes of light marching in place, arm circles, and dynamic stretches.
> 
> **Day 1: Full Body Low-Impact Cardio**
> * Modified Jumping Jacks (Step Jacks): 3 sets of 15 reps (60 sec rest)
> * Bodyweight Squats (to a chair): 3 sets of 10 reps (60 sec rest)
> * Incline Push-ups (against a wall): 3 sets of 10 reps (60 sec rest)
> 
> **Day 2: Core & Mobility**
> * Seated Knee Tucks: 3 sets of 12 reps (60 sec rest)
> * Bird-Dog: 3 sets of 10 reps per side (60 sec rest)
> * Plank from Knees: 3 sets of 20 seconds (60 sec rest)
>
> *(...Days 3, 4, 5 and Cool-down omitted for brevity...)*
> 
> **💡 Nutrition Tips for Weight Loss:**
> 1. **Caloric Deficit:** Aim to consume 300-500 calories less than your daily maintenance level for safe, steady weight loss.
> 2. **Hydration:** Drink at least 2.5 liters of water daily to support metabolism and joint health.
> 3. **Protein Focus:** Include lean protein in every meal to keep you feeling full and preserve muscle mass while losing fat.

### 🌐 Hugging Face Space Deployment Link
The project was hardened for public use, including creating a `requirements.txt` file and configuring the `HF_Token` in the Hugging Face Spaces "Secrets" settings.

🔗 **Live Application:** [(https://huggingface.co/spaces/Shriniwas1234/fit_1)]
