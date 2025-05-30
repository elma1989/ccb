from flask import Blueprint, request, render_template
from database import RecepeBook

recepe_bp = Blueprint('recepe',__name__)

@recepe_bp.route('/')
def index(): return render_template('index.html')

@recepe_bp.route('/countries')
def countries():
    book = RecepeBook()
    countries = book.countries()

    return [country.to_dict() for country in countries]