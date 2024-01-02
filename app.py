from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm
from flask_migrate import Migrate

app = Flask(__name__)

app.app_context().push()
migrate = Migrate(app, db)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_available_pets():
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)



@app.route('/add_pet')
def go_to_add_pet_form():
    form = AddPetForm()
    return render_template('addPetForm.html', form=form)


@app.route('/submit_pet_form', methods=['POST'])
def add_pet_form_submission():
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("addPetForm.html", form=form)


@app.route('/pet/<int:id>')
def go_to_individual_pet_page(id):
    pet = Pet.query.get(id)
    return render_template('individualPet.html', pet=pet)


@app.route('/edit_pet/<int:id>')
def go_to_edit_pet_form(id):
    """go to the form for editing a pet; get pet object instance using pet.id"""
    pet = Pet.query.get(id)
    form = AddPetForm(obj=pet)
    return render_template('edit_pet.html', pet=pet, form=form)


@app.route('/submit_form_for_edit/<int:id>', methods=['POST'])
def change_pet_info(id):
    """take edits to pet info and change attributes for pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        pet = Pet.query.get(id)
        pet.name=name 
        pet.species=species
        pet.photo_url=photo_url 
        pet.age=age
        pet.notes=notes
        db.session.commit()
    return redirect('/')
