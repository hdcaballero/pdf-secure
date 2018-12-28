from flask import Flask, request, jsonify, render_template
from json import dumps
from flask_restful  import Resource, Api
from PyPDF2 import PdfFileReader, PdfFileWriter
from base64 import b64encode, encodebytes, encodestring
from werkzeug.datastructures import FileStorage

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
         with open('ResumendeTarjetas.pdf', 'rb') as file:             
             data=  FileStorage(file).read()
             print(data)
         return jsonify(encodestring(data).decode('ascii'))
        

api.add_resource(PDF_Files,'/pdf')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5555, True)