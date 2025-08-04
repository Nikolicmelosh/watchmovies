from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "123MoviesFree scraper is alive!"

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = f"https://ww7.123moviesfree.net/?s={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch. Status code: {response.status_code}"}), 500

        soup = BeautifulSoup(response.text, "html.parser")
        movie_divs = soup.select("div.ml-item")

        results = []
        for movie in movie_divs:
            link_tag = movie.find("a")
            img_tag = movie.find("img")

            if link_tag and img_tag:
                title = img_tag.get("alt", "No title")
                image = img_tag.get("data-original", "") or img_tag.get("src", "")
                link = link_tag.get("href", "")

                results.append({
                    "title": title.strip(),
                    "image": image.strip(),
                    "link": link.strip()
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
