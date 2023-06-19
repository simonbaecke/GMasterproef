import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, session
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = r'C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\Flask_webserver\private'
ALLOWED_EXTENSIONS = {'bpmn','txt','json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'dd793de789f6df5210f233ce4a83f92d'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
def process_file(file_path):
    # Perform your script action on the file
    # For example, let's assume you want to convert the file to uppercase
    with open(file_path, 'r') as f:
        content = f.read().upper()
    with open(file_path, 'w') as f:
        f.write(content)
"""
        
def process_file(file_path):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Find IDs with null values
    null_ids = [item['id'] for item in data if item['value'] is None]

    # Return the data and null IDs
    return data, null_ids

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files.get('file')
        if file and allowed_file(file.filename) is False:
            return render_template('index.html', message='File type not supported')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            session['file_path'] = file_path

            # Process the file and get the data and null IDs
            data, null_ids = process_file(file_path)

            with open(file_path, 'r') as f:
                file_content = f.read()

            return render_template('index.html', message='File uploaded successfully', filename=filename)

    return render_template('index.html')

@app.route('/input', methods=['GET','POST'])
def input():
    file_path = session.get('file_path')  # Retrieve file_path from the session

    # If file_path is not available in the session, redirect back to the upload page
    if not file_path:
        return redirect(url_for('upload_file'))

    # Process the file and get the data and null IDs
    data, null_ids = process_file(file_path)

    with open(file_path, 'r') as f:
        file_content = f.read()
    return render_template('input.html', file_content=file_content, data=data, null_ids=null_ids)


@app.route('/bpmn', methods=['GET','POST'])
def bpmn():
    return render_template('bpmn.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__':
    app.run(debug=True)
