from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

# RSS feeds for different countries
RSS_FEEDS = {
    "India": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "US": "http://rss.cnn.com/rss/edition.rss",
    "UK": "http://feeds.bbci.co.uk/news/rss.xml",
    "Australia": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Canada": "https://www.cbc.ca/cmlink/rss-world",
    "Germany": "https://rss.dw.com/rdf/rss-en-world"
}

@app.route("/", methods=["GET"])
def home():
    # Default to India
    country = request.args.get("country", "India")
    feed_url = RSS_FEEDS.get(country, RSS_FEEDS["India"])

    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:10]:  # Get top 10
        article = {
            "title": entry.title,
            "link": entry.link,
            "description": getattr(entry, "summary", ""),
            "image": None
        }

        # Try extracting image
        if "media_content" in entry:
            article["image"] = entry.media_content[0]["url"]
        elif "links" in entry:
            for l in entry.links:
                if l.get("type", "").startswith("image"):
                    article["image"] = l["href"]
                    break

        articles.append(article)

    return render_template("index.html", 
                           articles=articles, 
                           country=country, 
                           countries=list(RSS_FEEDS.keys()))

if __name__ == "__main__":
    app.run(debug=True)
