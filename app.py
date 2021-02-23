from flask import Flask, request, url_for, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/PassionFroid'

mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        recherche = request.form.get("recherche")
        type = request.form.get("type")
        humain = request.form.get("humain")
        institutionelle = request.form.get("institutionelle")
        format = request.form.get("format")
        if recherche:
            products = mongo.db.PassionFroid.find({"$or": [{"titre": {"$regex": recherche}}, {"tag": {"$regex": recherche}}]})




    else:
        products = mongo.db.PassionFroid.find()

    return render_template('home.html', products=products)

@app.route('/newProduct')
def newProduct():
    return render_template('newProduct.html')

@app.route('/uploadProduct', methods=['POST'])
def createProduct():
    titre = request.form.get("title")
    type = request.form.get("type")
    humain = request.form.get("humain")
    institutionelle = request.form.get("institutionelle")
    format = request.form.get("format")
    credits = request.form.get("credits")
    droit_limite = request.form.get("droit_limite")
    copyright = request.form.get("copyright")
    copyright_date = request.form.get("copyright_date")
    tag = request.form.getlist("tag[]")

    if 'productImage[]' in request.files:
        productImage = request.files.getlist('productImage[]')
        for productImage in productImage:
            mongo.save_file(productImage.filename, productImage)
            mongo.db.PassionFroid.insert({'productImage_name': productImage.filename,
                                          'titre': titre,
                                          'type': type,
                                          'humain': humain,
                                          'institutionelle': institutionelle,
                                          'format': format,
                                          'credit': credits,
                                          'droit_limite': droit_limite,
                                          'copyright': copyright,
                                          'copyright_date': copyright_date,
                                          'tag': tag
                                          })
    return render_template('newProduct.html')


@app.route('/product_image/<filename>')
def product(filename):
    return mongo.send_file(filename)

@app.route('/product/<product>')
def render(product):
    product = mongo.db.PassionFroid.find_one({'productImage_name': product})
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)