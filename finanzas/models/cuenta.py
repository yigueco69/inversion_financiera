# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv


class res_users(models.Model):
    _inherit = "res.users"
    es_virtual = fields.Boolean("Es virtual")
    cuenta_ids = fields.One2many(comodel_name="if.cuenta", inverse_name="user_id", string="Cuenta", readonly=True)
    recomendador_id = fields.Many2one("res.users", string="Recomendador")
    recomendado_ids = fields.One2many(comodel_name="res.users", inverse_name="recomendador_id", string="Recomendados")

    @api.model
    def create(self, values):
        values["cuenta_ids"] = [(4, self.env['if.cuenta'].create({'user_id': self.id}).id)]
        record = super(res_users, self).create(values)
        return record

    # @api.onchange('cuenta_ids')
    # def onchange_cuenta_ids(self):
    #     cuenta_ids
        # hacer que la cuenta sea unica


class cuenta(models.Model):
    _name = "if.cuenta"
    _description = "Cuenta"
    _rec_name = 'numero_cuenta'

    @api.model
    def get_numero_cuenta(self):
        # seq = self.env["ir.sequence"].get("numero_tarea")
        return self.env["ir.sequence"].get("seq_numero_cuenta")

    numero_cuenta = fields.Char(string='Numero de cuenta', default=get_numero_cuenta)
    user_id = fields.Many2one("res.users", "Titular")
    saldo = fields.Float("Saldo", compute="get_saldo")
    movimiento_ids = fields.One2many(comodel_name="if.movimiento", inverse_name="cuenta_id", string="Movimientos")

    @api.one
    def get_saldo(self):
        # self.env['if.movimiento'].sear
        movimiento = self.env['if.movimiento'].search([['cuenta_id', '=', self.id]])

        if len(movimiento) > 0:
            self.saldo = sum(line.entra-line.sale for line in movimiento)
        # print movimiento

    _sql_constraints = [
        ('user_id_uniq', 'unique (user_id)', 'Solo puede haber una cuenta por usuario\n es posible que otro usuario tenga esta cuenta !'),
        ('numero_cuenta_uniq', 'unique (numero_cuenta)', 'El numero de cuenta debe ser unico!'),
    ]
