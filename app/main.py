from fastapi import FastAPI, Depends, Header, HTTPException
from app.config import get_settings
from app.routers import hymns, open_heavens, comments, likes, prayers

settings = get_settings()
app = FastAPI(
    root_path="/open-heavens",  # Add this line
    title="Open Heavens API"
)

# API key dependency
async def require_api_key(x_api_key: str = Header(...)):
    # Accept either the primary API_KEY or any in API_KEYS list.
    provided = x_api_key
    # support Authorization: Bearer <token> as well
    if provided.startswith("Bearer "):
        provided = provided.split(" ", 1)[1]

    allowed = [settings.api_key] + list(settings.api_keys or [])
    if provided not in allowed:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# include routers (protected by dependency)
app.include_router(hymns.router, prefix="/hymns", dependencies=[Depends(require_api_key)])
app.include_router(open_heavens.router, prefix="/open-heavens", dependencies=[Depends(require_api_key)])
app.include_router(comments.router, prefix="/comments", dependencies=[Depends(require_api_key)])
app.include_router(likes.router, prefix="/likes", dependencies=[Depends(require_api_key)])
app.include_router(prayers.router, prefix="/prayers", dependencies=[Depends(require_api_key)])

@app.get("/health")
async def health():
    return {"status": "ok"}
