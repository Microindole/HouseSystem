# blueprints/ai_chat_bp.py

from flask import Blueprint, request, jsonify, session, current_app, render_template, Response
from openai import OpenAI
import json
from decorators import login_required # 确保你的项目中存在这个装饰器

ai_chat_bp = Blueprint('ai_chat', __name__, url_prefix='/ai_chat')

def get_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = [
            {
                "role": "system",
                "content": (
                    "你是一个乐于助人的AI助手，专门为房屋租赁平台提供服务。"
                    "你可以回答关于租房流程、房源信息、合同条款以及提供一般性的租房建议。"
                    "请在适当的时候使用Markdown格式来排版你的回答，例如列表、代码块、加粗文本等。"
                )
            }
        ]
    return session['chat_history']

@ai_chat_bp.route('/')
@login_required
def chat_page():
    """提供聊天页面的路由，并传递当前用户的聊天记录"""
    chat_history = get_chat_history()
    return render_template('ai_chat_page.html', chat_history=chat_history)

@ai_chat_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "没有收到消息 (No message provided)"}), 400

    try:
        api_key = current_app.config['DEEPSEEK_API_KEY']
        base_url = current_app.config['DEEPSEEK_BASE_URL']

        client = OpenAI(api_key=api_key, base_url=base_url)

        chat_history = get_chat_history()
        chat_history.append({"role": "user", "content": user_input})

        def generate_response():
            """生成器函数，用于流式输出"""
            full_response = ""

            try:
                # 启用流式输出
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=chat_history,
                    stream=True  # 开启流式输出
                )

                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content

                        # 发送数据到前端，使用 Server-Sent Events 格式
                        yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"

                # 发送完成信号
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

                # 将完整回复保存到聊天历史
                chat_history.append({"role": "assistant", "content": full_response})
                session['chat_history'] = chat_history
                session.modified = True

            except Exception as e:
                current_app.logger.error(f"流式调用 DeepSeek API 出错: {e}")
                yield f"data: {json.dumps({'error': f'AI 服务暂时不可用: {str(e)}', 'done': True})}\n\n"

        return Response(
            generate_response(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
            }
        )

    except Exception as e:
        current_app.logger.error(f"调用 DeepSeek API 出错: {e}")
        return jsonify({"error": f"AI 服务暂时不可用: {str(e)}"}), 500

@ai_chat_bp.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    """清除当前用户的聊天记录"""
    if 'chat_history' in session:
        # 只保留系统消息，然后重新初始化历史记录
        system_message = session['chat_history'][0] if session['chat_history'] and session['chat_history'][0]['role'] == 'system' else {
            "role": "system",
            "content": (
                "你是一个乐于助人的AI助手，专门为房屋租赁平台提供服务。"
                "你可以回答关于租房流程、房源信息、合同条款以及提供一般性的租房建议。"
                "请在适当的时候使用Markdown格式来排版你的回答，例如列表、代码块、加粗文本等。"
            )
        }
        session['chat_history'] = [system_message]
        session.modified = True # 确保 session 被保存

    return jsonify({"status": "success", "message": "聊天记录已清除，保留系统提示。"})