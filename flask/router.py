# from crypt import methods
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template,request, redirect, url_for
import os, pathlib
from werkzeug.utils import secure_filename
import time
from coast_image import CoastImage
import CNN_classifier_API_tflite as classiflier # comment out if no tensorflow
import pickle
from math import exp
import threading

sem = threading.Semaphore()

app=Flask(__name__)

bootstrap = Bootstrap5(app)

SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH, 'static', 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_name = "model.tflite"
loaded_model = classiflier.load_model(model_name) # comment out if no tensorflow

classified_list = [
	{'filename':"type1.png", 'Title':"海岸遊憩與日常生活", "Eng":"Shoreline and recreational activities"},
	{'filename':"type2.png", 'Title':"海上活動與船隻", "Eng":"Ocean/Waterway Activities"},
	{'filename':"type3.png", 'Title':"抽煙相關行為", "Eng":"Smoking-related activities"},
	{'filename':"type4.png", 'Title':"傾倒廢棄物", "Eng":"Dumping activities"},
	{'filename':"type5.png", 'Title':"醫療/個人衛生用品", "Eng":"Medical/Personal hygiene"}
	]

action_img = [
	{'filename':"action1.png",'Title':"減少使用"},
	{'filename':"action2.png",'Title':"垃圾不落地"},
	{'filename':"action3.png",'Title':"參與淨灘"}
]

location_list = [
	{"name":"臺北","countcode":"A"},{"name":"基隆市","countcode":"C"},
	{"name":"桃園市","countcode":"H"},{"name":"新竹縣","countcode":"J"},{"name":"新竹市","countcode":"O"},
	{"name":"苗栗縣","countcode":"K"},{"name":"臺中市","countcode":"B"},{"name":"彰化縣","countcode":"N"},
	{"name":"雲林縣","countcode":"P"},
	{"name":"嘉義","countcode":"Q"},{"name":"臺南市","countcode":"D"},{"name":"高雄市","countcode":"E"},
	{"name":"屏東縣","countcode":"T"},{"name":"宜蘭縣","countcode":"G"},{"name":"花蓮縣","countcode":"U"},
	{"name":"臺東縣","countcode":"V"},{"name":"澎湖縣","countcode":"X"},{"name":"金門縣","countcode":"W"},
	{"name":"連江縣","countcode":"Z"},{"name":"蘭嶼","countcode":"V-1"},
	{"name":"綠島","countcode":"V-2"},{"name":"其他地區","countcode":"Y"}
]

uploadScore = {"score": 0, 
				"rank": 0, 
				"total": 0, 
				"location": "", 
				"time": "", 
				"desc": "", 
				"img": ""
				}

# load allImg pickle data if exist
if os.path.exists('allImg.pickle'):
	with open('allImg.pickle', 'rb') as file:
		allImg = pickle.load(file) 
else:
	allImg = []

# load ranking pickle data if exist
if os.path.exists('ranking.pickle'):
	with open('ranking.pickle', 'rb') as file:
		ranking = pickle.load(file)	
else:
	ranking = [{"location":"臺北", "total_score": 0, "num_of_img": 0},
		#{"location":"新北市", "total_score": 0, "num_of_img": 0},
		{"location":"桃園市", "total_score": 0, "num_of_img": 0},
		{"location":"臺中市", "total_score": 0, "num_of_img": 0},
		{"location":"臺南市", "total_score": 0, "num_of_img": 0},
		{"location":"高雄市", "total_score": 0, "num_of_img": 0},
		{"location":"宜蘭縣", "total_score": 0, "num_of_img": 0},
		{"location":"新竹縣", "total_score": 0, "num_of_img": 0},
		{"location":"苗栗縣", "total_score": 0, "num_of_img": 0},
		{"location":"彰化縣", "total_score": 0, "num_of_img": 0},
		# {"location":"南投縣", "total_score": 0, "num_of_img": 0},
		{"location":"雲林縣", "total_score": 0, "num_of_img": 0},
		{"location":"嘉義", "total_score": 0, "num_of_img": 0},
		{"location":"屏東縣", "total_score": 0, "num_of_img": 0},
		{"location":"花蓮縣", "total_score": 0, "num_of_img": 0},
		{"location":"臺東縣", "total_score": 0, "num_of_img": 0},
		{"location":"澎湖縣", "total_score": 0, "num_of_img": 0},
		{"location":"基隆市", "total_score": 0, "num_of_img": 0},
		{"location":"新竹市", "total_score": 0, "num_of_img": 0},
		#{"location":"嘉義市", "total_score": 0, "num_of_img": 0},
		{"location":"金門縣", "total_score": 0, "num_of_img": 0},
		{"location":"連江縣", "total_score": 0, "num_of_img": 0},
		{"location":"綠島", "total_score": 0, "num_of_img": 0},
		{"location":"蘭嶼", "total_score": 0, "num_of_img": 0}
		# {"location":"烈嶼", "total_score": 0, "num_of_img": 0}
	]

