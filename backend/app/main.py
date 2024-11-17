from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field

from .database import Database

load_dotenv()

SECRET_KEY = getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(getenv("DATABASE_URL"))


@app.lifespan
async def lifespan(app: FastAPI):
    """Lifespan event handler for the application"""
    await startup_event()
    yield
    await shutdown_event()

async def startup_event():
    """Initialize the database on startup"""
    print("Initializing database...")
    db.init_db()
    print("Database initialized!")


async def shutdown_event():
    """Clean up resources on shutdown"""
    pass


class ReviewSubmission(BaseModel):
    name: str = Field(..., description="Restaurant name")
    meal: str = Field(..., description="Name of the meal")
    meal_description: Optional[str] = Field(None, description="Description of the meal")
    reviewer: str = Field(..., description="Name of the reviewer")
    price: float = Field(..., ge=0, description="Price of the meal")
    quantity_score: int = Field(..., ge=1, le=10, description="Score for quantity")
    taste_score: int = Field(..., ge=1, le=10, description="Score for taste")
    atmosphere_score: int = Field(..., ge=1, le=10, description="Score for atmosphere")
    overall_score: int = Field(..., ge=1, le=10, description="Overall score")
    comments: Optional[str] = Field(None, description="Additional comments")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Test Restaurant",
                "meal": "Loaded Nachos",
                "meal_description": "Classic nachos with all the toppings",
                "reviewer": "John Doe",
                "price": 15.99,
                "quantity_score": 8,
                "taste_score": 9,
                "atmosphere_score": 7,
                "overall_score": 8,
                "comments": "Great nachos!",
            }
        }


async def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != getenv("ADMIN_USERNAME"):
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(status_code=401)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != getenv("ADMIN_USERNAME") or form_data.password != getenv(
        "ADMIN_PASSWORD"
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/reviews")
async def get_reviews():
    try:
        reviews = await db.get_reviews()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    stats = await db.get_stats()
    return stats


@app.post("/api/reviews")
async def submit_review(review: ReviewSubmission):
    try:
        review_id = await db.add_pending_review(review.dict())
        return {"message": "Review submitted successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pending-reviews")
async def get_pending_reviews(current_admin: str = Depends(get_current_admin)):
    return await db.get_pending_reviews()


@app.post("/api/reviews/{review_id}/approve")
async def approve_review(
    review_id: int, current_admin: str = Depends(get_current_admin)
):
    success = await db.approve_review(review_id)
    if success:
        return {"message": "Review approved successfully"}
    raise HTTPException(status_code=404, detail="Review not found")
