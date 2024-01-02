from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import NumberRange, URL, Optional

class AddPetForm(FlaskForm):
    # pet_name = StringField("Pet name", validators=[Optional(), Email()])
    pet_name = StringField("Pet name")
    species = StringField("Species")
    photo_url = StringField("Photo", validators=[URL(require_tld=False), Optional()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30, message='Must be between 0 and 30')])
    notes = StringField("Notes")