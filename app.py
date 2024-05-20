from flask import Flask, request, render_template, redirect, url_for
from blind_watermark import WaterMark
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files or 'watermark' not in request.form:
        return redirect(url_for('index'))
    
    image = request.files['image']
    watermark = request.form['watermark']

    if image.filename == '':
        return redirect(url_for('index'))

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Embed the watermark
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img(image_path)
    bwm1.read_wm(watermark, mode='str')
    embedded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'embedded.png')
    bwm1.embed(embedded_path)
    len_wm = len(bwm1.wm_bit)

    return render_template('index.html', embedded_image=embedded_path, wm_length=len_wm)

@app.route('/decode', methods=['POST'])
def decode():
    if 'encoded_image' not in request.files or 'wm_length' not in request.form:
        return redirect(url_for('index'))
    
    encoded_image = request.files['encoded_image']
    wm_length = int(request.form['wm_length'])

    if encoded_image.filename == '':
        return redirect(url_for('index'))

    encoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], encoded_image.filename)
    encoded_image.save(encoded_image_path)

    # Extract the watermark
    bwm1 = WaterMark(password_img=1, password_wm=1)
    wm_extract = bwm1.extract(encoded_image_path, wm_shape=wm_length, mode='str')

    return render_template('index.html', extracted_watermark=wm_extract)

if __name__ == '__main__':
    app.run(debug=True)
