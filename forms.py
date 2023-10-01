from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, BooleanField, validators, ValidationError
from wtforms.widgets import TextArea

import re

class SubmissionForm(FlaskForm):
	
	seqtext = TextAreaField('Sequence', [
		validators.Required("Sequence required."), 
		validators.Length(min=30,max=4000, message="Sequence must be between 30 and 4000 characters"),
		validators.Regexp(regex='^[ARNDCEQGHILKMFPSTWYV\s]*$', flags = re.IGNORECASE, message="Invalid Characters")], 
		widget=TextArea(), default= "")
	email = StringField('Email (Optional):', [validators.Email(), validators.Optional()])
	
	JPred = BooleanField('JPred', [validators.Optional()],default="checked")
	PSI = BooleanField('PSIPred', [validators.Optional()], default="checked")
	PSS = BooleanField('PSSPred', [validators.Optional()], default="checked")
	RaptorX = BooleanField('RaptorX', [validators.Optional()], default="checked")
	Sable = BooleanField('SABLE', [validators.Optional()], default="checked")
	Yaspin = BooleanField('YASPIN', [validators.Optional()], default="checked")
	SSPro = BooleanField('SSPRO', [validators.Optional()], default="checked")
	
	structureId = StringField('Structure Id:',[ 
		validators.Optional(),
		validators.Length(min=4,max=4, message="StructureID must be 4 characters"),
		validators.Regexp(regex='^[A-Z0-9]*$', flags = re.IGNORECASE, message="Invalid Characters")],
		render_kw={'style':'width:80px'})
	chainId = StringField('Chain Id:',[ 
		validators.Optional(),
		validators.Length(min=1,max=1, message="Chain ID must be single letter"),
		validators.Regexp(regex='^[A-Z]*$', flags = re.IGNORECASE, message="Invalid Characters")],
		 render_kw={'style':'width:50px'})
	
	submitbtn = SubmitField('Submit')
	
	#Override default validate
	def validate(self):
		if not FlaskForm.validate(self):
			return False
		
		validated = True
		
		#Check if at least one site selected
		if not self.JPred.data and not self.PSI.data and not self.PSS.data and not self.RaptorX.data and not self.Sable.data and not self.Yaspin.data and not self.SSPro.data:
			self.JPred.errors.append('At least one site must be selected.')
			validated = False
		
		#If at least one field is filled, the other must be filled as well
		if (self.structureId.data and not self.chainId.data) or (self.chainId.data and not self.structureId.data):
			self.structureId.errors.append('A chain id must be provided with a structure id.')
			validated = False
		
		return validated