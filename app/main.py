from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.grades.routes import router as grades_router

app = FastAPI(
    title="KSK Система за оценяване",
    version="1.0.0",
    description="🔐 API за логин, проверяващи и оценяване на студенти.",
)

# CORS (important for Streamlit frontend to talk to FastAPI backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TIP: Replace with Streamlit frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(grades_router, prefix="/grades", tags=["Grades"])
