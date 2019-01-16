from flask import Flask, request, jsonify, render_template,flash, redirect, url_for
from json import dumps
from flask_restful  import Resource, Api
from PyPDF2 import PdfFileReader, PdfFileWriter
from base64 import b64encode, encodebytes, encodestring
from werkzeug.utils import secure_filename
import os
import json
import socket
import datetime
from flask_wtf import FlaskForm 
from wtforms import TextField, validators, ValidationError, PasswordField
from flask_wtf.file import FileField, FileRequired

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf'])
UPLOAD_FOLDER =  os.path.dirname('__file__')
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'static')
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'uploads')

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = '/uploads'


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

api = Api(app)

class UploadForm(FlaskForm):     
    password = PasswordField(label ='Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    uploaded_file =  FileField(validators=[FileRequired()])


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)    
    print(UPLOAD_FOLDER)    
    if request.method == "POST":                
        file_url=encrypt_file(request.files['uploaded_file'], request.form['password']  )      
        print(request.form['password']  )
    else:
        file_url = None
    return render_template('home.html', form=form, file_url=file_url)


class PDF_Files(Resource):
    def post(self):                
        print(request.form['password']  )
        data={}
        if 'uploaded_file' not in request.files:
            print('No file part')
        else:
            print('file part found')         
        file = request.files['uploaded_file']         
        #file.save(os.path.join( file.filename))        
        result = {'status':'success'}
        encrypt_file(file, request.form['password'] )

        with open('encrypted_'+ file.filename, 'rb') as encrypted_file:      
            data['filename'] = 'encrypted_'+ file.filename
            file_read= encrypted_file.read()
        
        file_64_encode = encodebytes(file_read)         
        data['data'] = file_64_encode.decode('ascii')          

        final_data = json.dumps(data)
        final_data = json.loads(final_data)
        return final_data
    
    def get(self):
         data={}
         with open('encrypted_Eldridge. Willie P. TX-EB-SIGNED.pdf', 'rb') as file:                          
             data['filename'] = 'encrypted_Eldridge. Willie P. TX-EB-SIGNED.pdf'
             file_read= file.read()
         file_64_encode = encodebytes(file_read)         
         data['data'] = file_64_encode.decode('ascii')          

         final_data = json.dumps(data)
         final_data = json.loads(final_data)

         return final_data
        
def encrypt_file(file, password):
    pdf_reader = PdfFileReader(file)
    pdf_writer = PdfFileWriter()        
 
    

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
 
    pdf_writer.encrypt(user_pwd=password, owner_pwd=None,use_128bit=True)
    file_location = os.path.join(UPLOAD_FOLDER, 'encrypted_' + file.filename)
    with open(file_location , 'wb') as fh:
        pdf_writer.write(fh)
    a = os.path.getsize(file_location)
    save_log(file.filename,str(a))
    return url_for('static', filename= 'uploads/encrypted_' + file.filename)  
    
 
api.add_resource(PDF_Files,'/pdf')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_log(filename,filesize):
    now = datetime.datetime.now()
    f = open("static/uploads/encryptLog.txt", "a")
    f.write('\n' + now.strftime("%x") + ' ' + now.strftime("%X") + ' - ' + filename + ' - ' + filesize + ' - '+ getIp())
    return ''



def getIp():
    nameeqp = socket.gethostname()
    ipeqp = socket.gethostbyname(nameeqp)
    return ipeqp

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
