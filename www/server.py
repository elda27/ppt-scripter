import sys
import os
import os.path
sys.path.append('../Source/')

from xml.sax.saxutils import escape
import uuid

# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from gpt import Presentation
from gpt import SafePresentation

app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
	title = 'Scripter'
	message = 'Hello!'
	# index.html をレンダリングする
	return render_template('index.html', message=message, title=title)

@app.route('/home')
def home():
	title = 'Scripter'
	message = 'Home!'
	# index.html をレンダリングする
	return render_template('index.html', message=message, title=title)

@app.route('/whatis')
def whatis():
	title = 'Scripter'
	message = 'Whatis!'
	# index.html をレンダリングする
	return render_template('index.html', message=message, title=title)

@app.route('/help')
def help():
	title = 'Scripter'
	message = 'Help!'
	# index.html をレンダリングする
	return redirect(url_for('index', anchor='help'))

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
	title = "こんにちは"
	if request.method == 'POST':
		# リクエストフォームから「名前」を取得して
		name = request.form['name']
		# index.html をレンダリングする
		return render_template('index.html', name=name, title=title)
	else:
		# エラーなどでリダイレクトしたい場合はこんな感じで
		return redirect(url_for('index'))

@app.route('/convert', methods=['GET', 'POST'])
def uploadFile():
	target_id = 'fileinputs'

	filelist = None
	if target_id in request.files:
		filelist = request.files.getlist(target_id)
	elif target_id in request.form:
		filelist = request.form.getlist(target_id)[0]
	else:
		print('Wrong format')
		return redirect(url_for('home'))
		
	print('Files:', filelist)
	note_dict = dict()

	for file in filelist:
		print(file)
		#file.save(path)
		#with open(path, 'rb') as fp:
		try:
			ppt = Presentation.Presentation(file.stream)
			notes = ppt.getNoteTexts()
			print_note = '\n'.join([escape('P.{0.Page}\n{0.Text}'.format(note)) for note in notes])
			print(print_note)
			note_dict[file.filename] = print_note
		except Exception as e:
			print(e)
			note_dict[file.filename] = 'Error:'
			continue

	return jsonify(notes = note_dict, uuid = uuid.uuid4().hex)

@app.errorhandler(404)
def NotFound(error):
	return redirect(url_for('home'))

def main():
	UPLOAD_FOLDER = '/uploads'
	ALLOWED_EXTENSIONS = set(['pptx'])

	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	app.run(host='0.0.0.0') # どこからでもアクセス可能に

if __name__ == '__main__':
	app.debug = True # デバッグモード有効化
	main()
