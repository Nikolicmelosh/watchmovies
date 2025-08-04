from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "LookMovie scraper is alive!"

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = f"https://www.lookmovie2.to/movies/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.lookmovie2.to/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch"}), 500

        soup = BeautifulSoup(response.text, "html.parser")
        movie_divs = soup.select("div.movie-item-style-2")

        results = []
        for movie in movie_divs:
            link_tag = movie.select_one("a[href^='/movies/view']")
            img_tag = movie.select_one("img")

            if link_tag and img_tag:
                title = img_tag.get("alt", "No title")
                image = img_tag.get("data-src", "")
                link = link_tag.get("href", "")

                results.append({
                    "title": title.strip(),
                    "image": f"https://www.lookmovie2.to{image}",
                    "link": f"https://www.lookmovie2.to{link}"
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
