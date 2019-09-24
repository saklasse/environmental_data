from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_babel import lazy_gettext
from environmental_data.main.database.database import country, drinking_water_sample, ms_rate_sample, ms_rate_drinking_water_sample, site_type, site
import flask_babel

main = Blueprint('main', __name__, template_folder='templates')

db = SQLAlchemy()


@main.route('/')
def index():
    return render_template("home.html")


@main.route('/country', methods=['GET'])
def list_countries():
    return render_template('country/show.html', countries=country.query.all())


@main.route('/newCountry', methods=['GET', 'POST'])
def newCountry():
    if request.method == 'POST':
        newCountry = country(name=request.form['name'])
        db.session.add(newCountry)
        db.session.commit()
        return redirect(url_for('list_countries'))
    else:
        return render_template('country/new.html')

        
@main.route('/<int:country_id>/editCountry', methods=['GET', 'POST'])
def editCountry(country_id):
    editedCountry = db.session.query(country).filter_by(country_id=country_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCountry.name = request.form['name']
            db.session.add(editedCountry)
            db.session.commit()
            return redirect(url_for('list_countries'))
    else:
        return render_template('country/edit.html', country=editedCountry)

        
@main.route('/<int:country_id>/deleteCountry', methods=['GET', 'POST'])
def deleteCountry(country_id):
    countryToDelete = db.session.query(country).filter_by(country_id=country_id).one()
    if request.method == 'POST':
        db.session.delete(countryToDelete)
        db.session.commit()
        return redirect(url_for('list_countries'))
    else:
        return render_template('country/delete.html', country=countryToDelete)
    

@main.route('/site', methods=['GET'])
def list_sites():
   return render_template('site/show.html', sites=site.query.all())


@main.route('/newSite', methods=['GET', 'POST'])
def newSite():
    if request.method == 'POST':
        newSite = site(country_id=request.form.get('country_id'),
                       site_type_id=request.form.get('site_type_id'),
                       name=request.form['name'],
                       latitude=request.form['latitude'],
                       longitude=request.form['longitude'])
        db.session.add(newSite)
        db.session.commit()
        return redirect(url_for('list_sites'))
    else:
        return render_template('site/new.html', country=country.query.all(), site_type=site_type.query.all())


@main.route('/<int:site_id>/editSite', methods=['GET', 'POST'])
def editSite(site_id):
    editedSite = db.session.query(site).filter_by(site_id=site_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedSite.country_id = request.form.get('country_id')
            editedSite.site_type_id = request.form.get('site_type_id')
            editedSite.name = request.form['name']
            editedSite.latitude = request.form['latitude']
            editedSite.longitude = request.form['longitude']

            db.session.add(editedSite)
            db.session.commit()
            return redirect(url_for('list_sites'))
    else:
        return render_template('site/edit.html', site=editedSite, country=country.query.all(), site_type=site_type.query.all())

        
@main.route('/<int:site_id>/deleteSite', methods=['GET', 'POST'])
def deleteSite(site_id):
    siteToDelete = db.session.query(site).filter_by(site_id=site_id).one()
    if request.method == 'POST':
        db.session.delete(siteToDelete)
        db.session.commit()
        return redirect(url_for('list_sites'))
    else:
        return render_template('site/delete.html', site=siteToDelete)


@main.route('/site_type', methods=['GET'])
def list_sites_types():
   return render_template('site_type/show.html', site_types=site_type.query.all())


@main.route('/ms_sample_rate', methods=['GET'])
def list_ms_rate_samples():
   return render_template('ms_rate_sample/show.html', ms_rate_samples=ms_rate_sample.query.all())


@main.route('/newMsRateSample', methods=['GET', 'POST'])
def newMsRateSample():
    if request.method == 'POST':
        newMsRateSample = ms_rate_sample(site_id=request.form.get('site_id'), date=request.form['date'], rate=request.form['rate'])
        db.session.add(newMsRateSample)
        db.session.commit()
        return redirect(url_for('list_ms_rate_samples'))
    else:
        return render_template('ms_rate_sample/new.html', site=site.query.all())


@main.route('/newSiteType', methods=['GET', 'POST'])
def newSiteType():
    if request.method == 'POST':
        newSiteType = site_type(name=request.form['name'])
        db.session.add(newSiteType)
        db.session.commit()
        return redirect(url_for('list_sites_types'))
    else:
        return render_template('site_type/new.html')


@main.route('/<int:site_type_id>/editSiteType', methods=['GET', 'POST'])
def editSiteType(site_type_id):
    editedSite = db.session.query(site_type).filter_by(site_type_id=site_type_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedSite.name = request.form['name']
            db.session.add(editedSite)
            db.session.commit()
            return redirect(url_for('list_sites_types'))
    else:
        return render_template('site_type/edit.html', site_type=editedSite)

        
@main.route('/<int:site_type_id>/deleteSiteType', methods=['GET', 'POST'])
def deleteSiteType(site_type_id):
    siteTypeToDelete = db.session.query(site_type).filter_by(site_type_id=site_type_id).one()
    if request.method == 'POST':
        db.session.delete(siteTypeToDelete)
        db.session.commit()
        return redirect(url_for('list_sites_types'))
    else:
        return render_template('site_type/delete.html', site_type=siteTypeToDelete)


@main.route('/<int:ms_rate_sample_id>/editMsRateSample', methods=['GET', 'POST'])
def editMsRateSample(ms_rate_sample_id):
    editedMsRateSample = db.session.query(ms_rate_sample).filter_by(ms_rate_sample_id=ms_rate_sample_id).one()
    if request.method == 'POST':
        if request.form['site_id']:
            editedMsRateSample.site_id = request.form['site_id']
            editedMsRateSample.date = request.form['date']
            editedMsRateSample.rate = request.form['rate']
            
            db.session.add(editedMsRateSample)
            db.session.commit()
            return redirect(url_for('list_ms_rate_samples'))
    else:
        return render_template('ms_rate_sample/edit.html', editedMsRateSample=editedMsRateSample, site=site.query.all())

        
@main.route('/<int:ms_rate_sample_id>/deleteMsRateSample', methods=['GET', 'POST'])
def deleteMsRateSample(ms_rate_sample_id):
    MsRateSampleToDelete = db.session.query(ms_rate_sample).filter_by(ms_rate_sample_id=ms_rate_sample_id).one()
    if request.method == 'POST':
        db.session.delete(MsRateSampleToDelete)
        db.session.commit()
        return redirect(url_for('list_ms_rate_samples'))
    else:
        return render_template('ms_rate_sample/delete.html', MsRateSampleToDelete=MsRateSampleToDelete)


@main.route('/drinking_water_sample', methods=['GET'])
def list_drinking_water_samples():
   return render_template('drinking_water_sample/show.html', drinking_water_samples=drinking_water_sample.query.all())


@main.route('/newDrinkingWaterSample', methods=['GET', 'POST'])
def newDrinkingWaterSample():
    if request.method == 'POST':
        newDrinkingWaterSample = drinking_water_sample()
        setDrinkingWaterSample(newDrinkingWaterSample, request)
        db.session.add(newDrinkingWaterSample)
        db.session.commit()
        return redirect(url_for('list_drinking_water_samples'))
    else:
        return render_template('drinking_water_sample/new.html', site=site.query.all())


def setDrinkingWaterSample(editedDrinkingWaterSample, request):
    editedDrinkingWaterSample.site_id = request.form['site_id']
    editedDrinkingWaterSample.date = request.form['date']
    editedDrinkingWaterSample.population = request.form['population']
    if request.form['total_coliforms'] != "":
        editedDrinkingWaterSample.total_coliforms = float(request.form['total_coliforms']) * float(request.form['total_coliforms_units'])
    if request.form['e_coli'] != "":
        editedDrinkingWaterSample.e_coli = float(request.form['e_coli']) * float(request.form['e_coli_units'])
    if request.form['heterotrophic_plate_count'] != "":
        editedDrinkingWaterSample.heterotrophic_plate_count = float(request.form['heterotrophic_plate_count']) * float(request.form['heterotrophic_plate_count_units'])
    if request.form['ph'] != "":
        editedDrinkingWaterSample.ph = float(request.form['ph']) * float(request.form['ph_units'])
    if request.form['alkalinity'] != "":
        editedDrinkingWaterSample.alkalinity = float(request.form['alkalinity']) * float(request.form['alkalinity_units'])
    if request.form['bromide'] != "":
        editedDrinkingWaterSample.bromide = float(request.form['bromide']) * float(request.form['bromide_units'])
    if request.form['calcium'] != "":
        editedDrinkingWaterSample.calcium = float(request.form['calcium']) * float(request.form['calcium_units'])
    if request.form['chlorate'] != "":
        editedDrinkingWaterSample.chlorate = float(request.form['chlorate']) * float(request.form['chlorate_units'])
    if request.form['chloride'] != "":
        editedDrinkingWaterSample.chloride = float(request.form['chloride']) * float(request.form['chloride_units'])
    if request.form['chlorine'] != "":
        editedDrinkingWaterSample.chlorine = float(request.form['chlorine']) * float(request.form['chlorine_units'])
    if request.form['fluoride'] != "":
        editedDrinkingWaterSample.fluoride = float(request.form['fluoride']) * float(request.form['fluoride_units'])
    if request.form['magnesium'] != "":
        editedDrinkingWaterSample.magnesium = float(request.form['magnesium']) * float(request.form['magnesium_units'])
    if request.form['potassium'] != "":
        editedDrinkingWaterSample.potassium = float(request.form['potassium']) * float(request.form['potassium_units'])
    if request.form['silicon'] != "":
        editedDrinkingWaterSample.silicon = float(request.form['silicon']) * float(request.form['silicon_units'])
    if request.form['sodium'] != "":
        editedDrinkingWaterSample.sodium = float(request.form['sodium']) * float(request.form['sodium_units'])
    if request.form['sulphate'] != "":
        editedDrinkingWaterSample.sulphate = float(request.form['sulphate']) * float(request.form['sulphate_units'])
    if request.form['calcium_hardness'] != "":
        editedDrinkingWaterSample.calcium_hardness = float(request.form['calcium_hardness']) * float(request.form['calcium_hardness_units'])
    if request.form['nitrate'] != "":
        editedDrinkingWaterSample.nitrate = float(request.form['nitrate']) * float(request.form['nitrate_units'])
    if request.form['nitrite'] != "":
        editedDrinkingWaterSample.nitrite = float(request.form['nitrite']) * float(request.form['nitrite_units'])
    if request.form['aluminum'] != "":
        editedDrinkingWaterSample.aluminum = float(request.form['aluminum']) * float(request.form['aluminum_units'])
    if request.form['barium'] != "":
        editedDrinkingWaterSample.barium = float(request.form['barium']) * float(request.form['barium_units'])
    if request.form['boron'] != "":
        editedDrinkingWaterSample.boron = float(request.form['boron']) * float(request.form['boron_units'])
    if request.form['cadmium'] != "":
        editedDrinkingWaterSample.cadmium = float(request.form['cadmium']) * float(request.form['cadmium_units'])
    if request.form['chromium'] != "":
        editedDrinkingWaterSample.chromium = float(request.form['chromium']) * float(request.form['chromium_units'])
    if request.form['chromium_vi'] != "":
        editedDrinkingWaterSample.chromium_vi = float(request.form['chromium_vi']) * float(request.form['chromium_vi_units'])
    if request.form['copper'] != "":
        editedDrinkingWaterSample.copper = float(request.form['copper']) * float(request.form['copper_units'])
    if request.form['iron'] != "":
        editedDrinkingWaterSample.iron = float(request.form['iron']) * float(request.form['iron_units'])
    if request.form['lead'] != "":
        editedDrinkingWaterSample.lead = float(request.form['lead']) * float(request.form['lead_units'])
    if request.form['manganese'] != "":
        editedDrinkingWaterSample.manganese = float(request.form['manganese']) * float(request.form['manganese_units'])
    if request.form['mercury'] != "":
        editedDrinkingWaterSample.mercury = float(request.form['mercury']) * float(request.form['mercury_units'])
    if request.form['nickel'] != "":
        editedDrinkingWaterSample.nickel = float(request.form['nickel']) * float(request.form['nickel_units'])
    if request.form['selenium'] != "":
        editedDrinkingWaterSample.selenium = float(request.form['selenium']) * float(request.form['selenium_units'])
    if request.form['strontium'] != "":
        editedDrinkingWaterSample.strontium = float(request.form['strontium']) * float(request.form['strontium_units'])
    if request.form['uranium'] != "":
        editedDrinkingWaterSample.uranium = float(request.form['uranium']) * float(request.form['uranium_units'])
    if request.form['vanadium'] != "":
        editedDrinkingWaterSample.vanadium = float(request.form['vanadium']) * float(request.form['vanadium_units'])
    if request.form['zinc'] != "":
        editedDrinkingWaterSample.zinc = float(request.form['zinc']) * float(request.form['zinc_units'])
    if request.form['atrazine_metabolites'] != "":
        editedDrinkingWaterSample.atrazine_metabolites = float(request.form['atrazine_metabolites']) * float(request.form['atrazine_metabolites_units'])
    if request.form['diazinon'] != "":
        editedDrinkingWaterSample.diazinon = float(request.form['diazinon']) * float(request.form['diazinon_units'])
    if request.form['dicamba'] != "":
        editedDrinkingWaterSample.dicamba = float(request.form['dicamba']) * float(request.form['dicamba_units'])
    if request.form['dichloromethane'] != "":
        editedDrinkingWaterSample.dichloromethane = float(request.form['dichloromethane']) * float(request.form['dichloromethane_units'])
    if request.form['diclofop_methyl'] != "":
        editedDrinkingWaterSample.diclofop_methyl = float(request.form['diclofop_methyl']) * float(request.form['diclofop_methyl_units'])
    if request.form['metolachlor'] != "":
        editedDrinkingWaterSample.metolachlor = float(request.form['metolachlor']) * float(request.form['metolachlor_units'])
    if request.form['picloram'] != "":
        editedDrinkingWaterSample.picloram = float(request.form['picloram']) * float(request.form['picloram_units'])
    if request.form['simazine'] != "":
        editedDrinkingWaterSample.simazine = float(request.form['simazine']) * float(request.form['simazine_units'])
    if request.form['chloroform'] != "":
        editedDrinkingWaterSample.chloroform = float(request.form['chloroform']) * float(request.form['chloroform_units'])
    if request.form['bromodichloromethane'] != "":
        editedDrinkingWaterSample.bromodichloromethane = float(request.form['bromodichloromethane']) * float(request.form['bromodichloromethane_units'])
    if request.form['dibromochloromethane'] != "":
        editedDrinkingWaterSample.dibromochloromethane = float(request.form['dibromochloromethane']) * float(request.form['dibromochloromethane_units'])
    if request.form['total_trihalomethanes'] != "":
        editedDrinkingWaterSample.total_trihalomethanes = float(request.form['total_trihalomethanes']) * float(request.form['total_trihalomethanes_units'])
    if request.form['dichloroacetic_acid'] != "":
        editedDrinkingWaterSample.dichloroacetic_acid = float(request.form['dichloroacetic_acid']) * float(request.form['dichloroacetic_acid_units'])
    if request.form['trichloroacetic_acid'] != "":
        editedDrinkingWaterSample.trichloroacetic_acid = float(request.form['trichloroacetic_acid']) * float(request.form['trichloroacetic_acid_units'])
    if request.form['bromochloroacetic_acid'] != "":
        editedDrinkingWaterSample.bromochloroacetic_acid = float(request.form['bromochloroacetic_acid']) * float(request.form['bromochloroacetic_acid_units'])
    if request.form['total_haloacetic_acids_haa5'] != "":
        editedDrinkingWaterSample.total_haloacetic_acids_haa5 = float(request.form['total_haloacetic_acids_haa5']) * float(request.form['total_haloacetic_acids_haa5_units'])
    if request.form['caffeine'] != "":
        editedDrinkingWaterSample.caffeine = float(request.form['caffeine']) * float(request.form['caffeine_units'])
    if request.form['metformin'] != "":
        editedDrinkingWaterSample.metformin = float(request.form['metformin']) * float(request.form['metformin_units'])
    if request.form['total_organic_carbon'] != "":
        editedDrinkingWaterSample.total_organic_carbon = float(request.form['total_organic_carbon']) * float(request.form['total_organic_carbon_units'])
    if request.form['grossalpha_radioactivity'] != "":
        editedDrinkingWaterSample.grossalpha_radioactivity = float(request.form['grossalpha_radioactivity']) * float(request.form['grossalpha_radioactivity_units'])
    if request.form['grossbeta_radioactivity'] != "":
        editedDrinkingWaterSample.grossbeta_radioactivity = float(request.form['grossbeta_radioactivity']) * float(request.form['grossbeta_radioactivity_units'])
    if request.form['tritium'] != "":
        editedDrinkingWaterSample.tritium = float(request.form['tritium']) * float(request.form['tritium_units'])
    if request.form['ms_rate_sample'] != "NONE":
        editedDrinkingWaterSample.ms_rate_samples.clear()
        editedDrinkingWaterSample.ms_rate_samples.append(db.session.query(ms_rate_sample).filter_by(site_id=request.form['ms_rate_sample']).first())
    else:
        editedDrinkingWaterSample.ms_rate_samples.clear()


@main.route('/<int:drinking_water_sample_id>/editDrinkingWaterSample', methods=['GET', 'POST'])
def editDrinkingWaterSample(drinking_water_sample_id):
    editedDrinkingWaterSample = db.session.query(drinking_water_sample).filter_by(drinking_water_sample_id=drinking_water_sample_id).one()
    if request.method == 'POST':
        if request.form['site_id']:
            setDrinkingWaterSample(editedDrinkingWaterSample, request)
            
            db.session.add(editedDrinkingWaterSample)
            db.session.commit()
            return redirect(url_for('list_drinking_water_samples'))
    else:
        return render_template('drinking_water_sample/edit.html', editedDrinkingWaterSample=editedDrinkingWaterSample, site=site.query.all())

        
@main.route('/<int:drinking_water_sample_id>/deleteDrinkingWaterSample', methods=['GET', 'POST'])
def deleteDrinkingWaterSample(drinking_water_sample_id):
    drinkingWaterSampleToDelete = db.session.query(drinking_water_sample).filter_by(drinking_water_sample_id=drinking_water_sample_id).one()
    if request.method == 'POST':
        db.session.delete(drinkingWaterSampleToDelete)
        db.session.commit()
        return redirect(url_for('list_drinking_water_samples'))
    else:
        return render_template('drinking_water_sample/delete.html', drinkingWaterSampleToDelete=drinkingWaterSampleToDelete)

