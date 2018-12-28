from flask import Flask, request, jsonify, render_template,flash
from json import dumps
from flask_restful  import Resource, Api
from PyPDF2 import PdfFileReader, PdfFileWriter
from base64 import b64encode, encodebytes, encodestring
import os
import json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
PASSWORD = '123456'


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

api = Api(app)

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])    
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)    
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']                
    return render_template('home.html', form=form)


class PDF_Files(Resource):
    def post(self):
        print('this is the JSON request')
        print(request.files)
        print(request.json)
        if 'file' not in request.files:
            print('No file part')
        else:
            print('file part found')         
        file = request.files['file']         
        file.save(os.path.join( file.filename))        
        result = {'status':'success'}
        pdf_reader = PdfFileReader(file)
        pdf_writer = PdfFileWriter()        
 
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
 
        pdf_writer.encrypt(user_pwd=PASSWORD, owner_pwd=None,use_128bit=True)
        with open('encrypted_' + file.filename, 'wb') as fh:
            pdf_writer.write(fh)
        #return jsonify(result)
        #return jsonify({'pdf': b64encode(file.read())})
        return jsonify(encodestring(file.read()).decode('ascii'))

    
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
        

api.add_resource(PDF_Files,'/pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
