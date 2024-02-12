from quart import Quart, jsonify, request, send_file
from app import Amazon
import asyncio

app = Quart(__name__)
amazon_instance = Amazon()

@app.route("/amazon", methods=['POST'])
async def login_route():

    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")
    if 'url' in request_data:
        url = request_data['url']
        result = await amazon_instance.run(url)
        return jsonify(result), 200
    else:
        return jsonify({'error': "Enter valid url"}), 400


@app.route('/captcha', methods=['GET'])
async def get_captcha():
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")
    captcha_image_path = f"captcha.png"

    return await send_file(captcha_image_path, mimetype='image/png'), 300


@app.route('/solve', methods=['POST'])
async def solve_captcha():
    request_data = await request.get_json()

    if 'captcha' in request_data:

        captcha = request_data['captcha']
        requester_ip = request.remote_addr
        print(f"Requester IP Address: {requester_ip}")
        print(f"Requester data: {request_data}")
        result = await amazon_instance.captcha_inp(captcha)
        return jsonify(result), 201
    else:
        return jsonify({'error': 'Missing captcha or url'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
