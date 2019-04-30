#!/usr/bin/env python3
# apparently shebang is necessary if using docker smh

from flask import Flask, json, g, Response, request, render_template
from flask_cors import CORS
import requests

import cv2
import os
import base64
import PIL.Image
import io
import re

import deep_dream

# template_dir = os.path.abspath('../frontend/build')
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Welcome to the API!"


@app.route('/upload', methods=['POST'])
def upload():
    try:
        # call out to imgur to upload the image
        # os.environ.get('IMGUR_CLIENT_ID')
        IMGUR_CLIENT_ID = 'Client-ID 7f5f4b80e5266ff'
        headers = {'Authorization': IMGUR_CLIENT_ID}

        # dont need this one since image wil (prolly) be in base64 already
        # infile.write(base64.decodebytes(request.get_data()))
        json_data = request.get_json(force=True)

        imstr = re.sub(r'data:image\/[^;]+;base64,', '', json_data['data'])

        url = 'https://api.imgur.com/3/upload'
        params = {'image': imstr}
        res = requests.post(url=url, data=params, headers=headers)
        res = res.json()
        print(res)

        # run algo
        deep_dream.main(requests.get(res['data']['link'], stream=True).raw)

        # return output
        with open('out.png', 'rb') as outfile:
            encoded = base64.b64encode(outfile.read())

            url = 'https://api.imgur.com/3/upload'
            params = {'image': encoded}
            res = requests.post(url=url, data=params, headers=headers)
            res = res.json()
            print(res)

        data = {
            'link': res['data']['link'],
            'deletehash': res['data']['deletehash']
        }

        data = json.dumps(data)
        return Response(data, status=200, mimetype='application/json')

    except Exception as e:
        print(str(e), 'wut')
        err = {
            'message': 'could not generate your image'
        }
        err = json.dumps(err)
        return Response(err, status=500, mimetype='text/plain')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
