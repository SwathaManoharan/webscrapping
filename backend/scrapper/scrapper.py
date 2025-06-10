from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import requests
from bs4 import BeautifulSoup

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def scrape_the_hindu_headlines():
    url = "https://www.thehindu.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for tag in soup.find_all("a"):
        title = tag.get_text(strip=True)
        link = tag.get("href")
        if title and link and "article" in link:
            sentiment = get_sentiment(title)
            headlines.append({
                "title": title,
                "url": link,
                "sentiment": sentiment,
                "timestamp": datetime.utcnow().isoformat()
            })

    return headlines

if __name__ == "__main__":
    data = scrape_the_hindu_headlines()
    for item in data:
        print(f"[{item['timestamp']}] ({item['sentiment']}) {item['title']} → {item['url']}")
