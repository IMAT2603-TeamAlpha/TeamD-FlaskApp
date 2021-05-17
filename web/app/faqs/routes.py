from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.faqs.forms import AddFAQForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, FAQ
from app.funcs import save_picture, numberFormat
from app import db
from sqlalchemy.sql import func, or_


faqs = Blueprint('faqs', __name__)

@faqs.route('/faqs', methods=['GET', 'POST'])
def displayFAQS():
	faq = FAQ.query.get(id)
	return render_template('faqs/faq.html', title='About Us and Frequently Asked Questions', faq=faq)

@faqs.route('/faqs/new', methods=['GET', 'POST'])
def addNewFAQ():
	form = AddFAQForm()
	if form.validate_on_submit():

		faqs = FAQ(
			question = form.question.data,
			answer = form.answer.data
		)
		db.session.add(faqs)
		db.session.flush()
		new_id = faqs.id
		db.session.commit()
		flash("FAQ '%r' Added" % faqs.question, 'success')
	return render_template('faqs/addNewFAQ.html', title='Add New FAQ', form=form)