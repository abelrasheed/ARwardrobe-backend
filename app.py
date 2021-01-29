from flask_cors import CORS
from flask_restful import Api
from PIL import Image,ImageOps
import io
from flask import request,send_file,make_response,request,Flask,jsonify,url_for
from flask_restful import Resource
import numpy as np
from conversion import conversion
from base64 import encodebytes
import requests
import os

app = Flask(__name__)

CORS(app)
api = Api(app)

class image_return(Resource):
    def post(self):
        pic_loc = request.form['pic_loc']

        if not pic_loc :
            return "No image uploaded",400
        
        
        img_rgb = Image.open(requests.get(pic_loc, stream=True).raw)
        img_grey = ImageOps.grayscale(img_rgb)

        img_rbg = np.array(img_rgb)
        img_grey = np.array(img_grey)

        img_res = conversion(img_rbg,img_grey)
        # path = 'D:\Source codes\AR wardrobe\Backend\static\saved.png'
        rel_path = "\static\saved.png"
        abs_path = os.getcwd()
        
        path = abs_path+rel_path
        img_res.save(path,"png")
        # img_byte_arr = io.BytesIO()
        # img_res.save(img_byte_arr, format='png')

        # encoded_img =  encodebytes(img_byte_arr.getvalue()).decode('ascii')
        # return send_file(
        #     img_byte_arr,
        #     mimetype='image/jpeg',
        #     as_attachment = True,
        #     attachment_filename='image.jpg'
        # )
        # response = make_response(img_byte_arr)
        # response.headers.set('Content-type','image/png')
        # response.headers.set(
        #     'Content-Disposition','attachment',filename='image.png'
        # )
        url = url_for('static',filename ="saved.png")
        path_link = "https://arwardrobe.herokuapp.com/"
        url = path_link + url
        response =  {  'url': url} 
        return jsonify(response)


class home(Resource):
    def get(self):
        test_return = {"Home" : "Homes"}
        
        return "varunnundo kopile saanam ?"

api.add_resource(image_return, "/image")
api.add_resource(home, "/")








if __name__ == "__main__":
    app.run(debug=True)