from flask_restful import Resource, reqparse
from server.model.userModel import UserModel
from werkzeug.security import generate_password_hash
from flask import Response, session, jsonify, render_template, flash, url_for, redirect, make_response, request
import json
from server.auth import authenicate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from server.mail import send_mail
from flask_login import login_user, logout_user, \
    login_required, current_user
from server.mail.email_token import generate_confirmation_token, confirm_token
from datetime import datetime
import pytz
from flask_cors import cross_origin
from .form import LoginForm, RegisterForm, ChangePasswordForm, ForgotForm
from server.util import extractNumber
from server.mail import check_confirmed


class UserRegisterRoute(Resource):
    def get(self):
        form = RegisterForm()
        html = render_template('user/register.html', form=form)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)
    def post(self):
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = UserModel(username=form.username.data,
                             password= generate_password_hash(form.password.data),
                             name=form.name.data,
                             email=form.email.data,
                             phone=extractNumber(form.phoneNumber.data),
                             confirmed=False
                             )

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('index_bp.userconfirmemailroute', token=token, _external=True)
            html = render_template('user/activate.html', confirm_url=confirm_url, user_name=user.name)
            message = "Confirm Your email address"
            user.save_to_db()
            login_user(user)
            send_mail(user.email, message, html)
            return redirect(url_for("index_bp.unconfirmed"))
        headers = {'Content-Type': 'text/html'}
        html = render_template('user/register.html', form=form)
        return make_response(html, 200, headers)

class UserLoginRoute(Resource):
    def get(self):
        form = LoginForm()
        html = render_template('user/login.html', form=form)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)

    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = authenicate(username=form.username.data, password=form.password.data)
            if not user:
                flash("username or password is incorrect","error")
                html = render_template('user/login.html', form=form)
                headers = {'Content-Type': 'text/html'}
                return make_response(html, 200, headers)
            userObj = {
                'username': form.username.data,
                'user_id': user.id
            }
            login_user(user, remember=True)
            access_token = create_access_token(identity=userObj)
            jsonResponse = jsonify(access_token=access_token, user_id=user.id)
            return redirect(url_for('index_bp.profile'))
        html = render_template('user/login.html', form=form)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)

class Profile(Resource):
    @login_required
    @check_confirmed
    def get(self):
        flash("You have successful login" ,"success")
        html = render_template('user/profile.html')
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)



class UserConfirmEmailRoute(Resource):
    @cross_origin(origins='*')
    @login_required
    def get(self,token):
        if current_user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        email = confirm_token(token)
        user = UserModel.find_by_email(_email=current_user.email)
        if user.email == email:
            user.confirmed = True
            user.confirmed_on = datetime.now()
            user.save_to_db()
            message = 'You are in, ' + user.name
            flash(message=message,category='success')
            return redirect(url_for('index_bp.profile'))
        else:
            flash('The confirmation link is invalid or has expired.','error')
            return redirect(url_for('index_bp.unconfirmed'))

class UnConfirmed(Resource):
    @login_required
    def get(self):
        if current_user.confirmed:
            return jsonify({"message":"user has confirm his/her email address"})
        flash('Please confirm your account!', 'warning')
        html = render_template('user/unconfirmed.html',username=current_user.name)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)


class resend_confirmation(Resource):
    @login_required
    def get(self):
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('index_bp.userconfirmemailroute', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_mail(current_user.email, subject, html)
        resendhtml = render_template('user/resend.html', username=current_user.name, email=current_user.email)
        headers = {'Content-Type': 'text/html'}
        return make_response(resendhtml, 200, headers)

class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        flash('You were logged out.', 'success')
        return redirect(url_for('index_bp.userloginroute'))

class Forgetpassword(Resource):
    def get(self):
        form = ForgotForm()
        html =  render_template('user/forget.html', form=form)
        headers = {'Content-Type': 'text/html'}
        return make_response(html,200,headers)
    def post(self):
        form = ForgotForm(request.form)
        user = UserModel.find_by_username(username=form.username.data)
        token = generate_confirmation_token(user.email)
        user.password_reset_token = token
        user.save_to_db()
        reset_url = url_for('index_bp.resetpassword', token=token, _external=True)
        html = render_template('user/emailreset.html',
                               username=user.email,
                               reset_url=reset_url)
        subject = "Reset your password"
        send_mail(user.email, subject, html)
        flash('A password reset email has been sent via email.', 'success')
        return redirect(url_for("index_bp.indexroute"))

class ResetPassword(Resource):
    def get(self, token):
        form = ChangePasswordForm()
        email = confirm_token(token)
        user = UserModel.query.filter_by(email=email).first_or_404()
        if user.password_reset_token is not None and email == user.email:
            html = render_template("user/reset.html", form=form)
            headers = {'Content-Type': 'text/html'}
            return make_response(html, 200, headers)
        else:
            flash("password cannot be reset try again", "error")
            return redirect("index_bp.forgetpassword")
    def post(self,token):
        form = ChangePasswordForm(request.form)
        email = confirm_token(token)
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(form.password.data)
                user.password_reset_token = None
                user.save_to_db()

                login_user(user)

                flash('Password successfully changed.', 'success')
                return redirect(url_for('index_bp.profile'))
            else:
                flash('Password change was unsuccessful.', 'errors')
                return redirect(url_for('index_bp.forgetpassword'))

        html = render_template('user/reset.html', form=form)
        headers = {'Content-Type': 'text/html'}
        return make_response(html, 200, headers)


