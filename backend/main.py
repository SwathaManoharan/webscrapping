from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path

from scrapper.scrapper import scrape_the_hindu_headlines

app = FastAPI()

# CORS for React (local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Add security headers middleware (ZAP wants these)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 📦 Serve static React files from frontend/build
build_path = Path(__file__).parent.parent / "frontend" / "build"
app.mount("/static", StaticFiles(directory=build_path / "static"), name="static")

@app.get("/")
def serve_react():
    return FileResponse(build_path / "index.html")

@app.get("/headlines")
def get_headlines():
    headlines = scrape_the_hindu_headlines()
    return {"data": headlines}

@app.get("/summary")
def sentiment_summary():
    headlines = scrape_the_hindu_headlines()
    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for h in headlines:
        summary[h["sentiment"]] += 1
    return summary
