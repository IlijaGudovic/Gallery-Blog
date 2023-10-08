from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

import base64

from . import db

from .models import User, Section, Photo

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():

    users = User.query.all()

    profile = None

    if current_user.is_authenticated:
        profile = current_user.username

    return render_template("home.html", users = users, profile = profile)


@views.route('/profile/<username>', methods = ['GET', 'POST'])
def profile(username):

    user = User.query.filter_by(username = username).first()

    if not user:
        return username + " not found"

    request_methods(None)
        
    sections = Section.query.filter_by(author = user.id)

    return render_template("profile.html", user = user, sections = sections, guest = current_user)

@views.route('/profile/<username>/<name>', methods = ['GET', 'POST'])
def folder(username, name):

    user = User.query.filter_by(username = username).first()

    if not user:
        return username + " not found"
    
    section = Section.query.filter_by(author = user.id, name = name).first()

    if not section:
        flash(username + " have no section " + name)

        return redirect(url_for('views.profile', username = username))   
     
    request_methods(name)

    sections = Section.query.filter_by(author = user.id)

    images = []

    for image in Photo.query.filter_by(folder = section.id):
        images.append (image.data)

    titels = []

    for image in Photo.query.filter_by(folder = section.id):
        titels.append(image.description)


    base64_images = [base64.b64encode(image).decode("utf-8") for image in images]

    return render_template("photos.html", user = user, sections = sections, guest = current_user, selected = section, images=base64_images, count = len(images), size = int(len(images)/3), titels = titels)


def request_methods(selected):

    if request.method == 'POST':

        if request.form['btn'] == 'section':

            section_name = request.form.get('section_name')

            if not section_name:
                flash("Empty section name")
            else:

                names = []

                for s in Section.query.filter_by(author = current_user.id):
                    names.append(s.name)

                if section_name not in names:

                    new_section = Section(name = section_name, author = current_user.id)
                    db.session.add(new_section)
                    db.session.commit()

                    print(section_name)

                else:
                    flash("Section alredy exist")

        elif request.form['btn'] == 'photo':

            photo_description = request.form.get('photo_description')
            
            file = request.files['file']

            if not selected:
                flash("no selection")

            elif not file:
                flash('no file part')

            else:

                selected_section = Section.query.filter_by(author = current_user.id, name = selected).first()

                if selected_section:
                    new_photo = Photo(description = photo_description, data = file.read(), folder = selected_section.id)
                    db.session.add(new_photo)
                    db.session.commit()
                
                else:

                    flash(selected + " not found")


        elif request.form['btn'] == 'delete':

            delete_name = request.form.get('delete_name')

            if not delete_name:
                flash("Nhoting selected")
            else:

                names = []

                for s in Section.query.filter_by(author = current_user.id):
                    names.append(s.name)

                if delete_name in names:

                    section = Section.query.filter_by(name = delete_name).first()

                    Photo.query.filter_by(folder = section.id).delete()

                    db.session.delete(section)
                    db.session.commit()

                    print(delete_name)

                else:
                    flash(delete_name + " not found")

