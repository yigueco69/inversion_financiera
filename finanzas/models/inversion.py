# -*- coding: utf-8 -*-
from openerp import models, fields, api
# from openerp.osv import osv
# from openerp.tools.translate import _
# from odoo.exceptions import UserError
# import time

import datetime
import dateutil.parser


class inversion(models.Model):
    _name = 'if.inversion'
    _description = "Transaccion"
    name = fields.Char(string='Numero de inversion', readonly=True)
    fecha = fields.Datetime(String="Fecha de la inversion", required=True)
    compra_id = fields.Many2one("if.transaccion", "Origen", required=True)
    movimientos_line = fields.One2many(comodel_name='if.movimiento', inverse_name="transaccion_id", string="Movimientos")
    user_id = fields.Many2one("res.users", "Usuario Emisor", readonly=True, required=True)
    precio_accion = fields.Float("Precio de la accion", required=True)
    cantidad_acciones = fields.Float("cantidad de acciones", required=True)

    valor_total = fields.Float("Valor total", required=True)
    porcentaje_ejecucion = fields.Integer("Porcentaje de ejecucion", compute="get_datos")
    dias_restantes = fields.Integer("Dias restantes", compute="get_datos")
    dias_transcurridos = fields.Integer("Dias transcurridos", compute="get_datos")
    state = fields.Selection([
            ('enejecucion', 'En ejecucion'),
            ('hecho', 'Hecho'),
        ], default="enejecucion", string="Estado", required=True)

    @api.multi
    @api.depends('fecha')
    def get_datos(self):
        # return 5
        for line in self:
            hoy = datetime.datetime.now()
            resta = hoy - dateutil.parser.parse(line.fecha)
            line.porcentaje_ejecucion = (resta.days/90.00)*100
            line.dias_restantes = 90-resta.days
            line.dias_transcurridos = resta.days

    @api.model
    def get_numero_inversion(self):
        # seq = self.env["ir.sequence"].get("numero_tarea")
        return self.env["ir.sequence"].get("seq_numero_inversion")

    @api.model
    def create(self, values):
        print values
        values["name"] = self.get_numero_inversion()
        record = super(inversion, self).create(values)
        return record
