from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_real_url(short_url):
    try:
        r = requests.get(short_url, allow_redirects=False)
        return r.headers.get('Location')
    except:
        return None

def extract_douyin_text(url):
    try:
        real_url = get_real_url(url)
        if not real_url:
            return None

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        html = requests.get(real_url, headers=headers).text

        title = re.search(r'<title.*?>(.*?)</title>', html)
        author = re.search(r'"nickname":"(.*?)"', html)
        cover = re.search(r'"cover":{"url_list":\["(.*?)"\]', html)

        return {
            "title": title.group(1) if title else "提取失败",
            "author": author.group(1) if author else "未知作者",
            "cover": cover.group(1) if cover else ""
        }
    except:
        return None

@app.route('/parse', methods=['GET'])
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少参数 url"}), 400

    data = extract_douyin_text(url)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "解析失败"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
