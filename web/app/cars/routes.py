from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.cars.forms import AddNewCarForm, EditCarForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Cars
from app.funcs import save_picture, numberFormat
from app import db
from sqlalchemy.sql import func, or_


cars = Blueprint('cars', __name__)

@cars.route('/all_cars')
def allCars():
	return 'All Cars'

@cars.route('/cars/new', methods=['GET', 'POST'])
@login_required
def addNewCar():

	if current_user.admin:
		form = AddNewCarForm()
		if form.validate_on_submit():
			photo_file = 'default.png'
			if form.photo.data:
				photo_file = save_picture(form.photo.data)

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
				photo=photo_file,
				price=form.price.data
			)
			db.session.add(car)
			db.session.flush()
			new_id = car.id
			db.session.commit()
			flash("Car '%r' Added" % car.model, 'success')
		return render_template('cars/addNewCar.html', title='Add New Car', form=form)
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))

@cars.route('/cars/listing/<id>', methods=['GET'])
def displayCar(id):
	car = Cars.query.get(id)
	return render_template('cars/carListing.html', title='Used {} {} {}'.format(int(car.year), car.manufacturer, car.model), car=car, carMileageFormatted=numberFormat(int(car.mileage)), carPriceFormatted=numberFormat(int(car.price)))

@cars.route('/cars/search', methods=['GET', 'POST'])
def searchCars():
	car = None
	target_string = request.form['search']

	car = Cars.query.filter(Cars.manufacturer.contains(target_string)).all()

	if target_string == '':
		search_msg = 'No cars(s) found matching search criteria - displaying all records'
		color = 'warning'
	else:
		search_msg = f'{len(car)} number of car(s) found matching search criteria'
		color = 'success'
	return render_template('cars/search.html', title='Search Models', cars=car, search_msg=search_msg, color=color)

@cars.route('/cars/edit/<id>', methods=['GET', 'POST'])
@login_required
def editCar(id):
	if current_user.admin:
		car = Cars.query.get(id)
		form = EditCarForm(obj=car)
		if request.method == 'GET':
			form.populate_obj(car)
		elif request.method == 'POST':
			if form.update.data and form.validate_on_submit():
				car.manufacturer = form.manufacturer.data
				car.model = form.model.data
				car.summary = form.summary.data
				car.description = form.description.data
				car.year = form.year.data
				car.mileage = form.mileage.data
				car.transmission = form.transmission.data
				car.fuel = form.fuel.data
				car.engine_size = form.engine_size.data
				car.seats = form.seats.data
				car.doors = form.doors.data
				car.colour = form.colour.data
				car.mot = form.mot.data
				car.last_mot = form.last_mot.data
				car.has_warranty = form.has_warranty.data

				if form.photo.data:
					car.photo = save_picture(car.photo.data)

				car.price = form.price.data
				db.session.commit()
				flash("Car %r Updated" % car.model, 'success')
				return redirect(url_for('cars.displayCar', id=id))
			if form.cancel.data:
				return redirect(url_for('cars.displayCar', id=id))
		return render_template('cars/editCar.html', title='Edit Car', form=form)
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))

@cars.route('/cars/delete/<id>', methods=['GET', 'POST'])
@login_required
def deleteCar(id):
	if current_user.admin:
		if Cars.query.filter_by(id=id).delete():
			db.session.commit()
			flash('Car has been deleted', 'success')
			return redirect(url_for('main.index'))
		return redirect(url_for('cars.displayCar', id=id))
	else:
		flash('This page is for site administrators only - please login with an admin account.', 'danger')
		return redirect(url_for('main.index'))

@cars.route('/cars/all', methods=['GET', 'POST'])
def displayAllCars():
	car = Cars.query.all()
	return render_template('cars/allcars.html', cars=car)