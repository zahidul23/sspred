from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, BooleanField, IntegerField, validators, ValidationError
from wtforms.widgets import TextArea
from wtforms_components import ColorField, Email

import re
	
class SubmissionForm(FlaskForm):
	
	#maybe include seqtext length
	seqtext = TextAreaField('Sequence', [
		validators.Required("Sequence required."), 
		validators.Length(min=30,max=4000, message="Sequence must be between 40 and 4000 characters"),
		validators.Regexp(regex='^[A,R,N,D,C,E,Q,G,H,I,L,K,M,F,P,S,T,W,Y,V]*$', flags = re.IGNORECASE, message="Invalid Characters")  	
		], 
		widget=TextArea(), default= "")
	email = StringField('Email (Optional):', [Email(), validators.Optional()])
	
	JPred = BooleanField('JPred', [validators.Optional()],default="checked")
	PSI = BooleanField('PSIPred', [validators.Optional()], default="checked")
	PSS = BooleanField('PSSPred', [validators.Optional()], default="checked")
	RaptorX = BooleanField('RaptorX', [validators.Optional()], default="checked")
	Sable = BooleanField('SABLE', [validators.Optional()], default="checked")
	Yaspin = BooleanField('YASPIN', [validators.Optional()], default="checked")
	SSPro = BooleanField('SSPRO', [validators.Optional()], default="checked")
	
	rowlength = IntegerField("Amino Acids Per Row: ", [validators.NumberRange(min=60, message="The minimum length of amino acids per row is 60.")],default=60)
	
	helixcolor = ColorField(default="#0000FF")
	coilcolor = ColorField(default="#FF0000")
	betacolor = ColorField(default="#008000")
	
	submitbtn = SubmitField('Submit')

