from flask_bootstrap import Bootstrap5
from flask import Flask, render_template

app=Flask(__name__)

bootstrap = Bootstrap5(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/intro')
def intro():
	return render_template('intro.html')

@app.route('/classified')
def classified():
	return render_template('classified.html')

@app.route('/rank')
def rank():
	return render_template('rank.html')
if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000',debug=True)