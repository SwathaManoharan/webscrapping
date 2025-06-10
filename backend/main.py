from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrapper.scrapper import scrape_the_hindu_headlines

app = FastAPI()

# 🔧 Allow frontend access (React runs on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "API is live!"}

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
