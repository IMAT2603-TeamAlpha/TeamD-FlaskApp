from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Questions
from app.faqs.forms import SubmitQueryForm
from app import db
from sqlalchemy.sql import func, or_

faqs = Blueprint('faqs', __name__)

@faqs.route('/questions/new', methods=['GET', 'POST'])
def addQuestion():
	form = SubmitQueryForm()
	if form.validate_on_submit():
		questionForm = Questions(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, telephone=form.telephone.data, store=form.store.data, question=form.question.data)
		db.session.add(questionForm)
		db.session.flush()
		new_id = questionForm.id
		db.session.commit()
		flash("Thanks for asking. We will endeavour to respond to your question(s) within 1-2 business days.", 'success')
	return render_template('faqs/addQuestion.html', title='Submit Question', form=form)

@faqs.route('/questions/inbox', methods=['GET'])
@login_required
def displayQuestions():
	if current_user.admin:
		questions = Questions.query.filter(Questions.question.contains('')).all()
		return render_template('faqs/questionsInbox.html', title='Questions Inbox', questions=questions)
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))

@faqs.route('/questions/inbox/<id>', methods=['GET'])
@login_required
def displayQuestion(id):
	if current_user.admin:
		questions = Questions.query.get(id)
		return render_template('faqs/questionsInboxMessage.html', title='Questions Inbox', questions=questions)
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))

@faqs.route('/questions/delete/<id>', methods=['GET'])
@login_required
def deleteQuestion(id):
	if current_user.admin:
		if Questions.query.filter_by(id=id).delete():
			db.session.commit()
			db.session.commit()
			flash('Question has been deleted.', 'success')
			return redirect(url_for('faqs.displayQuestions'))
		return redirect(url_for('faqs.displayQuestions'))
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))