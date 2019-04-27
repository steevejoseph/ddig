from flask import Flask, json, g, Response, request
from flask_cors import CORS
import requests

import cv2
import os
import base64

import deep_dream

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    deep_dream.main()
    return "We in dis bitch"

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # print('Posted data: {}'.format(request.get_data()))
        with open('in', 'wb') as infile:

            # dont need this one since image wil (prolly) be in base64 already
            # infile.write(base64.decodebytes(request.get_data()))
            infile.write(request.get_data())
            
        # run algo
        deep_dream.main('in')

                # return output
        with open('out.png', 'rb') as outfile:
            encoded = base64.b64encode(outfile.read())
            
            #call out to imgur to upload the image
            IMGUR_CLIENT_ID = 'Client-ID {}'.format(os.environ.get('IMGUR_CLIENT_ID'))
            headers = {'Authorization':IMGUR_CLIENT_ID}
            url = 'https://api.imgur.com/3/upload'
            params = {'image': encoded}
            res = requests.post(url=url, data=params, headers=headers)
            res=res.json()
            print(res)

        data = {
            'link': res['data']['link'],
            'deletehash': res['data']['deletehash'] 
        }
        
        data = json.dumps(data)
        return Response(data, status=200, mimetype='application/json') 

    except Exception as e:
        print(e)
        err = {
            'message': 'could not generate your image'
        }
        err = json.dumps(err)
        return Response(err, status=500, mimetype='text/plain')