# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv

class transaccion(models.Model):
	_name = 'if.transaccion'
	_description = "Transaccion"
	_rec_name = "numero_transaccion"
	movimientos_line  = fields.Many2many('if.movimiento', "Movimientos")
	users_id = fields.Many2one("res.users", "Usuario")


	@api.model
	def get_numero_transaccion(self):
		# seq = self.env["ir.sequence"].get("numero_tarea")
		return self.env["ir.sequence"].get("seq_numero_transaccion")


	numero_transaccion = fields.Char(string='Numero de transaccion',default=get_numero_transaccion)
	@api.model
	def create(self, values):
		print values
		record = super(res_partner, self).create(values)
		return record

