# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

# classe pour gérer les matières
class GescothMatiere(models.Model):
	_name = 'gescoth.matiere'
	_description = 'Gestion des matière'
	_sql_constraints = [
	    ('name_uniq', 'unique (name)', _('Cette matière existe déjà !')),
	]

	name = fields.Char(string="Nom de la matière", required=True)
	nom_abrege = fields.Char(string="Nom abrégé")
	user_abrege = fields.Boolean(string="Utiliser le nom abrégé")


#classe pour ger les professeur
class GescothProfesseur(models.Model):
	_name = 'gescoth.professeur'
	_inherit = ['mail.thread','mail.activity.mixin']
	_description = 'Gestion des professeurs'

	name = fields.Char(string="Nom et prénoms", required=True, track_visibility='onchange')
	photo = fields.Binary(string="Photo de l'élève")
	date_naissance = fields.Date(string="Date de naissance",track_visibility='onchange')
	lieu_naissance = fields.Char(string="Lieu de naissance", track_visibility='onchange')
	sexe = fields.Selection([('masculin','Masculin'),('feminin','Féminin')], string="Sexe")
	nationalite = fields.Many2one('res.country', string="Nationalité")
	telephone = fields.Char(string="Téléphone", track_visibility='onchange')
	email =  fields.Char(string="E-mail")
	adresse= fields.Text(string="Adresse complète")
	date_service = fields.Date(
	    string='Date de prise de service'
	)
	statut = fields.Selection([('volontaire','Volontaire'),('permanent','Permanent'),('partiel','Partiel')], string='Statut')
	matieres = fields.Many2many('gescoth.matiere', string="Matière enseignées")


#classe pour gerer les classes
class GescothClasse(models.Model):
	_name = 'gescoth.classe'
	_description = 'Gestion des classes'
	_sql_constraints = [
	    ('name_uniq', 'unique (name)', _('Cette classe existe déjà !')),
	]

	name = fields.Char(string="Nom de la classe", required=True, index=True)
	description = fields.Char(string='Description')
	filiere = fields.Many2one('gescoth.filiere')
	professeur = fields.Many2one('gescoth.professeur', string="Professeur titulaire")
	coeficient_ids = fields.One2many('gescoth.coeficient', 'name', string="Coeficient de matières")
	eleve_ids =  fields.One2many('gescoth.eleve', 'classe', string="Liste des élèves")


#classe pour gerer les filières(series)
class GescothFiliere(models.Model):
	_name = 'gescoth.filiere'
	_description = 'Gestion des filiere'
	_sql_constraints = [
	    ('name_uniq', 'unique (name)', _('Cette filiere existe déjà !')),
	]

	name = fields.Char(string="Nom de filiere", required=True)
	specialite = fields.Char(string="Spécialité")
	classe_ids = fields.One2many('gescoth.classe', 'filiere', string="Liste des classe")


class GescothAnneeScolaire(models.Model):
    _name = 'gescoth.anneescolaire'
    _description = 'Gestion des années scolaire'
    _sql_constraints = [
        ('name_uniq', 'unique (name)', _('Cette années scolaire existe déjà !')),
    ]

    name = fields.Char(string="Année scolaire", required=True)
    date_rentree = fields.Date(string="Date de la rentrée", required=True)
    date_vacance = fields.Date(string="Date des vacance")
    note = fields.Text(
        string='Notes',
    )