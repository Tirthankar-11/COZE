from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Douyin 文案提取 API 正常运行，请访问 /parse?url='

@app.route('/parse')
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "请提供 url 参数"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
        real_url = response.url
        html = response.text

        title = re.search(r'<title>(.*?)</title>', html)
        title = title.group(1).replace('- 抖音', '').strip() if title else '未找到标题'

        author = re.search(r'"authorName":"(.*?)"', html)
        author = author.group(1) if author else '未知作者'

        cover = re.search(r'"cover":{"url_list":\["(.*?)"', html)
        cover = cover.group(1) if cover else ''

        return jsonify({
            'title': title,
            'author': author,
            'cover': cover,
            'real_url': real_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
