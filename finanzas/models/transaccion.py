# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv


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
    state = fields.Selection([
            ('borrador', 'Borrador'),
            ('hecho', 'Hecho'),
        ], default="borrador", string="Estado")
    cuenta_emisor = fields.Many2one("if.cuenta", compute="get_cuenta_emisor")
    cuenta_recetor = fields.Many2one("if.cuenta", compute="get_cuenta_recetor")

    @api.depends('user_emisor_id')
    def get_cuenta_emisor(self):
        try:
            # raise osv.UserError(self.user_emisor_id.cuenta_ids[0])
            self.cuenta_emisor = self.user_emisor_id.cuenta_ids[0]
        except:
            pass

    @api.depends('user_receptor_id')
    def get_cuenta_recetor(self):
        try:
            self.cuenta_recetor = self.user_receptor_id.cuenta_ids[0]
        except:
            pass

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

    @api.multi
    def continuar(self):
        # Movimiento de entrada
        if self.state == "borrador":
            self.movimientos_line |= self.env['if.movimiento'].create(
                                    {
                                        'cuenta_id': self.cuenta_recetor.id,
                                        'entra': self.valor,
                                        'sale': 0,
                                        'transaccion_id': self.id,
                                    })
            self.movimientos_line |= self.env['if.movimiento'].create(
                                    {
                                        'cuenta_id': self.cuenta_emisor.id,
                                        'entra': 0,
                                        'sale': self.valor,
                                        'transaccion_id': self.id,
                                    })
            self.state = "hecho"

    # @api.multi
    # def validar(self):
