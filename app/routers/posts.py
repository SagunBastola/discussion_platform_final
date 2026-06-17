from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Post, User
from app.schemas import PostCreate, PostOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostOut)
def create_post(
    post_data: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # Protects the route
):
    # current_user is available here because the JWT token was successfully validated
    new_post = Post(title=post_data.title, content=post_data.content, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

from typing import List

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return posts