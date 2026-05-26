from datetime import datetime
from app import db
 
class Course(db.Model):
    __tablename__ = 'courses'
 
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title     = db.Column(db.String(100), nullable=False, unique=True)
    course_fee       = db.Column(db.Float, nullable=False, default=0.0)
    duration_months  = db.Column(db.Integer, nullable=False)
    description      = db.Column(db.Text)
    is_available     = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
 
    def to_dict(self):
        return {
            'id':              self.id,
            'course_title':    self.course_title,
            'course_fee':      self.course_fee,
            'description':     self.description,
            'duration_months': self.duration_months,
            'is_available':    self.is_available,
        }