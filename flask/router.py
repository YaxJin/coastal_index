# from crypt import methods
from copyreg import pickle
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template,request
import os, pathlib
from werkzeug.utils import secure_filename
import time
from coast_image import CoastImage
import CNN_classifier_API_tflite as classiflier
import pickle

app=Flask(__name__)

bootstrap = Bootstrap5(app)

SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH, 'static', 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_name = "model.tflite"
loaded_model = classiflier.load_model(model_name)

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
	{"name":"臺北市","countcode":"A"},{"name":"新北市","countcode":"F"},{"name":"基隆市","countcode":"C"},
	{"name":"桃園市","countcode":"H"},{"name":"新竹縣","countcode":"J"},{"name":"新竹市","countcode":"O"},
	{"name":"苗栗縣","countcode":"K"},{"name":"臺中市","countcode":"B"},{"name":"彰化縣","countcode":"N"},
	{"name":"南投縣","countcode":"M"},{"name":"雲林縣","countcode":"P"},{"name":"嘉義市","countcode":"I"},
	{"name":"嘉義縣","countcode":"Q"},{"name":"臺南市","countcode":"D"},{"name":"高雄市","countcode":"E"},
	{"name":"屏東縣","countcode":"T"},{"name":"宜蘭縣","countcode":"G"},{"name":"花蓮縣","countcode":"U"},
	{"name":"臺東縣","countcode":"V"},{"name":"澎湖縣","countcode":"X"},{"name":"金門縣","countcode":"W"},
	{"name":"烈嶼","countcode":"W-1"},{"name":"連江縣","countcode":"Z"},{"name":"蘭嶼","countcode":"V-1"},
	{"name":"綠島","countcode":"V-2"},{"name":"其他地區","countcode":"Y"}
]

uploadScore = {"score":90, "rank":2, "total":22}


allImg = []
ranking = [{"location":"臺北市", "total_score": 0, "num_of_img": 0},
		{"location":"新北市", "total_score": 0, "num_of_img": 0},
		{"location":"桃園市", "total_score": 0, "num_of_img": 0},
		{"location":"臺中市", "total_score": 0, "num_of_img": 0},
		{"location":"臺南市", "total_score": 0, "num_of_img": 0},
		{"location":"高雄市", "total_score": 0, "num_of_img": 0},
		{"location":"宜蘭縣", "total_score": 0, "num_of_img": 0},
		{"location":"新竹縣", "total_score": 0, "num_of_img": 0},
		{"location":"苗栗縣", "total_score": 0, "num_of_img": 0},
		{"location":"彰化縣", "total_score": 0, "num_of_img": 0},
		{"location":"南投縣", "total_score": 0, "num_of_img": 0},
		{"location":"雲林縣", "total_score": 0, "num_of_img": 0},
		{"location":"嘉義縣", "total_score": 0, "num_of_img": 0},
		{"location":"屏東縣", "total_score": 0, "num_of_img": 0},
		{"location":"花蓮縣", "total_score": 0, "num_of_img": 0},
		{"location":"臺東縣", "total_score": 0, "num_of_img": 0},
		{"location":"澎湖縣", "total_score": 0, "num_of_img": 0},
		{"location":"基隆市", "total_score": 0, "num_of_img": 0},
		{"location":"新竹市", "total_score": 0, "num_of_img": 0},
		{"location":"嘉義市", "total_score": 0, "num_of_img": 0},
		{"location":"金門縣", "total_score": 0, "num_of_img": 0},
		{"location":"連江縣", "total_score": 0, "num_of_img": 0},
		{"location":"綠島", "total_score": 0, "num_of_img": 0},
		{"location":"蘭嶼", "total_score": 0, "num_of_img": 0},
		{"location":"烈嶼", "total_score": 0, "num_of_img": 0}
]

@app.route('/')
def rank():
	return render_template('rank.html', cityList = ranking)

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
			# upload image files
			f = request.files['file']
			filename = secure_filename(f.filename)
			save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			f.save(save_path)

			location = int(request.form.get('location')) # get location info
			location = location_list[location-1]['name']
			desc = request.form.get('desc') # get image description
			times = time.localtime() # get struct_time
			# time_string = time.strftime("%Y/%m/%d, %H:%M:%S", times)

			# Construct new CoastImage obj
			newImg = CoastImage(times, location, filename, None, desc=desc)
			# run prediction
			predictions, objs = classiflier.predict_trash(save_path, loaded_model)
			# mask_prediction(imgPath, predictions)
			score = classiflier.calculate_score(predictions)
			result = {"score": score, "objects": objs}

			# set prediction result 
			newImg.setResult(result)
			allImg.append(newImg)

			# print result for debugging
			# print(newImg.getTimeStamp())
			# print(newImg.getLoaction()) 
			# print(newImg.getImgName())
			# print(newImg.getDesc())
			# print(newImg.getResult())
			print(allImg)
			# print(ranking)

			# Pickling the data
			with open('data.pickle', 'wb') as file:
				pickle.dump(allImg, file)
		else:
			print("Error") # unknown
	elif request.method == 'GET':
		return render_template('upload.html', location = location_list)

	return render_template('upload_result.html', result = uploadScore)


@app.route('/result')
def result():
	return render_template('upload_result.html', result = uploadScore)


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