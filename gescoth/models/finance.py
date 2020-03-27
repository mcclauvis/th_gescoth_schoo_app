# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import *
import datetime

class GescothPayementEleve(models.Model):
    _name = 'gescoth.paiement.eleve'
    _description = 'Gestion des paiement des élèves'
    _rec_name = 'numer_recu'

    numer_recu = fields.Char(
        string="N° de reçu", 
        readonly=True, 
        required=True, 
        copy=False, 
        default='Nouveau',
    )

    eleve_id = fields.Many2one(
    	'gescoth.eleve',
    	string='Elève',
    	required=True,
    )
    date_paiement = fields.Date(
        string='Date de paiement',
        required=True,
        default=datetime.date.today(),
    )

    montant = fields.Float(
        string='Montant du paiement',
        required=True,
    )
    recu_manuel = fields.Char(string="N° du recu manuel")

    @api.model
    def create(self, vals):
        if vals.get('numer_recu', 'Nouveau') == 'Nouveau':
            vals['numer_recu'] = self.env['ir.sequence'].next_by_code(
                'gescoth.paiement.eleve') or 'Nouveau'
        result = super(GescothPayementEleve, self).create(vals)
        return result

    class GescothTranche(models.Model):
        _name = 'gescoth.tranche'
        _description = 'Tranche'
        _rec_name = "eleve_id"
    
        eleve_id = fields.Many2one(
            'gescoth.eleve',
            string='Elève',
        )
        date = fields.Date(
            string='Date',
        )
        montant = fields.Float(
            string='Montant',
        )
        montat_deja_paye = fields.Float(
            string='Montant déjà payé',
        )
        nombre = fields.Integer(
            string='Nombre de payement',
            default=5,
        )
        date_premier_tranche = fields.Date(string="Date de la première tranche",)
        line_ids = fields.One2many('gescoth.tranche.line','tranche_id', string="Linge de tranche")

        def calculer_tranche(self):
            reste_a_payer = self.montant - self.montat_deja_paye
            my_date = self.date
            for n in range(0, self.nombre):
                vals ={
                    'date_echeanche': my_date,
                    'montant': (reste_a_payer / self.nombre),
                    'paye': False,
                    'tranche_id': self.id,
                }
                my_date = my_date + timedelta(days=30)
                self.env['gescoth.tranche.line'].create(vals)

    class GescothPaiementLine(models.Model):
        _name = 'gescoth.tranche.line'
        _description = 'Ligne de tranche'

        date_echeanche = fields.Date(string="Date d'échéance",)
        montant = fields.Float(string="Montant",)
        paye = fields.Boolean(string="Payé", default=False,)
        tranche_id = fields.Many2one(
            'gescoth.tranche',
            string='Tranche',
        )