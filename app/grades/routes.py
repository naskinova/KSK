from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.grades.models import Grade
from app.database.session import get_db

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/save")
def save_grades(
    data: list[dict],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "examiner":
        raise HTTPException(status_code=403, detail="Only examiners can submit grades.")

    for item in data:
        existing = db.query(Grade).filter_by(student_id=item["student_id"], examiner_id=user.id).first()
        if existing:
            for i in range(1, 9):
                setattr(existing, f"task_{i}", item.get(str(i), 0.0))
            existing.total = sum([item.get(str(i), 0.0) for i in range(1, 9)])
        else:
            new_grade = Grade(
                student_id=item["student_id"],
                examiner_id=user.id,
                **{f"task_{i}": item.get(str(i), 0.0) for i in range(1, 9)},
                total=sum([item.get(str(i), 0.0) for i in range(1, 9)])
            )
            db.add(new_grade)

    db.commit()
    return {"message": "Grades saved successfully."}


@router.get("/assigned/me")
def get_my_assigned_students(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role != "examiner":
        raise HTTPException(status_code=403, detail="Access denied")

    student_ids = db.query(Grade.student_id)\
        .filter(Grade.examiner_id == user.id)\
        .distinct()\
        .all()

    return {"student_ids": [sid for (sid,) in student_ids]}


@router.get("/me")
def get_my_grades(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role != "examiner":
        raise HTTPException(status_code=403, detail="Access denied")

    grades = db.query(Grade).filter(Grade.examiner_id == user.id).all()
    return {
        "grades": [
            {
                "student_id": g.student_id,
                **{str(i): getattr(g, f"task_{i}") for i in range(1, 9)},
                "total": g.total
            } for g in grades
        ]
    }


@router.get("/by_examiner/{examiner_id}")
def get_grades_by_examiner(
    examiner_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role not in ["admin", "report_admin"] and user.id != examiner_id:
        raise HTTPException(status_code=403, detail="Access denied")

    grades = db.query(Grade).filter(Grade.examiner_id == examiner_id).all()
    return {
        "grades": [
            {
                "student_id": g.student_id,
                **{str(i): getattr(g, f"task_{i}") for i in range(1, 9)},
                "total": g.total
            } for g in grades
        ]
    }
