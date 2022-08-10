from flask_bootstrap import Bootstrap5
from flask import Flask, render_template

app=Flask(__name__)

bootstrap = Bootstrap5(app)

classified_list = [
	{'filename':"type1.png",'Title':"海岸遊憩與日常生活(Shoreline and recreational activities)"},
	{'filename':"ocean.jpg",'Title':"海上活動與船隻(Ocean/Waterway Activities)"},
	{'filename':"ocean.jpg",'Title':"抽煙相關行為(Smoking-related activities)"}
	]

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/intro')
def intro():
	return render_template('intro.html')

@app.route('/classified')
def classified():
	return render_template('classified.html', classified_list = classified_list)

@app.route('/rank')
def rank():
	return render_template('rank.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/result')
def result():
	return render_template('upload_result.html')

@app.route('/action')
def action():
	return render_template('action.html')

@app.route('/404')
def error():
	return render_template('404.html')
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


##### debug #####
@app.route('/test')
def test():
	return render_template('test.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8000',debug=True)