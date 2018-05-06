# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, fields, widgets

# Import Form validators
from wtforms.validators import Email, DataRequired, Length


# Define the create group form (WTForms)
class MultiCheckboxField(fields.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
class CreateGroupForm(FlaskForm):
    name    = TextField('Nombre', [DataRequired(message='Forgot your group name?')])
    members = MultiCheckboxField('Members', coerce=int)
    
    # def __init__(self, **kwargs):
    #   print('inicializando')
    #   super(CreateGroupForm, self).__init__(**kwargs)

    def set_members(self, friends):
      self.members.choices = [(f.id, str(f.name)) for f in friends]