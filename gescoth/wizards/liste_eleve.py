# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GescothAbsence(models.TransientModel):
	_name = 'gescoth.liste.eleve'
	_description = "Impression des liste d'élève"

	classe_id = fields.Many2one('gescoth.classe', string='classe', required=True,)

	@api.multi
	def Imprimer(self):
		data = {
			'model':'gescoth.liste.eleve',
			'form':self.read()[0],
		}
		# raise ValidationError(_(data))
		return self.env.ref('gescoth.bulletin_report_view').report_action(self, data=data)
		