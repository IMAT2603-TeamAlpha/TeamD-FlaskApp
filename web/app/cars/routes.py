from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.cars.forms import AddNewCarForm, EditCarForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
#from app.funcs import save_picture #causing a problem (flask.cli.NoAppException)
from app import db

cars = Blueprint('cars', __name__)

@cars.route('/all_cars')
def allCars():
	return 'Cars page'

@cars.route('/cars/new', methods=['GET', 'POST'])
@login_required
def addNewCar():
	form = AddNewCarForm()
	if form.validate_on_submit():
		image_file = 'default.png'
		if form.data.photo:
			image_file = save_picture(form.photo.data)

		car = Cars(
			manufacturer=form.manufacturer.data,
			model=form.model.data,
			summary=form.summary.data,
			description=form.description.data,
			year=form.year.data,
			mileage=form.mileage.data,
			transmission=form.transmission.data,
			fuel=form.fuel.data,
			engine_size=form.engine_size.data,
			seats=form.seats.data,
			doors=form.doors.data,
			colour=form.colour.data,
			mot=form.mot.data,
			last_mot=form.last_mot.data,
			has_warranty=form.has_warranty.data,
			photo=image_file,
			price=form.price.data
		)
		db.session.add(car)
		db.session.flush()
		new_id = car.id
		db.session.commit()
		flash('Car Added', 'success')
		return redirect(url_for('cars.cars'), id=new_id)
	return render_template('cars/addNewCar.html', title='Add New Car', form=form)

