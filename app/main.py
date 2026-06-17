import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware 
from app.routers import comments
from .database import engine, Base
from .routers import auth, posts

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Reddit API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origin, swap to your frontend URL later if desired
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "traceback": traceback.format_exc().split("\n")
        }
    )

app.include_router(auth.router, tags=["Authentication"])
app.include_router(posts.router, tags=["Posts"])
app.include_router(comments.router,  tags=["Comments"])
@app.get("/")
def root():
    return {"message": "Welcome to the Anonymous Reddit Platform Backend!"}