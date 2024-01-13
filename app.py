import logging as log
import pyvips
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from solution import vips_to_numpy
app = Flask(__name__)

log.basicConfig(filename='logs/app.log', level=log.INFO)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route('/pdf2img', methods=['POST', 'GET'])
def pdf2image():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        data = pdf_file.read()
        try:
            # pdf = convert_from_bytes(data, dpi=300) # incomment to produce the bug
            # the following block correct the pdf2image bug
            pdf = pyvips.Image.new_from_buffer(data, "", dpi=300)
            n_pages = pdf.get_n_pages()
            for i in range(n_pages):
                vips_img = pyvips.Image.new_from_buffer(data, "", dpi=300, page=i)
                img_arr = vips_to_numpy(vips_img)
                plt.imshow(img_arr)
                plt.show()
        except Exception as e:
            log.error(e)
    return render_template('pdf2img.html')


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as err:
        log.critical(err)
