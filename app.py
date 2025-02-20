
from flask import Flask, request, make_response, render_template, flash,jsonify, session
from flask import make_response
import pandas as pd
import os
app = Flask(__name__, template_folder='templates',static_folder='static', static_url_path='/')
app.config["IMAGE_UPLOADS"] = "images/"
app.secret_key = "SOME KEY"
@app.route('/')
def index():
    #return "<h1>Hello World</h1>"
    greet = 'hello'
    name = 'Shan'
    list = ['Pen', 'Pencil', 'Eraser']
    return render_template('index.html',greet=greet, name=name, list=list)

@app.route('/set_data')
def set_data():
    session['name'] = 'Mike'
    session['other'] = 'Hello World'
    return render_template('index.html',message='Session Data Set')
@app.route('/get_data')
def get_data():
    if 'name' in session.keys():
        return render_template('index.html',message=f'Name: {session["name"]}, Other: {session["other"]}')
@app.route('/clear_session')
def clear_session():
    session.clear()
    #session.pop('name') #for clearing particular key
    return render_template('index.html', message='Session Data cleared')
@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html',message='Cookie Set'))
    response.set_cookie('cookie_name','cookie_value')
    return response
@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies['cookie_name']
    return render_template('index.html',message=f'Cookie value {cookie_value}')
@app.route('/remove_cookie')
def remove_cookie():
    response = make_response(render_template('index.html', message='Cookie Removed'))
    response.set_cookie('cookie_name', expires=0)
    return response
@app.route('/about_us')
def about_us():
    filters="Filters"
    return render_template('about.html',filters=filters)
@app.route('/hello')
def hello():
    response = make_response()
    response.status_code = 202
    response.headers['content-type']='application/octet-stream'
    return response
#parameter passed to endpoint
@app.route('/greet/<name>')
def greet(name):
    return f"Hello {name}"

@app.route('/handle_urls')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return str(request.args)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')
    if request.method == 'POST':
        if 'login_id' in request.form.keys():
            login_id = request.form['login_id']
            login_pwd = request.form.get('login_pwd')
        if login_id == 'shan' and login_pwd== '123':
            return 'Login Success'
        else:
            return 'Login Failure'
    return 'form'
@app.route('/file_upload',methods=['POST'])
def file_upload():

    file = request.files['uploaded_file']
    #return file.content_type
    if file.content_type == 'text/plain' or file.content_type == 'images/*':
        return file.read().decode()
    if file.content_type == 'application/vnd.ms-excel' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
        return df.to_html()
    if file.content_type == 'image/jpeg' or file.content_type == 'image/jpg' or file.content_type == 'image/png':
        #return file.filename
        file.save(os.path.join("static/",app.config["IMAGE_UPLOADS"], file.filename))
        filename = os.path.join(app.config["IMAGE_UPLOADS"], file.filename)
        #return str("stored as:" + filename)
        #return str('<img src="/'+filename+'">')
        #return file.filename
        return render_template("login_form.html", uploaded_image=filename)


@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]
@app.route('/handle_post', methods=['POST'])#for JSON data
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']
    with open('file.txt','w') as f:
        f.write(f'{greeting}, {name}')
    return jsonify({'message':'Successfully Written'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555, debug=True)
