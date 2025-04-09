from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/")
def read_example():
    return {"message": "Hello from example controller!"}
