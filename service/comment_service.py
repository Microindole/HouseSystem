from flask import request, jsonify, session
from datetime import datetime
from models import CommentModel, db

def add_comment_form_logic():
    house_id = request.form.get('house_id')
    desc = request.form.get('comment')
    at = request.form.get('at')
    user_type = session.get('user_type', 1)
    username = session.get('username')
    
    if not house_id or not desc or not username:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    
    try:
        comment = CommentModel(
            house_id=house_id,
            username=username,
            type=user_type,
            desc=desc,
            at=at if at else None,
            time=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        
        # 构造回复信息
        at_username = None
        at_desc = None
        if at:
            at_comment = CommentModel.query.filter_by(comment_id=at).first()
            if at_comment:
                at_username = at_comment.username
                at_desc = at_comment.desc
        
        # 返回新评论的完整数据
        comment_data = {
            'comment_id': comment.comment_id,
            'username': comment.username,
            'type': comment.type,
            'desc': comment.desc,
            'time': comment.time.strftime('%Y-%m-%d %H:%M:%S'),
            'at_username': at_username,
            'at_desc': at_desc
        }
        
        return jsonify({
            'success': True, 
            'message': '评论发表成功',
            'comment': comment_data
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'评论发表失败: {str(e)}'}), 500

