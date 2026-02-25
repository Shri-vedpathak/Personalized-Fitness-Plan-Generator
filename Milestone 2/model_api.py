from huggingface_hub import InferenceClient
import os

def query_model(prompt):
    try:
        # Ensure your HF_Token is set in your environment variables
        HF_TOKEN = os.getenv("HF_Token") 
        
        client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=HF_TOKEN
        )

        response = client.chat_completion(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a world-class certified personal trainer and nutritionist. "
                               "Your goal is to provide highly structured, scientific, and safe workout plans."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000, # Increased for a full 5-day plan
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
