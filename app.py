from flask import Flask, request, url_for, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/PassionFroid'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/newProduct')
def newProduct():
    return render_template('newProduct.html')

@app.route('/uploadProduct', methods=['POST'])
def createProduct():
    if 'productImage' in request.files:
        productImage = request.files['productImage']
        mongo.save_file(productImage.filename, productImage)
        mongo.db.PassionFroid.insert({'productImage_name': productImage.filename})
    return render_template('newProduct.html')


@app.route('/product_image/<filename>')
def product(filename):
    return mongo.send_file(filename)

@app.route('/product/<filename>')
def render(filename):
    filename = mongo.db.PassionFroid.find_one({'productImage_name': filename})
    return render_template('product.html', filename=filename['productImage_name'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)