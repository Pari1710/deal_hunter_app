# api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database

app = FastAPI(title="EstateVision AI API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome! API is running. Go to /results to see data."}

@app.get("/results")
def get_results():
    """Quickly fetches the latest results from the database."""
    print("API endpoint called: /results")
    database.init_db() # Ensures table exists
    df = database.load_all_properties()
    if df.empty:
        return {"properties": []}
    
    # Return the most recent 30 results
    results = df.head(30).to_dict(orient='records')
    return {"properties": results}