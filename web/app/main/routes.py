from flask import Blueprint, render_template, redirect, url_for, request, session
from app.main.forms import MainForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import First_name, Last_name, query
from app.funcs import save_picture
from app import db
from sqlalchemy.sql import func, or_
from flask_login import current_user, login_user, logout_user, login_required


main = Blueprint('main', __name__)

@main.route('/all_faq')
@login_required
def all_faq():
    return 'All faq'

@main.route('/FAQ', methods=['GET', 'POST'])
@login_required
def faq():

if current_user.admin:
	form = AddNewFAQ()
	if form.validate_on_submit():
		photo_file = 'default.png'
		if form.photo.data:
			photo_file = save_picture(form.photo.data)
        
        faq = FAQ (
    first_name=form.first_name.data,
	last_name=form.last_name.data,
	store= form.store.data,
	query= form.query.data,
              
        )
        db.session.add(faq)
        db.session.flush()
        new_id = faq.id
        db.session.commit()
        flash('faq was added successfully', 'success')
        return render_template('faq.html', title='Ass new faq', form=form)
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))
    