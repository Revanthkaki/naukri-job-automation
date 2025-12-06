import google.generativeai as genai

def generate_ai_answer(question, api_key):
    """Generate AI answers using Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"You are helping someone answer a job application question professionally. Question: {question}. Provide a professional answer in 2-3 sentences."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"AI answer generation failed: {e}")
        return "I am very interested in this position and believe my skills align well with the requirements."
