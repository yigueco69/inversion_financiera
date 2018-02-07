# -*- coding: utf-8 -*-
from openerp import models, fields, api
# from openerp.osv import osv


class movimiento(models.Model):
    _name = 'if.movimiento'
    _description = "Movimiento"

    cuenta_id = fields.Many2one('if.cuenta', "Cuenta", required=True)
    entra = fields.Float("Entrada")
    sale = fields.Float("Salida")
    transaccion_id = fields.Many2one("if.transaccion", "transaccion", required=True)

    # @api.model
    # def create(self, values):
    #     print values
    #     record = super(movimiento, self).create(values)
    #     return record
