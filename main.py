from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.controller import app_client, app_instagram

app = FastAPI()

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")

app.include_router(app_client, prefix="/api/v1", tags=["client"])
app.include_router(app_instagram, prefix="/api/v1", tags=["instagram"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)