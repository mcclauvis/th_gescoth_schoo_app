# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# classe élève pour inscrire les élèves de l'établissement
class GescothEleve(models.Model):
	_name = 'gescoth.eleve'
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = 'Inscription des élèves'
	_rec_name = 'nom_eleve'

	name = fields.Char(string="N° Matricule", readonly=True, required=True, copy=False, default='Nouveau')
	nom_eleve = fields.Char(string="Nom et prénom(s)", required=True,)
	photo = fields.Binary(string="Photo de l'élève")
	date_naissance = fields.Date(string="Date de naissance",track_visibility='always', default='')
	lieu_naissance = fields.Char(string="Lieu de naissance", default='')
	sexe = fields.Selection([('masculin','Masculin'),('feminin','Féminin')], string="Sexe", default='')
	nationalite = fields.Many2one('res.country', string="Nationalité", default='')
	telephone = fields.Char(string="Téléphone", track_visibility='onchange', default='')
	email =  fields.Char(string="E-mail", track_visibility='always')
	adresse= fields.Text(string="Adresse complète", default='')
	classe = fields.Many2one('gescoth.classe', string="Classe", default='')
	statut = fields.Selection([('N','Nouveau'),('D','Doublant'),('T','Triplant'),('Q','Quatriplant')], string='Statut', default='N')
	Apt_sport = fields.Boolean(string="Apte pour le sport", default=True)
	absence_ids =fields.Many2many('gescoth.absence', string='Absence')
	active = fields.Boolean(string="Active", default=True)



	@api.model
	def create(self, vals):
		if vals.get('name', 'Nouveau') == 'Nouveau':
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'gescoth.eleve') or 'Nouveau'
		result = super(GescothEleve, self).create(vals)
		return result