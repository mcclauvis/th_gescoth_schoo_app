# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import *

class GescothAbsence(models.TransientModel):
	_name = 'gescoth.absence'
	_description = 'Gestion des absence'

	eleve_id = fields.Many2one('gescoth.eleve', string='Elève', required=True,)
	date_absence = fields.Date(string="Date d'absence", default=fields.Date.today,)
	nbr_heure = fields.Float(string="Nombre d'heure",)


	def ajouter_absence_eleve(self):
		vals={
		'eleve_id':self.eleve_id.id,
		'date_absence':self.date_absence,
		'nbr_heure':self.nbr_heure,
		}
		self.env['gescoth.absence'].create(vals)