from quart import Quart, jsonify, request, send_file
from app import Amazon

app = Quart(__name__)

global uuidn
global captcha_count
global amazon_instance

@app.route("/amazon", methods=['POST'])
async def login_route():

    request_data = await request.get_json()
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")
    print(f"Requester data: {request_data}")
    try:
        if 'url' in request_data:
            url = request_data['url']
            if '/dp/' in url:
                global uuidn
                global captcha_count
                global amazon_instance

                amazon_instance = Amazon()
                uuidn = amazon_instance.uuidn
                captcha_count = amazon_instance.captcha_count

                result = await amazon_instance.run(url)
                return jsonify(result), 200
            else:
                return jsonify({'error': "Enter full product url. Short url not accepted"}), 400
        else:
            return jsonify({'error': "Enter valid url"}), 400
    except TypeError:
        return jsonify({'error': "Enter url"}), 400


@app.route('/captcha', methods=['GET'])
async def get_captcha():
    requester_ip = request.remote_addr
    print(f"Requester IP Address: {requester_ip}")

    try:
        with open(f'captcha_{login_route}.txt', 'r') as f:
            cou = f.read()
            print(cou)
            print(captcha_count)
            if captcha_count == int(cou):
                return await send_file(f'captcha_{uuidn}.png', mimetype='image/png'), 200
            else:
                return jsonify({"msg": "try_again"}), 401

    except FileNotFoundError:
        return jsonify({"msg": "No captcha"}), 200


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
