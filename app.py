from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__, template_folder='.')
CORS(app)

# Khởi tạo Groq client với API Key của bạn
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template('webchat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages_history = data.get('messages', [])
    
    if not messages_history:
        return jsonify({'reply': 'Vui lòng nhập nội dung.'})

    try:
        # Sử dụng model đang hoạt động ổn định của Groq
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages_history,
            temperature=0.7,
            max_completion_tokens=2048,
            top_p=1,
            stream=False,
            stop=None
        )
        bot_reply = completion.choices[0].message.content
    except Exception as e:
        bot_reply = f"Lỗi Groq API: {str(e)}"
    
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)