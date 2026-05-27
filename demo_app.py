from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
#testing security agent 1
app = Flask(__name__)
app.secret_key = 'demo-retail-secret-key-2026'

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    products = load_products()
    category = request.args.get('category', 'all')
    if category != 'all':
        products = [p for p in products if p['category'] == category]
    return render_template('index.html', products=products, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    products = load_products()
    items = []
    total = 0
    for item in cart_items:
        product = next((p for p in products if p['id'] == item['id']), None)
        if product:
            items.append({**product, 'quantity': item['quantity']})
            total += product['price'] * item['quantity']
    return render_template('cart.html', items=items, total=total)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    item = next((i for i in cart if i['id'] == product_id), None)
    if item:
        item['quantity'] += 1
    else:
        cart.append({'id': product_id, 'quantity': 1})
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [i for i in cart if i['id'] != product_id]
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    session['cart'] = []
    return render_template('checkout_PROD.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8500)
