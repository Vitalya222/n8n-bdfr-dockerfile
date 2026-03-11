import subprocess
import base64
import tempfile
import os
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_image():
    data = request.get_json()
    post_url = data.get('url')

    if not post_url:
        return jsonify({'error': 'URL not provided'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        # Создаём поддиректорию внутри временной папки
        download_dir = Path(tmpdir) / 'downloads'
        download_dir.mkdir(exist_ok=True)
        
        try:
            subprocess.run([
                'bdfr', 'download', str(download_dir),
                '--link', post_url,
                '--file-scheme', '{POSTID}',
                '--no-dupes'
            ], check=True, capture_output=True, timeout=30)

            # Ищем любой файл в папке
            files = list(download_dir.glob('*'))
            if not files:
                return jsonify({'error': 'No file downloaded'}), 500

            with open(files[0], 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')

            return jsonify({'image': img_base64})

        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'bdfr failed: {e.stderr.decode()}'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
