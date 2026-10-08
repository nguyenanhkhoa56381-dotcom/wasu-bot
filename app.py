from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__, template_folder='.')
CORS(app)

import os
from groq import Groq

# Lấy key từ biến môi trường của hệ thống (Render sẽ cung cấp)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('webchat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages_history = data.get('messages', [])
    
    if not messages_history:
        return jsonify({'reply': 'Vui lòng nhập nội dung.'})

    # Thêm System Prompt để ép AI xuất chuẩn Markdown và LaTeX, tránh lỗi ngoặc kép
    system_prompt = {
        "role": "system", 
        "content": "Bạn là WASU's bot, trợ lý AI chuyên nghiệp hỗ trợ học sinh và dự án STEM. "
                   "Khi viết công thức toán học hoặc ký hiệu, LUÔN LUÔN sử dụng định dạng LaTeX chuẩn: "
                   "dùng $...$ cho công thức inline và $$...$$ cho khối phương trình độc lập. "
                   "TUYỆT ĐỐI KHÔNG bọc biểu thức LaTeX bằng dấu ngoặc kép dạng ((...)) hay hiển thị sai ký tự. "
                   "Hãy trình bày rõ ràng, đẹp mắt bằng Markdown."
    }

    # Đưa system prompt lên đầu tiên nếu chưa có
    if not messages_history or messages_history[0].get("role") != "system":
        messages_history.insert(0, system_prompt)

    try:
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