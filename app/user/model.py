import jwt, string, secrets, bcrypt
from datetime import datetime

from sqlalchemy import or_
from app import app, db, secret
from helpers.phonenumber import validate_phonenumber

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    language = db.Column(db.String)
    country = db.Column(db.String)
    state = db.Column(db.String)
    lga = db.Column(db.String)
    town = db.Column(db.String)
    is_set = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    role = db.Column(db.String, nullable=True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, name=None, language=None, country=None, state=None, lga=None, town=None, is_set=None):
        self.name = name or self.name
        self.language = language or self.language
        self.country = country or self.country
        self.state = state or self.state
        self.lga = lga or self.lga
        self.town = town or self.town
        self.is_set = is_set or self.is_set
        self.updated_at = db.func.now()
        db.session.commit()
    
    def generate_password(self):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        return password
    
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def generate_token(self):
        payload = {
            'exp': app.config.get('JWT_REFRESH_TOKEN_EXPIRES'),
            'iat': datetime.utcnow(),
            'sub': self.id,
            'role': self.role
        }
        return jwt.encode(payload, secret, algorithm='HS256')
    
    def update_password(self, old_password, new_password):
        if self.is_verified(old_password):
            self.password = new_password
            self.hash_password()
            self.update()
            return True
        return False
    
    def reset_password(self, new_password):
        self.password = new_password
        self.hash_password()
        self.update()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_by_phone(self, phone):
        return User.query.filter(User.phone.ilike(f"%{phone[1:]}%")).first()
    
    @classmethod
    def get_by_location(self, location):
        return User.query.filter(or_(User.country.ilike(f"%{location}%"), User.state.ilike(f"%{location}%"), User.lga.ilike(f"%{location}%"), User.town.ilike(f"%{location}%"))).all()
    
    @classmethod
    def create(cls, name, language, country, state, lga, town, phone, password, role):
        user = cls(name=name, language=language, country=country, state=state, lga=lga, town=town, phone=validate_phonenumber(phone), password=password, role=role)
        user.hash_password()
        user.save()
        return user