from flask import Flask, jsonify, request, send_file
from app import Amazon
import asyncio

app = Flask(__name__)
amazon_instance = Amazon()
#

@app.route("/amazon", methods=['POST'])
def login_route():
    # Assuming you receive some data in the request, for example, JSON data
    request_data = request.get_json()
    requester_ip = request.remote_addr

    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")
    if 'url' in request_data:
        url = request_data['url']
        return jsonify(asyncio.run(amazon_instance.run(url))), 200
    else:
        return jsonify({'error': "Enter valid url"}), 400


@app.route('/captcha', methods=['GET'])
def get_captcha():
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")
    captcha_image_path = f"captcha.png"

    return send_file(captcha_image_path, mimetype='image/png'), 300


@app.route('/solve', methods=['POST'])
def solve_captcha():
    request_data = request.get_json()

    if 'captcha' in request_data:

        captcha = request_data['captcha']
        requester_ip = request.remote_addr
        print(f"Requester IP Address: {requester_ip}")
        print(f"Requester data: {request_data}")
        result = asyncio.run(amazon_instance.captcha(captcha))  # Start the captcha-solving thread
        return jsonify(result), 201
    else:
        return jsonify({'error': 'Missing captcha or url'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
