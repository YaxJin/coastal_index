# from crypt import methods
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template,request
import os, pathlib
from werkzeug.utils import secure_filename

app=Flask(__name__)

bootstrap = Bootstrap5(app)

SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

location_list = [
	{"name":"臺北市"},{"name":"新北市"},{"name":"桃園市"},{"name":"臺中市"},{"name":"臺南市"},
	{"name":"高雄市"},{"name":"宜蘭縣"},{"name":"新竹縣"},{"name":"苗栗縣"},{"name":"彰化縣"},{"name":"南投縣"},
	{"name":"雲林縣"},{"name":"嘉義縣"},{"name":"屏東縣"},{"name":"花蓮縣"},{"name":"臺東縣"},{"name":"澎湖縣"},
	{"name":"基隆市"},{"name":"新竹市"},{"name":"嘉義市"},{"name":"金門縣"},{"name":"連江縣"},{"name":"釣魚臺列嶼"},
	{"name":"龜山島"},{"name":"東沙群島"},{"name":"南沙群島太平島"},{"name":"中洲礁"},{"name":"其他地區"}
]

uploadScore = {"score":90, "rank":2, "total":22}



@app.route('/')
def rank():
	return render_template('rank.html')

@app.route('/classified')
def classified():
	return render_template('classified.html', classified_list = classified_list)

@app.route('/intro')
def intro():
	return render_template('intro.html')

@app.route('/action')
def action():
	return render_template('action.html', img = action_img)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if request.form.get('Upload') == 'Upload':
			print(request.files)
			f = request.files['file']
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			l = int(request.form.get('location'))
			desc = request.form.get('desc')
		else:
			print("Error") # unknown
	elif request.method == 'GET':
		return render_template('upload.html',location = location_list)

	return render_template('upload_result.html', result= uploadScore)

@app.route('/result')
def result():
	return render_template('upload_result.html', result= uploadScore)


@app.route('/404')
def error():
	return render_template('404.html')


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


##### debug #####
@app.route('/test',methods={'POST','GET'})
def test():
	return render_template('(x)test.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8080',debug=True)