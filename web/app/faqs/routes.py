from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Questions
from app.faqs.forms import SubmitQueryForm
from app import db
from sqlalchemy.sql import func, or_

faqs = Blueprint('faqs', __name__)

@faqs.route('/questions/new', methods=['GET', 'POST'])
def addQuestion():
	form = SubmitQueryForm()
	if form.validate_on_submit():
		queryForm = Questions(first_name=form.first_name.data, last_name=form.last_name.data, store=form.store.data, query=form.query.data)
		db.session.add(queryForm)
		db.session.flush()
		new_id = queryForm.id
		db.session.commit()
		flash("Thanks for asking. We will endeavour to respond to your question(s) within 2 business days.", 'success')
	return render_template('faqs/addQuestion.html', title='Submit Question', form=form)

@faqs.route('/questions/inbox', methods=['GET'])
def displayQuestions():
	#questions = Questions.query.filter(Questions.query.contains('')).all()
	return render_template('faqs/questionsInbox.html', title='Questions Inbox', questions=questions)