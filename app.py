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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.reddit.com/',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
    }

    try:
        response = requests.get(post_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Проверяем, что вернулось изображение, а не HTML
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type:
            return jsonify({'error': 'Reddit returned HTML block page'}), 500
            
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return jsonify({'image': image_base64})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to download: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
