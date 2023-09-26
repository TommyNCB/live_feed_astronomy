from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.widgets import TextArea

class CreatePostForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired()])
    summary = StringField("Descripción", widget=TextArea())
    attachment = FileField('Upload File', validators=[
        FileRequired(message='File is required!'),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], message='Only image files are allowed!')
    ])
    submit = SubmitField("Crear Publicación")
