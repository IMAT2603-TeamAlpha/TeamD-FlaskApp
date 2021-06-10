from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.cars.forms import AddNewCarForm, EditCarForm, searchCarsForm
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

@cars.route('/cars/enhancedsearch', methods=['GET', 'POST'])
def enhancedSearch():
	form = searchCarsForm()
	if form.validate_on_submit():
		print('Data Received: type={}, term={}'.format(form.searchFiltersList.data, form.searchTerms.data))
		return redirect(url_for('cars.filteredCarSearch', type=form.searchFiltersList.data, term=form.searchTerms.data))
	return render_template('cars/enhancedSearch.html', title='Search Cars', form=form)

#v2 search
@cars.route('/cars/search/<term>/<type>', methods=['GET'])
def filteredCarSearch(type, term):
	if type == 'manufacturer':
		car = Cars.query.filter(Cars.manufacturer.contains(term)).all()
		return render_template('cars/filteredSearch.html', title='Filtered Search', cars=car, searchFilter=type, search_msg='{} car(s) found'.format(len(car)), color='success')
	elif type == 'model':
		car = Cars.query.filter(Cars.model.contains(term)).all()
		return render_template('cars/filteredSearch.html', title='Filtered Search', cars=car, searchFilter='Car {}'.format(type), search_msg='{} car(s) found'.format(len(car)), color='success')
	elif type == 'year':
		car = Cars.query.filter(Cars.year.contains(term)).all()
		return render_template('cars/filteredSearch.html', title='Filtered Search', cars=car, searchFilter=type, search_msg='{} car(s) found'.format(len(car)), color='success')
	elif type == 'miles':
		car = Cars.query.filter(Cars.mileage <= term).all() #filter by mileage (less than or equal to mileage)
		return render_template('cars/filteredSearch.html', title='Filtered Search', cars=car, searchFilter=type, search_msg='{} car(s) found'.format(len(car)), color='success')
	elif type == 'price':
		car = Cars.query.filter(Cars.price <= term).all()
		return render_template('cars/filteredSearch.html', title='Filtered Search', cars=car, searchFilter=type, search_msg='{} car(s) found'.format(len(car)), color='success')
	else:
		flash("'%r' is not a valid search filter." % type, 'warning')
		return redirect(url_for('main.index'))

@cars.route('/cars/allCars', methods=['GET'])
def displayAllCars():
	car = Cars.query.filter(Cars.manufacturer.contains('')).all()
	return render_template('cars/search.html', title='Search Models', cars=car, search_msg='{} car(s) found'.format(len(car)), color='success')


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