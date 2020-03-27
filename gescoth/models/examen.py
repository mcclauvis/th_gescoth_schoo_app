# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .. functions.myFunctions import *

# classe pour gérer les les coeficients
class GescothCoeficient(models.Model):
	_name = 'gescoth.coeficient'
	_description = 'Gestion des coeficient'
	_rec_name = 'matiere'

	name = fields.Many2one('gescoth.classe', string="Classe")
	matiere = fields.Many2one('gescoth.matiere', string="Matière", required=True)
	est_facultative = fields.Boolean(string="La matière est facultative")
	coef = fields.Float(string="Coeficient", default=1)
	professeur_id = fields.Many2one('gescoth.professeur','Professeur')


class GesocthNote(models.Model):
	_name = 'gescoth.note'
	_description = 'Gestion des notes'
	_rec_name = 'eleve_id'
	_sql_constraints = [
		('saison_unique_note', 'UNIQUE (eleve_id, classe_id, matiere_id, saison)', 'Cette note existe déjà !')
	]

	eleve_id = fields.Many2one('gescoth.eleve', string="Elève", required=True)
	classe_id = fields.Many2one('gescoth.classe', string="Classe", required=True)
	coeficient_id = fields.Many2one('gescoth.coeficient', string="Matière", required=True)
	saison = fields.Selection([('s1','Semestre 1'),('s2','Semestre 2'),('s3','Semestre 3')], required=True)
	note_compo = fields.Float(string="Note de composition",)
	moy_classe = fields.Float(string="Moyenne de classe",)
	moyenne = fields.Float(string="Moyenne", default=0, )
	rang = fields.Char(string="Rang",compute="CalculerRang")
	annee_scolaire = fields.Many2one('gescoth.anneescolaire', required=True, string="Année scolaire",)
	bulletin_id = fields.Many2one('gescoth.bulletin', string="Bulletin", ondelete="cascade")
	professeur_id = fields.Many2one('gescoth.professeur', "Professeur")
	appreciation = fields.Char(string='Appréciation', compute='Appreciation')

	@api.one
	# @api.onchange('note_compo','moy_classe')
	def CalculerRang(self):
		data = list()
		notes = self.env['gescoth.note'].search([
			('classe_id','=', self.classe_id.id),
			('saison','=', self.saison),
			('coeficient_id','=', self.coeficient_id.id),
		])
		for note in notes:
			data.append(note.moyenne)
		for rec in self:
			rec.rang = Rang(rec.moyenne, self.eleve_id.sexe, data)

	    

	@api.onchange('moy_classe','note_compo')	    
	def Appreciation(self):
		appr = self.env['gescoth.appreciation'].search([])
		for rec in self:
			for ap in appr:
				if rec.moyenne >= ap.inf and rec.moyenne < ap.sup:
					rec.appreciation = ap.name
				if rec.moyenne >= 20:
					rec.appreciation = 'Excellent'

	@api.constrains('moy_classe','note_compo')
	def check_notes(self):
		for rec in self:
			if rec.moy_classe < 0 or rec.moy_classe > 20:
				raise ValidationError(_('La moyenne de classe doit être entre 0 et 20. Vous avez taper : ' + str(rec.moy_classe)))
			if rec.note_compo < 0 or rec.note_compo> 20:
				raise ValidationError(_('La moyenne de classe doit être entre 0 et 20. Vous avez taper : ' + str(rec.note_compo)))

	@api.onchange('note_compo','moy_classe')
	def _onchange_note_compo(self):
		for rec in self:
			rec.moyenne = (rec.note_compo + rec.moy_classe)/2



class GescothAppreciation(models.Model):
	_name = 'gescoth.appreciation'
	_description = 'Gestion des appications'

	name= fields.Char(string="Appréciation")
	type_appreciation = fields.Selection([('general','Générale'),('note','Note')], string="Type d'appications")
	inf = fields.Float(string='Inférieur')
	sup = fields.Float(string='Supérieur')


class GescothBulletin(models.Model):
	_name = 'gescoth.bulletin'
	_description = 'Impression des bulletins'
	_rec_name= "eleve_id"

	eleve_id = fields.Many2one(
	    'gescoth.eleve',
	    string='Elève',
	    required=True,
	)
	saison = fields.Selection(
		[('s1','Semestre 1'),('s2','Semestre 2'),('s3','Semestre 3')], 
		required=True,
		string="Saison",
	)

	annee_scolaire = fields.Many2one('gescoth.anneescolaire', string="Année scolaire", required=True,)

	note_ids = fields.One2many(
		'gescoth.note',
		'bulletin_id',
		string='Liste des notes',
	)

	lot_id = fields.Many2one(
		'gescoth.lot.bulletin',
		string='Lot de bulletin',
		ondelete='cascade',
	)

	def calcule_de_note(self):
		for el in self.eleve_id.classe.coeficient_ids:
			vals = {
				'eleve_id' : self.eleve_id.id,
				'annee_scolaire': self.annee_scolaire.id,
				'classe_id': self.eleve_id.classe.id,
				'coeficient_id': el.id,
				'saison' : self.saison,
				'bulletin_id' : self.id,
			}
			self.env['gescoth.note'].create(vals)

class GescothLotBulletin(models.Model):
    _name = 'gescoth.lot.bulletin'
    _description = 'Générer le bulletins par lot pour facilité le traitement'
    _rec_name= 'classe_id'

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
        required=True,
    )
    name = fields.Char(string="Nom du bulletin", compute="nom_bulletin")
    saison = fields.Selection([('s1','Semestre 1'),('s2','Semestre 2'),('s3','Semestre 3')], required=True, string="Saison")
    annee_scolaire_id = fields.Many2one(
        'gescoth.anneescolaire',
        string='Année scolaire',
    )
    bulletin_ids = fields.One2many(
        'gescoth.bulletin',
        'lot_id',
        string='Liste des bulletin',
    )

    def calcule_de_note(self):
    	for el in self.bulletin_ids:
    		el.calcule_de_note()

    def nom_bulletin(self):
    	for rec in self:
    		rec.name = rec.classe_id.name + ' ' + str(rec.saison) + ' ' + rec.annee_scolaire_id.name

    def generer_bulletin(self):
    	for el in self.classe_id.eleve_ids:
    		vals = {
    		'eleve_id' : el.id,
    		'annee_scolaire': self.annee_scolaire_id.id,
    		'saison' : self.saison,
    		'lot_id': self.id
    		}
    		self.env['gescoth.bulletin'].create(vals)



class GescothSaisieNote(models.Model):
    _name = 'gescoth.saisie.note'
    _description = 'Saisir les notes par classe et par matiere'

    classe_id = fields.Many2one(
        'gescoth.classe',
        string='Classe',
    )
    matiere_id = fields.Many2one(
        'gescoth.matiere',
        string='Matiere',
    )
    saison = fields.Selection(
    	[('s1','Semestre 1'),
    	('s2','Semestre 2'),
    	('s3','Semestre 3')], 
    	required=True,
    	string='Saision',
    )
    annee_scolaire = fields.Many2one(
    	'gescoth.anneescolaire', 
    	required=True, 
    	string="Année scolaire",
    )

    note_ids = fields.Many2many(
    	'gescoth.note',
    	string="liste de notes",
    )
