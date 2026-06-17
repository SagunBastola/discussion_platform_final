from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Internal imports structured around your project layout
from app.database import get_db
from app.routers.auth import get_current_user
from app.model import User, Comment, Post  
from app.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Verify the target post exists before allowing a comment to be added
    post = db.query(Post).filter(Post.id == comment_data.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {comment_data.post_id} does not exist"
        )

    new_comment = Comment(
        content=comment_data.content,
        post_id=comment_data.post_id,
        owner_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/post/{post_id}", response_model=List[CommentOut])
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    # Verify the post exists first
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} does not exist"
        )
        
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    comment_query = db.query(Comment).filter(Comment.id == comment_id)
    comment = comment_query.first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Comment with id {comment_id} not found"
        )

    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this comment"
        )

    comment_query.delete(synchronize_session=False)
    db.commit()
    return None