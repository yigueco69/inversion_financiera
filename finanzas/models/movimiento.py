# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv

class movimiento(models.Model):
	_name = 'if.movimiento'
	_description = "Movimiento"

	cuenta_id  = fields.Many2one('if.cuenta', "Cuenta")
	entra = fields.Float("Entrada")
	sale = fields.Float("Salida")
	transaccion_id = fields.Many2one("if.transaccion", "transaccion")
	@api.model
	def create(self, values):
		print values
		record = super(res_partner, self).create(values)
		return record


class res_users(models.Model):
	_inherit = "res.users"
	cuenta_id = fields.One2many(comodel_name="if.cuenta",inverse_name="user_id", string="Cuenta")
	recomendador_id = fields.Many2one("res.users", string = "Recomendador")
	recomendado_ids = fields.One2many(comodel_name="res.users",inverse_name="recomendador_id", string="Recomendados")

class cuenta(models.Model):
	_name = "if.cuenta"
	_description = "Cuenta"
	_rec_name = 'numero_cuenta'

	@api.model
	def get_numero_cuenta(self):
		# seq = self.env["ir.sequence"].get("numero_tarea")
		return self.env["ir.sequence"].get("seq_numero_cuenta")


	numero_cuenta = fields.Char(string='Numero de cuenta',default=get_numero_cuenta)
	user_id = fields.Many2one("res.users", "Titular")
