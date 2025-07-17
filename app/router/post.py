from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                limit: int=5, skip: int=0, search: Optional[str] = ""):
    # ex link: /posts?skip=1&limit=1&search=new%post
    # getting all posts of everyone
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # join automatically do left inner join. isouter=True -> left outer join

    # getting only the posts of the logged in user
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)): 
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
        #title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve the new post created ~= RETURNING *, and store it under new_post

    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
        #{id}: path perimeter - always return as STRING
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    ### if only able to view your own post (same logic as delete, etc.)
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    #                         detail=f'not authorized to view post')
    

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f'not authorized to delete post')
         

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f'not authorized to update post')
         

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
