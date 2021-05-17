from flask import Blueprint, render_template, redirect, url_for, request
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index(cat=None):
    return render_template('index.html',  title='Home')

@main.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html', title='About')

@main.route('/services', methods=['GET', 'POST'])
def services():
	return render_template('services.html', title='Our Services')

@main.route('/contactus', methods=['GET', 'POST'])
def contactUs():
	return render_template('contact.html', title='Contact Us')