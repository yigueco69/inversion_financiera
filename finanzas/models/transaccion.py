# -*- coding: utf-8 -*-
from openerp import models, fields, api
# from openerp.osv import osv


class transaccion(models.Model):
    _name = 'if.transaccion'
    _description = "Transaccion"
    name = fields.Char(string='Numero de transaccion', readonly=True)

    # @api.model
    # def default_user_emisor_id(self):

    #     if self.tipo_transaccion == 'transferencia':
    #         self.user_emisor_id = self._uid

    movimientos_line = fields.One2many(comodel_name='if.movimiento', inverse_name="transaccion_id", string="Movimientos")
    user_emisor_id = fields.Many2one("res.users", "Usuario Emisor", readonly=True, required=True)

    login_user_char = fields.Char("Escriba el username al cual transferir")
    user_receptor_id = fields.Many2one("res.users", "Usuario Receptor", required=True)
    user_receptor_name = fields.Char(related="user_receptor_id.name", string="Nombre del usuario", readonly=True)
    user_receptor_email = fields.Char(related="user_receptor_id.email", string="Email", readonly=True)
    user_receptor_phone = fields.Char(related="user_receptor_id.phone", string="Telefono", readonly=True)

    valor = fields.Float("Valor", required=True)

    tipo_transaccion = fields.Selection([
            ('compra', 'Compra'),
            ('retiro', 'Retiro'),
            ('transferencia', 'transferencia'),
        ], string="Tipo de transaccion")

    @api.onchange('login_user_char')
    def onchange_email_user_char(self):
        # prin
        result = self.env["res.users"].search([("login", "=", self.login_user_char)])
        if result:
            self.user_receptor_id = result

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
