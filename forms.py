from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, BooleanField, validators, ValidationError
from wtforms.widgets import TextArea
		
class SubmissionForm(FlaskForm):
	defaultseq = "MSAEREIPAEDSIKVVCRFRPLNDSEEKAGSKFVVKFPNNVEENCISIAGKVYLFDKVFKPNASQEKVYNMSAEREIPAEDSIKVVCRFRPLNDSEEKAGSKFVVKFPNNVEENCISIAGKVYLFDKVFKPNASQEKVYN"
	#maybe include seqtext length
	seqtext = TextAreaField('Sequence', [validators.Required("Sequence required.")], widget=TextArea(), default= defaultseq)
	email = StringField('Email (Optional):', [validators.Email("Invalid email address."), validators.Optional()])
	
	JPred = BooleanField('JPred', [validators.Optional()],default="checked")
	PSI = BooleanField('PSIPred', [validators.Optional()], default="checked")
	PSS = BooleanField('PSSPred', [validators.Optional()], default="checked")
	RaptorX = BooleanField('RaptorX', [validators.Optional()], default="checked")
	Sable = BooleanField('SABLE', [validators.Optional()], default="checked")
	Yaspin = BooleanField('YASPIN', [validators.Optional()], default="checked")
	SSPro = BooleanField('SSPRO', [validators.Optional()], default="checked")
	
	submitbtn = SubmitField('Submit')