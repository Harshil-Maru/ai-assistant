from flask import Flask, request, render_template
import google.generativeai as genai
import os

# --- SETUP ---
# This tells Flask to look for the 'index.html' file in the current directory (.)
# instead of a 'templates' subfolder.
app = Flask(__name__, template_folder='.')

# --- SECURITY BEST PRACTICE ---
# Load the API key from an environment variable for security.
# On your deployment server, you will set an environment variable named 'GOOGLE_API_KEY'.
GOOGLE_API_KEY = os.environ.get("AIzaSyCSrHhPeT2X5G9_d-ptfPwRIwY6ACuluTM")

# Check if the API key was found. If not, the app will stop with an error.
if not GOOGLE_API_KEY:
    raise ValueError("API Key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure the generative AI model with the key.
genai.configure(api_key=GOOGLE_API_KEY)


# --- CORE AI FUNCTION ---
def get_ai_response(prompt_text):
    """
    Sends a prompt to the Gemini API and returns the generated text.
    Includes error handling for API issues.
    """
    try:
        # Initialize the specific Gemini model you want to use.
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Generate content based on the provided prompt.
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        # If there's an error with the API call, return a user-friendly error message.
        print(f"An API error occurred: {e}")
        return "Sorry, there was an error communicating with the AI. Please check the server logs."


# --- WEB ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles both displaying the page (GET) and processing the form (POST).
    """
    response_text = None # Initialize response as empty.

    # This block runs only when the user submits the form.
    if request.method == 'POST':
        # Get the data submitted in the form fields.
        task = request.form['task']
        user_input = request.form['user_input']

        # Build a clear and specific prompt for the AI based on the selected task.
        if task == 'question':
            prompt = f"Please answer the following question: {user_input}"
        elif task == 'summarize':
            prompt = f"Please provide a concise summary of the following text: {user_input}"
        elif task == 'creative':
            prompt = f"Write a short, creative piece inspired by this topic: {user_input}"
        else:
            # A fallback just in case.
            prompt = user_input

        # Call the AI function with the constructed prompt to get the response.
        response_text = get_ai_response(prompt)

    # Render the HTML page.
    # The 'response' variable in index.html will be filled with the value of 'response_text'.
    return render_template('index.html', response=response_text)


# --- RUN THE APP ---
# This part of the script only runs when you execute 'python app.py' directly.
# A production server like Gunicorn will run the 'app' object directly without this.
if __name__ == '__main__':
    # debug=True automatically reloads the server when you save changes.
    # Do not use debug=True in a production environment.
    app.run(debug=True)
