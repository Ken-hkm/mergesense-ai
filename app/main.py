from fastapi import FastAPI
# from app.api.endpoints import reviews, users

app = FastAPI()

# # Register API routers
# app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
# app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "Welcome to MergeSense AI!"}