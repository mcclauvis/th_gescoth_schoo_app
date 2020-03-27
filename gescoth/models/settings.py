# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval

class GescothSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	annee_scolaire_id = fields.Many2one(
	    'gescoth.anneescolaire',
	    string='Année scolaire',
	)
	my_name = fields.Char(
	    string='My_name',
	)
	eleve_ids = fields.Many2many(
	    'gescoth.eleve',
	    string='Elève',
	)


	@api.model
	def set_values(self):
		res = super(GescothSettings, self).set_values()
		self.env['ir.config_parameter'].set_param('gescoth.annee_scolaire_id', self.annee_scolaire_id)
		self.env['ir.config_parameter'].set_param('gescoth.my_name', self.my_name)
		self.env['ir.config_parameter'].set_param('gescoth.eleve_ids', self.eleve_ids)		
		return res

	@api.model
	def get_values(self):
		res = super(GescothSettings, self).get_values()
		ICPSudo = self.env['ir.config_parameter'].sudo()
		anneescolaires = ICPSudo.get_param('gescoth.annee_scolaire_id.id')
		myname = ICPSudo.get_param('gescoth.my_name')
		eleve_ids = ICPSudo.get_param('gescoth.eleve_ids')
		res.update(
			annee_scolaire_id = anneescolaires,
			my_name =myname,
			eleve_ids = [6, 0, literal_eval(eleve_ids)],
		)
		return res