import json
from flask import render_template, request, flash, redirect, url_for, session, jsonify, current_app
from datetime import datetime
from models import NewsModel, HouseStatusModel, db

def add_news_logic():
    if session.get('user_type') != 2:
        flash('只有房东可以发布新闻', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = session.get('username')
    houses = HouseStatusModel.query.filter_by(landlord_name=landlord_name).all()
    if request.method == 'GET':
        return render_template('house/add_news.html', houses=houses)
    try:
        house_id = request.form.get('house_id')
        title = request.form.get('title')
        desc = request.form.get('desc')
        if not all([house_id, title]):
            flash('请填写必填信息', 'error')
            return render_template('house/add_news.html', houses=houses)
        house_status = HouseStatusModel.query.filter_by(
            house_id=house_id,
            landlord_name=landlord_name
        ).first()
        if not house_status:
            flash('房源不存在或您无权发布相关新闻', 'error')
            return render_template('house/add_news.html', houses=houses)
        news = NewsModel(
            time=datetime.now(),
            house_id=house_id,
            title=title,
            desc=desc,
            landlord_username=landlord_name
        )
        db.session.add(news)
        db.session.commit()
        flash('新闻发布成功！', 'success')
        return redirect(url_for('house.manage_news'))
    except Exception as e:
        db.session.rollback()
        flash(f'发布失败：{str(e)}', 'error')
        return render_template('house/add_news.html', houses=houses)

def manage_news_logic():
    if session.get('user_type') != 2:
        flash('只有房东可以管理新闻', 'error')
        return redirect(url_for('account.landlord_home'))
    landlord_name = session.get('username')
    news_list = NewsModel.query.filter_by(landlord_username=landlord_name)\
                               .order_by(NewsModel.time.desc()).all()
    return render_template('house/manage_news.html', news_list=news_list)

def delete_news_logic(news_id):
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以删除新闻'}), 403
    landlord_name = session.get('username')
    news = NewsModel.query.filter_by(id=news_id, landlord_username=landlord_name).first()
    if not news:
        return jsonify({'success': False, 'message': '新闻不存在或您无权删除'}), 404
    try:
        db.session.delete(news)
        db.session.commit()
        return jsonify({'success': True, 'message': '新闻删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败：{str(e)}'}), 500

def batch_delete_news_logic():
    if session.get('user_type') != 2:
        return jsonify({'success': False, 'message': '只有房东可以批量删除新闻'}), 403
    try:
        data = request.get_json()
        news_ids = data.get('news_ids', [])
        if not news_ids:
            return jsonify({'success': False, 'message': '未选择任何新闻'}), 400
        landlord_name = session.get('username')
        deleted_count = 0
        for news_id in news_ids:
            news = NewsModel.query.filter_by(id=news_id, landlord_username=landlord_name).first()
            if news:
                db.session.delete(news)
                deleted_count += 1
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'成功删除 {deleted_count} 条新闻',
            'count': deleted_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'批量删除失败：{str(e)}'}), 500

def load_more_news_logic():
    start = int(request.args.get('start', 0))
    limit = 7
    news_query = NewsModel.query.order_by(NewsModel.time.desc())
    news = news_query.offset(start).limit(limit).all()
    has_more = news_query.count() > start + limit
    news_data = [
        {
            'title': n.title,
            'desc': n.desc,
            'time': n.time.strftime('%Y-%m-%d')
        }
        for n in news
    ]
    return jsonify({'news': news_data, 'has_more': has_more})

