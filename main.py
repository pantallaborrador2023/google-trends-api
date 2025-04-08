from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "146a288824d07a7eb9df8da42b1196bb"

@app.get("/news")
def get_news(keyword: str = Query(...)):
    try:
        url = f"https://gnews.io/api/v4/search?q={keyword}&lang=es&country=es&max=5&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "keyword": keyword,
            "articles": [
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "publishedAt": article["publishedAt"]
                }
                for article in data.get("articles", [])
            ]
        }
    except Exception as e:
        return {"error": str(e)}
