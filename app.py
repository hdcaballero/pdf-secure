from flask import Flask, request, jsonify, render_template
from json import dumps
from flask_restful  import Resource, Api
from PyPDF2 import PdfFileReader, PdfFileWriter
from base64 import b64encode, encodebytes, encodestring
from werkzeug.datastructures import FileStorage
import os
import json

app = Flask(__name__)
PASSWORD = '123456'


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

api = Api(app)

@app.route('/')
def home():
   return render_template('home.html')


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
         with open('ResumendeTarjetas.pdf', 'rb') as file:             
             #data=  FileStorage(file).read()
             data['filename'] = 'ResumendeTarjetas.pdf'
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
