from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import google.generativeai as genai

app = Flask(__name__)

# ----------------------------
# 🔹 Gemini API Configuration
# ----------------------------
genai.configure(api_key="AIzaSyB02H1j5t99ETRi2zWu2AO7k1u-gqS8Yc0")  # Replace with your Gemini key
model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# 🔹 Main Routes
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/asl')
def asl():
    return render_template('ASL.html')

@app.route('/isl')
def isl():
    return render_template('ISL.html')


# ----------------------------
# 🔹 Application Launchers
# ----------------------------
@app.route('/start_asl')
def start_asl():
    subprocess.Popen(["python", "applicationA.py"])
    return "American Sign Language Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/start_isl')
def start_isl():
    subprocess.Popen(["python", "applicationI.py"])
    return "Indian Sign Language Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/keyboard')
def keyboard():
    subprocess.Popen(["python", "keyboard.py"])
    return "Virtual Keyboard Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/calculator')
def calculator():
    subprocess.Popen(["python", "calculator.py"])
    return "Virtual Calculator Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/car_game')
def car_game():
    subprocess.Popen(["python", "cargame.py"])
    return "Car Game Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/catch_ball')
def catch_ball():
    subprocess.Popen(["python", "catch ball.py"])
    return "Catch the Ball Game Started! Please wait for some time. The camera will open in a new window."

@app.route('/word_detection')
def word_detection():
    subprocess.Popen(["python", "word_detection.py"])
    return "Word Detection Application Started! Please wait for some time. The camera will open in a new window."

@app.route('/text_to_image')
def text_to_image():
    subprocess.Popen(["python", "text_to_image.py"])
    return "Text-to-Image Application Started! Please wait for some time. The camera will open in a new window."


# ----------------------------
# 🔹 Gemini Chatbot Integration
# ----------------------------
@app.route('/bot')
def bot():
    return render_template('bot.html')  # Serve the chatbot UI

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"
    return jsonify({"reply": reply})


# ----------------------------
# 🔹 Run Server
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)
