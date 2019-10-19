from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, BooleanField, validators, ValidationError
from wtforms.widgets import TextArea

class SubmissionForm(FlaskForm):
	defaultseq = "MSAEREIPAEDSIKVVCRFRPLNDSEEKAGSKFVVKFPNNVEENCISIAGKVYLFDKVFKPNASQEKVYNMSAEREIPAEDSIKVVCRFRPLNDSEEKAGSKFVVKFPNNVEENCISIAGKVYLFDKVFKPNASQEKVYN"
	#maybe include seqtext length
	seqtext = TextAreaField('Sequence', [validators.Required("Sequence required.")], widget=TextArea(), default= defaultseq)
	email = StringField('Email (Optional)', [validators.Email("Invalid email address.")])
	
	# ----------add constraint that at least one is selected-------------
	JPred = BooleanField('JPred', default="checked")
	PSI = BooleanField('PSIPred', default="checked")
	PSS = BooleanField('PSSPred', default="checked")
	RaptorX = BooleanField('RaptorX', default="checked")
	Sable = BooleanField('SABLE', default="checked")
	Yaspin = BooleanField('YASPIN', default="checked")
	SSPro = BooleanField('SSPRO', default="checked")
	
	submitbtn = SubmitField('Submit')
