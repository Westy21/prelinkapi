import requests
from flask import Flask, request, Response, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)


def generate_link_preview(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title of the page
        title = soup.title.string if soup.title else ""

        # Extract the meta description, if available
        meta_description = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_description = meta_tag.get('content')

        # Extract an image URL, if available
        image_url = ""
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']

        # Return the link preview data
        link_preview = {
            'title': title,
            'description': meta_description,
            'image_url': image_url,
            'url': url
        }

        return link_preview

    except Exception as e:
        return {'error': str(e)}


@app.route("/prelink/<path:url>")
def compute(url):

    extra = request.args.get("extra")
    if extra:
        response["extra"] = extra

    return jsonify(generate_link_preview(url=url)), 200


@app.route("/")
def index():
    return "Hello World", 200


@app.route("/create-resonse", methods=["POST"])
def create_response():
    data = request.get_json()

    return jsonify(data), 201


if __name__ == "__main__":
    # Run on all addresses
    app.run(debug=True, host="0.0.0.0")
