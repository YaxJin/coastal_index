from flask_bootstrap import Bootstrap5
from flask import Flask, render_template

app=Flask(__name__)

bootstrap = Bootstrap5(app)

classified_list = [
	{'filename':"type1.png",'Title':"海岸遊憩與日常生活(Shoreline and recreational activities)"},
	{'filename':"type2.png",'Title':"海上活動與船隻(Ocean/Waterway Activities)"},
	{'filename':"type3.png",'Title':"抽煙相關行為(Smoking-related activities)"},
	{'filename':"type4.png",'Title':"傾倒廢棄物(Dumping activities)"},
	{'filename':"type5.png",'Title':"醫療/個人衛生用品(Medical/Personal hygiene)"}
	]
action_img = [
	{'filename':"action1.png",'Title':"減少使用"},
	{'filename':"action2.png",'Title':"垃圾不落地"},
	{'filename':"action3.png",'Title':"參與淨灘"}
]
uploadScore = {"score":90, "rank":2, "total":22}

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
	return render_template('upload_result.html', result= uploadScore)

@app.route('/action')
def action():
	return render_template('action.html', img = action_img)

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