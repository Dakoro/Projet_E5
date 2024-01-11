
import logging as log
from flask import Flask, render_template, request
from pdf2image import convert_from_bytes
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route('/pdf2img', methods=['POST', 'GET'])
def pdf2image():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        data = pdf_file.read()
        try:
            _ = convert_from_bytes(data, dpi=300)
        except Exception as e:
            print(log.error(e))
    return render_template('pdf2img.html')


if __name__ == '__main__':
    app.run(debug=True)
