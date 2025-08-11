# api.py (Now with a Health Check endpoint)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database

app = FastAPI(title="Capital Realty Hub API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW HEALTH CHECK ENDPOINT ---
@app.get("/health-check")
def health_check():
    """
    This special endpoint tests the database connection.
    """
    try:
        # Try to establish a connection and immediately close it.
        connection = database.engine.connect()
        connection.close()
        return {"status": "ok", "database_connection": "successful"}
    except Exception as e:
        # If it fails for any reason, return the error message.
        return {"status": "error", "database_connection": "failed", "error_message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Welcome! API is running. Go to /results to see data."}

@app.get("/results")
def get_results():
    print("API endpoint called: /results")
    database.init_db()
    df = database.load_all_properties()
    if df.empty:
        return {"properties": []}
    
    results = df.head(30).to_dict(orient='records')
    return {"properties": results}
