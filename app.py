from flask import Flask, request, render_template
import google.generativeai as genai
import os

# --- SETUP ---
# This tells Flask to look for the 'index.html' file in the current directory (.)
app = Flask(__name__, template_folder='.')

# --- SECURITY BEST PRACTICE ---
# Load the API key from an environment variable. This is CRITICAL for deployment.
GOOGLE_API_KEY = os.environ.get("AIzaSyCSrHhPeT2X5G9_d-ptfPwRIwY6ACuluTM")

# This check is what causes the crash if the environment variable is not set on Vercel.
if not GOOGLE_API_KEY:
    # This error message will appear in your Vercel logs.
    raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY environment variable is not set.")

# Configure the generative AI model with the key.
genai.configure(api_key=GOOGLE_API_KEY)


# --- CORE AI FUNCTION ---
def get_ai_response(prompt_text):
    """
    Sends a prompt to the Gemini API and returns the generated text.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"An API error occurred: {e}")
        return "Sorry, there was an error communicating with the AI. Please check the server logs."


# --- WEB ROUTES for VERCEL ---
# This single function will now handle all requests sent to the app.
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    """
    This function catches all requests and handles the form logic.
    It's the entry point for the Vercel serverless function.
    """
    response_text = None

    if request.method == 'POST':
        try:
            task = request.form['task']
            user_input = request.form['user_input']

            if task == 'question':
                prompt = f"Please answer the following question: {user_input}"
            elif task == 'summarize':
                prompt = f"Please provide a concise summary of the following text: {user_input}"
            elif task == 'creative':
                prompt = f"Write a short, creative piece inspired by this topic: {user_input}"
            else:
                prompt = user_input

            response_text = get_ai_response(prompt)
        except Exception as e:
            print(f"Form processing error: {e}")
            response_text = "An error occurred while processing the form."

    # For both GET and POST requests, it renders the same HTML page.
    # If it was a POST, 'response_text' will have a value. If GET, it will be None.
    return render_template('index.html', response=response_text)

# The __main__ block is for local testing and is ignored by Vercel.
if __name__ == '__main__':
    app.run(debug=True)
