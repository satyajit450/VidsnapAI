from flask import Flask, render_template,request
import uuid
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER ='user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET","POST"])
def create():
    my_id = uuid.uuid1()
    input_files = []    
    if request.method   == "POST" :
        print(request.files.keys())   # isse upload ke data mil jayange
        rec_id = request.form.get("uuid")  # isse ak unique id mil jayega
        desc = request.form.get("text")    #jo humlog text area me likhenge yaha pe show hoga (like a white box)
        for key,value in request.files.items():
            print(key,value)
            #upload the file
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, filename))
            #capture the description and save it to a file
                input_files.append(file.filename)
                print(file.filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"),"w") as f:
            f.write(desc)
    for fl in input_files:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,"input.txt"),"a") as f:    # file 'user_uploads/d658c606-d2c5-11f0-a04c-fe57aa71bd8e/Screenshot 2025-11-29 110536.png'duration 1 aise store hoga  
            f.write(f"file '{fl}'\nduration 1\n")

    return render_template("create.html",my_id = my_id)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html",reels = reels)

app.run(debug=True)
