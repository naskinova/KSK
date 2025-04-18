# app/grades/models.py
from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    examiner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_1 = Column(Float, default=0.0)
    task_2 = Column(Float, default=0.0)
    task_3 = Column(Float, default=0.0)
    task_4 = Column(Float, default=0.0)
    task_5 = Column(Float, default=0.0)
    task_6_a = Column(Float, default=0.0)
    task_6_b = Column(Float, default=0.0)
    task_6_c = Column(Float, default=0.0)
    task_6 = Column(Float, default=0.0)
    task_7_a = Column(Float, default=0.0)
    task_7_b = Column(Float, default=0.0)
    task_7_c = Column(Float, default=0.0)
    task_7 = Column(Float, default=0.0)
    task_8_a = Column(Float, default=0.0)
    task_8_b = Column(Float, default=0.0)
    task_8_c = Column(Float, default=0.0)
    task_8 = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    __table_args__ = (UniqueConstraint("student_id", "examiner_id", name="uix_student_examiner"),)

    examiner = relationship("User", backref="grades")
