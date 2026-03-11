import requests
import base64
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_image():
    data = request.get_json()
    post_url = data.get('url')

    if not post_url:
        return jsonify({'error': 'URL not provided'}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.reddit.com/'
    }

    try:
        # Скачиваем картинку
        response = requests.get(post_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Конвертируем в base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')

        return jsonify({'image': image_base64})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to download: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
