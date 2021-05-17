from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.cars.forms import AddNewCarForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Cars
from app.funcs import save_picture #causing a problem (flask.cli.NoAppException)
from app import db
from sqlalchemy.sql import func, or_


cars = Blueprint('cars', __name__)

@cars.route('/all_cars')
def allCars():
	return 'Cars page'

@cars.route('/cars/new', methods=['GET', 'POST'])
def addNewCar():
	form = AddNewCarForm()
	if form.validate_on_submit():
		photo_file = 'default.png'
		if form.photo.data:
			photo_file = save_picture(form.photo.data)

		car = Cars(
			manufacturer=form.manufacturer.data, #issue coming from here (according to error output: TypeError: __init__() got an unexpected keyword argument 'manufacturer') -- needs fixing
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
			photo=photo_file,
			price=form.price.data
		)
		db.session.add(car)
		db.session.flush()
		new_id = car.id
		db.session.commit()
		flash('Car Added', 'success')
		#return redirect(url_for('cars.cars'), id=new_id) #cars page needs to be implemented
	return render_template('cars/addNewCar.html', title='Add New Car', form=form)