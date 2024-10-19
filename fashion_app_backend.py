from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from base64 import b64decode
from flask import Flask, send_file, url_for, redirect,request, render_template  
from werkzeug.utils import secure_filename
import os
import sqlite3



app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
DATABASE_FILENAME = "/Users/annabelleloh/Desktop/Comp Sci IA/database/Screenshot 2022-02-27 at 6.11.14 PM"
#app.secret.key = 'random secret'

#oauth = OAuth(app)
#google = oauth.register(
 #   name = 'google',
  #  client_id = '226621739167-rv920bjgu6744rvgcsrni0gv1vpcb3vm.apps.googleusercontent.com',
   # client_secret='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',
    #access_token_url='https://accounts.google.com/o/oauth2/token',
    #acess_token_params=None,
    #authorize_url='https://accounts.google.com/o/oauth2/auth',
    #authorize_params=None,
    #api_base_url='https://www.googleapls.com/oauth2/v1',
    #client_kwargs={'scope':'openid profile email'},
#)

@app.route("/",methods=['GET','POST'])
def index():
    return send_file("static/home/Home.html")

@app.route("/scan", methods=['GET'])
def scan():
     return send_file("test.html")
    
@app.route("/scan", methods=['POST'])
def scan_this_photo():
    f = request.files['image']
    name = os.path.join(app.root_path, secure_filename(f.filename))
    f.save(name)
    print("file name of photo: ",name)
    
    location = "/Users/annabelleloh/Desktop/Comp Sci IA/converted_keras (1)/keras_model.h5"
    model = load_model(location)

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(name)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image = image.convert("RGB")

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction)

    categories = ['ankleboot','bag','coat','dress','pullover','sandals','shirt','sneakers','tanks','tops','trousers']
    for item in prediction:
        print(item, type(item))
        highest = item.argmax(axis=0)
        result = categories [highest]
    print(result) 
    return redirect(url_for(result))

@app.route("/upload", methods=['GET'])
def upload_get():
    return render_template("uploadimage.html")
# secure_filename protects you from security risks associated with using a user-supplied filename.
@app.route("/upload", methods=['POST'])
def upload_post():
  
    ankleboots = 'Y' if 'ankle boots' in request.values else 'N'
    sneakers = 'Y' if 'sneakers' in request.values else 'N'
    sandals = 'Y' if 'sandals' in request.values else 'N'
    bag = 'Y' if 'bag' in request.values else 'N'
    coat = 'Y' if 'coat' in request.values else 'N'
    pullover = 'Y' if 'pullover' in request.values else 'N'
    dress = 'Y' if 'dress' in request.values else 'N'
    tops = 'Y' if 'tops' in request.values else 'N'
    tanks = 'Y' if 'tanks' in request.values else 'N'
    shirt = 'Y' if 'shirt' in request.values else 'N'
    trousers = 'Y' if 'trousers' in request.values else 'N'

    f = request.files['image']
    filename = os.path.join(app.root_path, secure_filename(f.filename))
    lastdot = filename.rfind(".")
    if filename[lastdot+1:] == "png" or filename[lastdot+1:] =="PNG" or filename[lastdot+1:] =="jpeg"or filename[lastdot+1:] =="JPEG" or filename[lastdot+1:] =="jpg" or filename[lastdot+1:] =="JPG": 
        f.save(filename) 
        
    else :
        return render_template("uploadimage.html", message="Invalid file type uploaded. Upload 'pdf' 'jpeg' or 'png'")       
    
    conn= sqlite3.connect(DATABASE_FILENAME) 
    cursor=conn.cursor()
    ok = cursor.execute('''INSERT INTO Clothingdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(filename, ankleboots, sneakers, sandals, bag, coat, pullover, dress, tops, tanks, shirt, trousers))
    print(ok)

    conn.commit()
    cursor.close()
    conn.close()
    return render_template("uploadimage.html")

@app.route("/ankleboots", methods=['GET'])
def ankleboots():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where ankleboots='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
  
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("ankleboots.html", images=rows)

@app.route("/sneakers", methods=['GET'])
def sneakers():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where sneakers='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("sneakers.html", images=rows)

@app.route("/sandals", methods=['GET'])
def sandals():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where sandals='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("sandals.html", images=rows)

@app.route("/bag", methods=['GET'])
def bag():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where bag='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("bags.html", images=rows)

@app.route("/coat", methods=['GET'])
def coat():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where coat='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("coats.html", images=rows)

@app.route("/pullover", methods=['GET'])
def pullover():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where pullover='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("pullover.html", images=rows)

@app.route("/dress", methods=['GET'])
def dress():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where dress='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("dress.html", images=rows)

@app.route("/tops", methods=['GET'])
def tops():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where tops='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("top.html", images=rows)

@app.route("/tanks", methods=['GET'])
def tanks():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where tanks='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("tank.html", images=rows)

@app.route("/shirt", methods=['GET'])
def shirt():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where shirt='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("shirt.html", images=rows)

@app.route("/trousers", methods=['GET'])
def trousers():
    conn= sqlite3.connect(DATABASE_FILENAME) 
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Clothingdata Where trousers='Y'")
    rows = [dict(record) for record in cursor.fetchall()]
    # /Users/annabelleloh/Desktop/Comp Sci IA/Users_annabelleloh_Desktop_Comp_Sci_IA_Screen_Shot_2021-10-21_at_11.27.46_AM.png
    for i in range(len(rows)):
        filename = rows[i]['filename']
        lastSlash = filename.rfind("/")
        filename = filename[lastSlash+1:]
        rows[i]['filename'] = filename
    return render_template("trousers.html", images=rows)

@app.route("/getphoto", methods=['GET'])
def getphoto():
   filename = request.values['filename']
   filename = secure_filename(filename)
   return send_file(filename)

# http://localhost/getphoto?filename=photo.jpg

     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 





