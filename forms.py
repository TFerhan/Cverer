from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, PasswordField, EmailField, SelectField, BooleanField, TimeField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Email, Length, InputRequired, NumberRange, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed

class KeywordField(FlaskForm):
    keyword = StringField('Job Role/Field', validators=[DataRequired()])
    submit = SubmitField('Next')

class UploadPDFForm(FlaskForm):
    file = FileField('PDF file', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    submit = SubmitField('Optimize')


class UploadPDFForm(FlaskForm):
    file = FileField('PDF file', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    submit = SubmitField('Optimize')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Results')

class JobMarketForm(FlaskForm):
    marketKeyword = StringField('Job Role/Field', validators=[DataRequired()])
    submit = SubmitField('Analyze')

class KeywordAndActionForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    action = SelectField('Action', choices=[('choose', 'Choose an action'),('optimize', 'Optimize your resume'), ('analyze', 'Analyze the job market'), ('lettre', 'Optimize your cover letter')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')