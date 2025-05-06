import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort # 导入 abort
from sqlalchemy import or_
from datetime import datetime

from models import HouseInfoModel, HouseStatusModel, CommentModel, NewsModel, db  # 确保导入 NewsModel
from decorators import login_required

house_bp = Blueprint('house', __name__)

with open('static/json/cities.json', 'r', encoding='utf-8') as f:
    cities_data = json.load(f)
@house_bp.route('', methods=['GET'])
def house_list():
    # 获取筛选条件
    region = request.args.get('region', '').strip()
    city = request.args.get('city', '').strip()
    keyword = request.args.get('keyword', '').strip()
    rooms = request.args.get('rooms', '').strip()
    address = request.args.get('address', '').strip()
    min_price = request.args.get('min_price', None, type=float)
    max_price = request.args.get('max_price', None, type=float)

    selected_region = region or ''
    selected_city = city or ''

    query = HouseInfoModel.query

    #  先处理所有过滤条件
    if address:
        query = query.filter(
            or_(
                HouseInfoModel.addr.like(f"%{address}%"),
                HouseInfoModel.region.like(f"%{address}%")
            )
        )

    if selected_region:
        query = query.filter(HouseInfoModel.region.like(f"%{selected_region}%"))

    if selected_city:
        query = query.filter(HouseInfoModel.region.like(f"%{selected_city}%"))

    if keyword:
        query = query.filter(HouseInfoModel.house_name.like(f"%{keyword}%"))

    if rooms == '4室及以上':
        query = query.filter(
            or_(
                HouseInfoModel.rooms.like("4室%"),
                HouseInfoModel.rooms.like("5室%"),
                HouseInfoModel.rooms.like("6室%"),
                HouseInfoModel.rooms.like("8室%"),
                HouseInfoModel.rooms.like("9室%"),
                HouseInfoModel.rooms.like("10室%"),
                HouseInfoModel.rooms.like("11室%"),
                HouseInfoModel.rooms.like("12室%"),
            )
        )
    else:
        query = query.filter(HouseInfoModel.rooms.like(f"%{rooms}%"))

    if min_price is not None:
        query = query.filter(HouseInfoModel.price >= min_price)

    if max_price is not None:
        query = query.filter(HouseInfoModel.price <= max_price)

    #  再执行分页
    page = request.args.get('page', 1, type=int)
    per_page = 9
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    houses = pagination.items

    # 新闻区
    news_list = NewsModel.query.order_by(NewsModel.time.desc()).limit(5).all()

    return render_template(
        'house/house_list.html',
        houses=houses,
        news_list=news_list,
        cities_data=cities_data,
        selected_region=selected_region,
        selected_city=selected_city,
        pagination=pagination,
        filters={
            'region': selected_region,
            'city': selected_city,
            'keyword': keyword or '',
            'rooms': rooms or '',
            'min_price': min_price,
            'max_price': max_price,
            'address': address or ''
        }
    )


@house_bp.route('/<int:house_id>', methods=['GET'])
def house_detail(house_id):
    house = HouseInfoModel.query.get(house_id)
    if not house:
        abort(404) # 如果房源不存在，返回404

    status = HouseStatusModel.query.filter_by(house_id=house_id).first()
    if not status:
        # 可以根据业务逻辑决定是否报错，或者提供默认状态
        status = HouseStatusModel(landlord_name='未知', status=-1) # 示例默认值

    # --- 分页处理 ---
    page = request.args.get('page', 1, type=int) # 从 URL 参数获取页码，默认为1
    per_page = 10 # 每页显示10条评论

    # 使用 paginate 进行查询
    pagination = CommentModel.query.filter_by(
        house_id=house_id
    ).order_by(
        CommentModel.time.desc() # 按时间倒序排列
    ).paginate(page=page, per_page=per_page, error_out=False) # error_out=False 避免页码超出范围时报错

    comments_on_page = pagination.items # 获取当前页的评论列表

    # --- 处理 @ 信息 (只处理当前页的评论) ---
    enriched_comments = []
    for comment in comments_on_page:
        comment_data = {
            'comment_id': comment.comment_id,
            'username': comment.username,
            'type': comment.type,
            'desc': comment.desc,
            'time': comment.time,
            'at': comment.at,
            'at_username': None,
            'at_desc': None
        }
        if comment.at:
            at_comment = CommentModel.query.filter_by(comment_id=comment.at).first()
            if at_comment:
                comment_data['at_username'] = at_comment.username
                comment_data['at_desc'] = at_comment.desc
        enriched_comments.append(comment_data)

    # --- 调试打印 (确认 comment_id) ---
    # print("传递给模板的 enriched_comments 数据:")
    # for c_data in enriched_comments:
    #     print(c_data)
    # --- 调试打印结束 ---

    return render_template(
        'house/house_detail.html',
        house=house,
        status=status,
        comments=enriched_comments, # 传递当前页处理后的评论
        pagination=pagination # 将分页对象传递给模板
    )


@house_bp.route('/load_more_news', methods=['GET'])
def load_more_news():
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



@house_bp.route('/add_comment_form', methods=['POST'])
@login_required
def add_comment_form():
    house_id = request.form.get('house_id')
    desc = request.form.get('comment')
    at = request.form.get('at')
    user_type = session.get('user_type', 1)
    username = session.get('username')

    # --- 添加调试打印 ---
    print(f"收到的表单数据: {request.form}")
    print(f"获取到的 'at' 值: {at}")
    # --- 调试打印结束 ---

    if not house_id or not desc or not username:
        # 可以重定向回原页面并带上错误提示
        return redirect(request.referrer or url_for('house.house_detail', house_id=house_id))

    comment = CommentModel(
        house_id=house_id,
        username=username,
        type=user_type,
        desc=desc,
        at=at, # 确认这里传递了 at
        time=datetime.now()
    )
    # --- 添加调试打印 ---
    print(f"准备存入数据库的 CommentModel: house_id={comment.house_id}, username={comment.username}, desc={comment.desc}, at={comment.at}")
    # --- 调试打印结束 ---
    db.session.add(comment)
    db.session.commit()
    # 添加成功后重定向回详情页
    return redirect(url_for('house.house_detail', house_id=house_id))
