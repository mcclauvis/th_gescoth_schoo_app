# -*- coding: utf-8 -*-
{
    'name' : 'GescoTh',
    'version' : '12.1.0',
    'summary' : """
        Module de gestion complète de école secondaire
    """,
    'category' : 'Gestion des écoles',
    'author' : 'Thomas ATCHA',
    'maintainer' : 'Thomas ATCHA',
    'company': 'Thomas ATCHA',
    'website' : 'https://gescoth.edu',
    'depends' : ['base','mail','report_xlsx'],
    'data' : [

        'security/ir.model.access.csv',
        'wizards/absence.xml',
        'views/eleve_view.xml',
        'wizards/liste_eleve_view.xml',
        'views/cours_view.xml',
        'views/ecole_view.xml',
        'views/examen_view.xml',
        'views/finance_view.xml',
        'views/settings.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'reports/bulletin_view.xml',
        'reports/eleve_report_view.xml',
        'reports/paiement_recu.xml',
    ],

    'images' : [],
    'licence' : 'AGPL-3',
    'installable' : True,
    'application' : True,
    'auto_install' : False,
}