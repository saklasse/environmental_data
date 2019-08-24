from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.DB_CONNECTION_STRING
db = SQLAlchemy(app)

#The country table
class country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

#The site type table
class site_type(db.Model):
    site_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

#The site table
class site(db.Model):
    site_id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
    site_type_id = db.Column(db.Integer, db.ForeignKey('site_type.site_type_id'))
    name = db.Column(db.String(45))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)

    country = db.relationship('country', backref=db.backref('site', lazy=True))    
    site_type = db.relationship('site_type', backref=db.backref('site', lazy=True))

#The ms rate sample table
class ms_rate_sample(db.Model):
    ms_rate_sample_id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.site_id'))
    date = db.Column(db.DATE)
    rate = db.Column(db.Integer)
    
    site = db.relationship('site', backref=db.backref('ms_rate_sample', lazy=True))

#The drinking water sample table
class drinking_water_sample(db.Model):
    drinking_water_sample_id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.site_id'))
    date = db.Column(db.DATE)
    population =db.Column(db.FLOAT)
    total_coliforms =db.Column(db.FLOAT)
    e_coli =db.Column(db.FLOAT)
    heterotrophic_plate_count =db.Column(db.FLOAT)
    ph =db.Column(db.FLOAT)
    alkalinity =db.Column(db.FLOAT)
    bromide =db.Column(db.FLOAT)
    calcium =db.Column(db.FLOAT)
    chlorate =db.Column(db.FLOAT)
    chloride =db.Column(db.FLOAT)
    chlorine =db.Column(db.FLOAT)
    fluoride =db.Column(db.FLOAT)
    magnesium =db.Column(db.FLOAT)
    potassium =db.Column(db.FLOAT)
    silicon =db.Column(db.FLOAT)
    sodium =db.Column(db.FLOAT)
    sulphate =db.Column(db.FLOAT)
    calcium_hardness =db.Column(db.FLOAT)
    nitrate =db.Column(db.FLOAT)
    nitrite =db.Column(db.FLOAT)
    aluminum =db.Column(db.FLOAT)
    barium =db.Column(db.FLOAT)
    boron =db.Column(db.FLOAT)
    cadmium =db.Column(db.FLOAT)
    chromium =db.Column(db.FLOAT)
    chromium_vi =db.Column(db.FLOAT)
    copper =db.Column(db.FLOAT)
    iron =db.Column(db.FLOAT)
    lead =db.Column(db.FLOAT)
    manganese =db.Column(db.FLOAT)
    mercury =db.Column(db.FLOAT)
    nickel =db.Column(db.FLOAT)
    selenium =db.Column(db.FLOAT)
    strontium =db.Column(db.FLOAT)
    uranium =db.Column(db.FLOAT)
    vanadium =db.Column(db.FLOAT)
    zinc =db.Column(db.FLOAT)
    atrazine_metabolites =db.Column(db.FLOAT)
    diazinon =db.Column(db.FLOAT)
    dicamba =db.Column(db.FLOAT)
    dichloromethane =db.Column(db.FLOAT)
    diclofop_methyl =db.Column(db.FLOAT)
    metolachlor =db.Column(db.FLOAT)
    picloram =db.Column(db.FLOAT)
    simazine =db.Column(db.FLOAT)
    chloroform =db.Column(db.FLOAT)
    bromodichloromethane =db.Column(db.FLOAT)
    dibromochloromethane =db.Column(db.FLOAT)
    total_trihalomethanes =db.Column(db.FLOAT)
    dichloroacetic_acid =db.Column(db.FLOAT)
    trichloroacetic_acid =db.Column(db.FLOAT)
    bromochloroacetic_acid =db.Column(db.FLOAT)
    total_haloacetic_acids_haa5 =db.Column(db.FLOAT)
    caffeine =db.Column(db.FLOAT)
    metformin =db.Column(db.FLOAT)
    total_organic_carbon =db.Column(db.FLOAT)
    grossalpha_radioactivity =db.Column(db.FLOAT)
    grossbeta_radioactivity =db.Column(db.FLOAT)
    tritium =db.Column(db.FLOAT)
    
    site = db.relationship('site', backref=db.backref('drinking_water_sample', lazy=True))

def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def home():
    return render_template("home.html" )

@app.route('/country', methods = ['GET'])
def list_countries():
   return render_template('countries.html', countries = country.query.all() )

@app.route('/site', methods = ['GET'])
def list_sites():
   return render_template('sites.html', sites = site.query.all() )
   
@app.route('/newCountry', methods=['GET', 'POST'])
def newCountry():
    if request.method == 'POST':
        newCountry = country(name=request.form['name'])
        db.session.add(newCountry)
        db.session.commit()
        return redirect(url_for('list_countries'))
    else:
        return render_template('newCountry.html')
        
@app.route('/<int:country_id>/editCountry', methods=['GET', 'POST'])
def editCountry(country_id):
    editedCountry = db.session.query(country).filter_by(country_id=country_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCountry.name = request.form['name']
            db.session.add(editedCountry)
            db.session.commit()
            return redirect(url_for('list_countries'))
    else:
        return render_template('editCountry.html', country = editedCountry )
        
@app.route('/<int:country_id>/deleteCountry', methods=['GET', 'POST'])
def deleteCountry(country_id):
    countryToDelete = db.session.query(country).filter_by(country_id=country_id).one()
    if request.method == 'POST':
        db.session.delete(countryToDelete)
        db.session.commit()
        return redirect(url_for('list_countries'))
    else:
        return render_template('deleteCountry.html', country = countryToDelete )

@app.route('/site_type', methods = ['GET'])
def list_sites_types():
   return render_template('site_types.html', site_types = site_type.query.all() )

@app.route('/ms_sample_rate', methods = ['GET'])
def list_ms_rate_samples():
   return render_template('ms_rate_samples.html', ms_rate_samples = ms_rate_sample.query.all() )

@app.route('/drinking_water_sample', methods = ['GET'])
def list_drinking_water_samples():
   return render_template('drinking_water_samples.html', drinking_water_samples = drinking_water_sample.query.all() )

if __name__ == "__main__":
    app.run(debug=True, port=5001,host='0.0.0.0')
