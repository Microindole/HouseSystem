# blueprints/ai_chat_bp.py

from flask import Blueprint, request, jsonify, session, current_app, render_template, Response, g
from openai import OpenAI
from functools import wraps
import json
import re
from bs4 import BeautifulSoup
from decorators import login_required, verify_token # Ensure these are correctly imported from your project structure

ai_chat_bp = Blueprint('ai_chat', __name__, url_prefix='/ai_chat')

def get_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = [
            {
                "role": "system",
                "content": (
                        "你是一个乐于助人的AI助手，专门为房屋租赁平台提供服务。"
                        "你可以回答关于租房流程、房源信息、合同条款以及提供一般性的租房建议。"
                        "当用户提供页面内容时，你可以分析页面内容并基于页面信息给出针对性的回答。"
                        "请在适当的时候使用Markdown格式来排版你的回答，例如列表、代码块、加粗文本等。"
                        "用户名为：" + (g.username if hasattr(g, 'username') and g.username else "访客") +
                        "，用户类型为：" + (str(g.user_type) if hasattr(g, 'user_type') and g.user_type is not None else "未知")
                )
            }
        ]
    # Update username and user_type in system prompt if they exist and changed
    elif session['chat_history'] and session['chat_history'][0]['role'] == 'system':
        current_username = g.username if hasattr(g, 'username') and g.username else "访客"
        current_user_type = str(g.user_type) if hasattr(g, 'user_type') and g.user_type is not None else "未知"
        system_content = (
                "你是一个乐于助人的AI助手，专门为房屋租赁平台提供服务。"
                "你可以回答关于租房流程、房源信息、合同条款以及提供一般性的租房建议。"
                "当用户提供页面内容时，你可以分析页面内容并基于页面信息给出针对性的回答。"
                "请在适当的时候使用Markdown格式来排版你的回答，例如列表、代码块、加粗文本等。"
                "用户名为：" + current_username +
                "，用户类型为：" + current_user_type
        )
        if session['chat_history'][0]['content'] != system_content:
            session['chat_history'][0]['content'] = system_content
            session.modified = True

    return session['chat_history']

def clean_html_content(html_content):
    """清理和提取HTML内容中的有用文本"""
    if not html_content:
        return ""

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 移除脚本和样式标签
    for script in soup(["script", "style"]):
        script.decompose()

    # 提取文本
    text = soup.get_text()

    # 清理多余的空白字符
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text

# --- token身份校验 ---
def token_required_for_ai(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return jsonify({'error': '未登录或登录已过期'}), 401
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token无效或已过期'}), 401
        g.username = payload.get('username')
        g.user_type = payload.get('user_type')
        return f(*args, **kwargs)
    return decorated_function

@ai_chat_bp.route('/')
@token_required_for_ai
@login_required
def chat_page():
    """提供聊天页面的路由，并传递当前用户的聊天记录"""
    chat_history = get_chat_history()
    return render_template('ai_chat_page.html', chat_history=chat_history)

@ai_chat_bp.route('/get_history', methods=['GET'])
@token_required_for_ai
@login_required
def get_history_api():
    """API端点，用于获取当前用户的聊天记录"""
    chat_history = get_chat_history()
    return jsonify(chat_history)

@ai_chat_bp.route('/send_message', methods=['POST'])
@token_required_for_ai
@login_required
def send_message():
    data = request.json
    user_input = data.get('message')
    page_content = data.get('pageContent', '')  # 获取页面内容

    if not user_input:
        return jsonify({"error": "没有收到消息 (No message provided)"}), 400

    try:
        api_key = current_app.config['DEEPSEEK_API_KEY']
        base_url = current_app.config['DEEPSEEK_BASE_URL']

        client = OpenAI(api_key=api_key, base_url=base_url)

        chat_history = get_chat_history()

        # 如果有页面内容，将其添加到用户消息中
        if page_content:
            cleaned_content = clean_html_content(page_content)
            if cleaned_content.strip():
                enhanced_message = f"{user_input}\n\n[当前页面内容参考]:\n{cleaned_content[:3000]}"  # 限制长度避免token过多
                chat_history.append({"role": "user", "content": enhanced_message})
            else:
                chat_history.append({"role": "user", "content": user_input})
        else:
            chat_history.append({"role": "user", "content": user_input})

        def generate_response():
            """生成器函数，用于流式输出"""
            full_response = ""
            first_chunk_sent = False
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=chat_history,
                    stream=True
                )

                for chunk in response:
                    if chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
                        first_chunk_sent = True

                    if chunk.choices[0].finish_reason == "stop" or chunk.choices[0].finish_reason == "length":
                        break

                if not first_chunk_sent:
                    yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
                else:
                    yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

                if full_response:
                    chat_history.append({"role": "assistant", "content": full_response})
                    session['chat_history'] = chat_history
                    session.modified = True

            except Exception as e:
                current_app.logger.error(f"流式调用 DeepSeek API 出错: {e}")
                yield f"data: {json.dumps({'error': f'AI 服务暂时不可用: {str(e)}', 'done': True})}\n\n"

        return Response(
            generate_response(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            }
        )

    except Exception as e:
        current_app.logger.error(f"调用 DeepSeek API 出错: {e}")
        return jsonify({"error": f"AI 服务暂时不可用: {str(e)}"}), 500

@ai_chat_bp.route('/clear_history', methods=['POST'])
@token_required_for_ai
@login_required
def clear_history():
    """清除当前用户的聊天记录"""
    if 'chat_history' in session:
        session.pop('chat_history', None)
        get_chat_history()
        session.modified = True

    return jsonify({"status": "success", "message": "聊天记录已清除，并已使用最新用户信息重置系统提示。"})