from Gallery.models import Photo
from flask import Blueprint,render_template ,flash ,request,render_template,jsonify, Flask, flash, request, redirect, url_for
from flask_login.utils import login_fresh, login_required
from . import app,db
from .models import Photo,Like
from werkzeug.utils import secure_filename
from flask_login import  current_user
import os ,json

views=Blueprint('views',__name__)


def check_file(filename):
     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
     return '.' in filename and filename.rsplit('.',1)[1].lower() in  ALLOWED_EXTENSIONS

@views.route('/post',methods=['GET','POST'])
@login_required
def post(): 
   if request.method=='POST':
     file=request.files['file'] # get the file 
     process_file(file)
   return render_template("upload_file.html",user=current_user)


def process_file(file):
    if file.filename== '':# if user didn'y select anyfile
        flash('Please select a file to upload',category='error')
    elif file and check_file(file.filename):# if the file is good
         filename=secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
         description=request.form.get('description')
         photo = Photo(description=description, path='static/'+filename,user_id=current_user.id)
         db.session.add(photo)
         db.session.commit()
         flash('you added your photo',category='success') 
    else:
          flash("Don't try something funny",category='error')     

@views.route('/our_post')
@login_required
def our_photo():
   photos=Photo.query.all()
   return render_template("our_photo.html",user=current_user,photos=photos,Like=Like)

@views.route('/add_like', methods=['POST'])
@login_required
def add_like():
    data = json.loads(request.data)
    print(data)
    photoId = data['photoId']
    like=Like.query.filter_by(photo_id=photoId,user_id=current_user.id).first()
    if like:
         flash("you can only like a picture once",category='error')
    else:
         like=Like(photo_id=photoId,user_id=current_user.id)
         db.session.add(like)
         db.session.commit()    
    return jsonify(
                    status=200
                )
