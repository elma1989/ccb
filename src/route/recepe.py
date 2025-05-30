from flask import Blueprint, request, render_template

recepe_bp = Blueprint('recepe',__name__)

@recepe_bp.route('/')
def index(): return render_template('index.html')