from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

# exts.py
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
