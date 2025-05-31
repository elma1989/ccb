from flask import Blueprint, request, render_template
from database import RecepeBook, Country

recepe_bp = Blueprint('recepe',__name__)

@recepe_bp.route('/')
def index(): return render_template('index.html')

@recepe_bp.route('/countries')
def countries():
    book = RecepeBook()
    countries = book.countries()

    return [country.to_dict() for country in countries]

@recepe_bp.route('/recepies')
def recepies():
    book = RecepeBook()
    country = request.args.get('country')

    if not country: return {'message': 'Country unknown'}, 400

    recepies = book.recepies(Country(country))

    if not recepies: return {'message':'Country not found'}, 404

    return [recepe.to_dict() for recepe in recepies]