@app.before_request
def refresh_data():
	# get current time
	currentTime = time.localtime()
	currYear = currentTime.tm_year
	currMonth = currentTime.tm_mon

	# delcare global variable for modification
	global ranking, allImg

	# clear all total score for refreshing
	newRank = ranking.copy()
	for i in newRank:
		i['total_score'] = 0
		
	# loop through every image to update credibility
	for img in allImg:
		month = img.getTimeStamp().tm_mon
		year = img.getTimeStamp().tm_year
		time_diff = (currYear - year) * 12 + (currMonth - month)
		credibility = exp(-time_diff * 0.185) # 10% credibility after 1 year
		img.setCredibility(credibility)
		for city in newRank:
			if city['location'] == img.getLoaction():
				city['total_score'] += img.getResult()['score']*img.getCredibility()

	# Sort updated data
	allImg = sorted(allImg, key=lambda x : x.getResult()["score"]*x.getCredibility(), reverse=True)
	newRank = sorted(newRank, key=lambda x : x['total_score']/x['num_of_img'] if x['num_of_img'] > 0 else x['total_score'], reverse=True)
	ranking = newRank

	# Pickling ranking and allImg data
	with open('allImg.pickle', 'wb') as file:
		pickle.dump(allImg, file)
	with open('ranking.pickle', 'wb') as file:
		pickle.dump(ranking, file)


@app.route('/')
def rank():
	return render_template('rank.html', cityList = ranking, imgList=allImg)

@app.route('/classified')
def classified():
	return render_template('classified.html', classified_list = classified_list)

# @app.route('/intro')
# def intro():
# 	return render_template('intro.html')

@app.route('/action')
def action():
	return render_template('action.html', img = action_img)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if request.form.get('Upload') == 'Upload':
			sem.acquire()
			# get struct_time
			times = time.localtime()
			time_string = time.strftime("%Y%m%d_%H%M%S", times)

			# upload image files
			f = request.files['file']
			filename = time_string + "_" + secure_filename(f.filename)
			save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			f.save(save_path)

			# get location info
			location = int(request.form.get('location'))
			location = location_list[location-1]['name']
			# get image description
			desc = request.form.get('desc')

			# Construct new CoastImage obj
			newImg = CoastImage(times, location, filename, {"score": 0, "objects": None}, desc=desc)

			# run prediction, comment out if no tensorflow
			predictions, objs = classiflier.predict_trash(save_path, loaded_model)
			score = classiflier.calculate_score(predictions)
			result = {"score": score, "objects": objs}

			# set prediction result 
			newImg.setResult(result)

			# store to allImg and sort by score
			global allImg
			allImg.append(newImg)
			allImg = sorted(allImg, key=lambda x : x.getResult()["score"]*x.getCredibility(), reverse=True)

			# update ranking info and sort by score
			global ranking
			for city in ranking:
				if city['location'] == newImg.getLoaction():
					city['total_score'] += newImg.getResult()['score']
					city['num_of_img'] += 1
			
			ranking = sorted(ranking, key=lambda x : x['total_score']/x['num_of_img'] if x['num_of_img'] > 0 else x['total_score'], reverse=True)
			
			# print result for debugging
			#for img in allImg:
			#	print(img.getTimeStamp())
			#	print(img.getLoaction()) 
			#	print(img.getImgName())
			#	print(img.getResult()["score"])
			#	print(img.getDesc())
			# print(ranking)

			# Pickling allImg data
			with open('allImg.pickle', 'wb') as file:
				pickle.dump(allImg, file)
			# Pickling ranking data
			with open('ranking.pickle', 'wb') as file:
				pickle.dump(ranking, file)
		else:
			print("Error") # unknown
	elif request.method == 'GET':
		sem.release()
		return render_template('upload.html', location = location_list)

	# create uploadScore for result page
	display_time = time.strftime("%Y/%m/%d", times)
	global uploadScore
	uploadScore = {"score": newImg.getResult()["score"], 
				"rank": allImg.index(newImg)+1, 
				"total":len(allImg), 
				"location": newImg.getLoaction(), 
				"time": display_time, 
				"desc": newImg.getDesc(), 
				"img": newImg.getImgName()
				}
	sem.release()
	return redirect(url_for('result'))


@app.route('/result')
def result():
	return render_template('upload_result.html', result = uploadScore)

@app.route('/about')
def about():
	return render_template('aboutUS.html')


@app.route('/404')
def error():
	return render_template('404.html')


@app.route('/more')
def more():
	return render_template('more.html')

@app.route('/intro')
def intro():
	return render_template('intro.html')

@app.route('/process')
def process():
	return render_template('process.html')

@app.route('/rule')
def rule():
	return render_template('rule.html')


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


##### debug #####

@app.route('/test')
def test():
	return render_template('(x)test.html')



if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0',port='8080',debug=True)
