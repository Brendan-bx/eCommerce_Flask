from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    return render_template('market.html', item_name = [{'id' :1, 'name':'Mobile', 'barcode':'12345679012', 'price':'500'},
                                                     {'id' :2, 'name':'Laptop', 'barcode':'12345679013', 'price':'1000'},
                                                     {'id' :3, 'name':'Earphone', 'barcode':'12345679014', 'price':'200'}])



if __name__ == '__main__':
    app.run(debug=True)