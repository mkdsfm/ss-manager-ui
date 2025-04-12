from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/")
def read_example(user: str = Depends(get_current_user)):
    return {"message": "Hello from example controller!"}
