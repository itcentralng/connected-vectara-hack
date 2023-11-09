from app import db

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.String)
    answer = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, user_id=None, question=None, answer=None):
        self.user_id = user_id or self.user_id
        self.question = question or self.question
        self.answer = answer or self.answer
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_latest_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).limit(10).all()
    
    @classmethod
    def create(cls, user_id, question, answer):
        search = cls(user_id=user_id, question=question, answer=answer)
        search.save()
        return search