# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Gescoth(http.controller):

	@http.route('/gescoth/eleve/', website=True, auth='public')
	def gescoth_eleve(self, **kw):
		return 'Bonjour tout le mode'