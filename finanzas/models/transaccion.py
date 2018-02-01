# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv

class transaccion(models.Model):
	_name = 'if.transaccion'
	_description = "Transaccion"
	name = fields.Char(string='Numero de transaccion')

	movimientos_line  = fields.One2many(comodel_name='if.movimiento', inverse_name="transaccion_id", string="Movimientos")

	user_id = fields.Many2one("res.users", "Usuario", readonly = True)
	email_user_char = fields.Char("Email")
	@api.onchange('email_user_char')
	def onchange_email_user_char(self):
		# prin
		result = self.env["res.users"].search([("login","=",self.email_user_char)])
		if result:
			self.user_id = result


	tipo_transaccion = fields.Selection([
        ('compra','Compra'),
        ('retiro','Retiro'),
        ('transferencia','transferencia'),
        ], string="Tipo de transaccion")


	@api.model
	def get_numero_transaccion(self):
		# seq = self.env["ir.sequence"].get("numero_tarea")
		return self.env["ir.sequence"].get("seq_numero_transaccion")


	
	@api.model
	def create(self, values):
		print values
		values["name"] = self.get_numero_transaccion()
		record = super(transaccion, self).create(values)
		return record

