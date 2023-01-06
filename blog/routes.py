from blog import app
from flask import render_template, redirect, url_for, flash, Response, request
from blog.models import User, Post, Media, followers
from blog.forms import RegisterForm, LoginForm, postForm, userupdateForm, searchForm
from blog import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from sqlalchemy import or_

@app.route("/", methods=['GET','POST'])
@login_required
def home_page():
    form = postForm()
    if form.validate_on_submit():
        new_post = Post(created_by=current_user.id, post_title=form.post_title.data, post_text=form.post_text.data)
        db.session.add(new_post)
        db.session.commit()
        saver = form.post_picture.data
        if saver:
            pic_filename = secure_filename(saver.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            new_media = Media(post_id=new_post.id ,photo=pic_name)
            db.session.add(new_media)
            db.session.commit()
        flash("Your post have been uplaoded", category="success")
    img = Media.query.all()
    return render_template('dashboard.html', form = form, img=img)

@app.route("/search", methods=['GET','POST'])
@login_required
def search_page():
    form = searchForm()
    if form.validate_on_submit():
        users = User.query.filter(or_(User.username.like('%'+ form.search.data + '%'),User.fullname.like('%'+ form.search.data + '%'))).order_by(User.username).all()
        return render_template('search.html',form=form, user_data = users)
    return render_template('search.html',form=form)

@app.route('/<user>', methods=['GET','POST'])
def user_page(user):
    user_data = User.query.filter_by(username=user).first()
    if user_data:
        img = Media.query.all()
        return render_template('user.html', user = user_data, img=img)
    else:
        return render_template('404.html')

@app.route('/follow/<username>')
@login_required
def follow(username):
    users = User.query.filter_by(username=username).first()
    if users is None:
        flash('User %s not found.' % username)
        return redirect(url_for('home_page'))
    if users == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user_page', user=username))
    u = current_user.follow(users)
    if u is None:
        flash('You are already following ' + username + '.')
        return redirect(url_for('user_page', user=username))
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('user_page', user=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    users = User.query.filter_by(username=username).first()
    if users is None:
        flash('User %s not found.' % username)
        return redirect(url_for('home_page'))
    if users == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user_page', user=username))
    u = current_user.unfollow(users)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('user_page', user=username))

@app.route('/showfollowing/<username>')
@login_required
def showfollowing(username):
    users = User.query.filter_by(username=username).first()
    return render_template('following.html',user = users)

@app.route('/showfollowers/<username>')
@login_required
def showfollowers(username):
    users = User.query.filter_by(username=username).first()
    return render_template('followers.html',user = users)

@app.route('/updateUser', methods=['GET','POST'])
def updateUser_page():
    form = userupdateForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(username=form.username.data).count() < 2:
            user = User.query.filter_by(username = current_user.username).first()
            profile_pic = form.Profile_picture.data
            if profile_pic:
                pic_filename = secure_filename(profile_pic.filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                user.profilePicture = pic_name
            user.fullname = form.fullname.data
            user.username=form.username.data
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
        flash("Account Updated.", category="success")
        return redirect(url_for('home_page'))
    return render_template('updateuser.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(username=form.username.data).count() < 1:
            new_user = User(username=form.username.data,
                        fullname=form.fullname.data,
                        email = form.email.data,
                        password = form.password1.data)
            db.session.add(new_user)
            db.session.commit()
            db.session.add(new_user.follow(new_user))
            db.session.commit()
            flash("Your account has been created, You may login now", category="success")
            return redirect(url_for('login_page'))
        else:
            flash("Username Already exists", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html', form = form)

@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.passwordCheck(givenPassword = form.password.data):
            login_user(attempted_user)
            return redirect(url_for('home_page'))
    return render_template('login.html', form = form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been Logged out", category='info')
    return redirect(url_for('login_page'))

@app.route("/delPost/<int:id>")
def deletepost(id):
    post = Post.query.filter_by(id=id).first()
    media = Media.query.filter_by(post_id=id).first()
    if post.created_by == current_user.id:
        db.session.delete(media)
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted", category="success")
        return redirect(url_for('user_page', user=current_user.username))

@app.route("/editPost/<int:id>", methods=['GET','POST'])
def editpost(id):
    form = postForm()
    post = Post.query.filter_by(id = id).first()
    if form.validate_on_submit():
        if post.created_by == current_user.id:
            post_pic = form.post_picture.data
            if post_pic:
                media = Media.query.filter_by(post_id=id).first()
                if media:
                    db.session.delete(media)
                    db.session.commit()
                pic_filename = secure_filename(post_pic.filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                post_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                new_media = Media(post_id=post.id ,photo=pic_name)
                db.session.add(new_media)
                db.session.commit()
        post.post_title = form.post_title.data
        post.post_text=form.post_text.data
        db.session.commit()
        flash("Post Updated.", category="success")
        return redirect(url_for('user_page', user=current_user.username))
    return render_template('updatepost.html', form = form, post = post)
