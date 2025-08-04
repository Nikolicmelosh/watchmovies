from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://www.lookmovie2.to/movies/search?q={query}"
    response = requests.get(url, headers=headers)
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

if __name__ == "__main__":
    app.run(port=5000)
