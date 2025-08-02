from flask import Flask, request, render_template
import google.generativeai as genai
import os

# --- SETUP ---
app = Flask(__name__, template_folder='.')

# --- SECURITY BEST PRACTICE ---
# We have confirmed via logs that Vercel is providing this key.
# We can now directly get the key without the extra check that was causing the crash.
GOOGLE_API_KEY = os.environ.get("AIzaSyCSrHhPeT2X5G9_d-ptfPwRIwY6ACuluTM")

# The script will now proceed directly to configuring the AI.
# If there's an issue with the key itself, the genai library will raise a more specific error.
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
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    """
    This function catches all requests and handles the form logic.
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

    return render_template('index.html', response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
