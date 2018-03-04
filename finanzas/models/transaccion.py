# -*- coding: utf-8 -*-
from openerp import models, fields, api
# from openerp.osv import osv
from openerp.tools.translate import _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class transaccion(models.Model):
    _name = 'if.transaccion'
    _description = "Transaccion"
    name = fields.Char(string='Numero de transaccion', readonly=True)
    fecha = fields.Datetime("Fecha")
    movimientos_line = fields.One2many(comodel_name='if.movimiento', inverse_name="transaccion_id", string="Movimientos")
    user_emisor_id = fields.Many2one("res.users", "Usuario Emisor")
    user_emisor_name = fields.Char(related="user_emisor_id.name", string="Nombre del usuario", readonly=True)
    user_emisor_email = fields.Char(related="user_emisor_id.email", string="Email", readonly=True)
    user_emisor_phone = fields.Char(related="user_emisor_id.phone", string="Telefono", readonly=True)

    login_user_char = fields.Char("Escriba el username al cual transferir")
    user_receptor_id = fields.Many2one("res.users", "Usuario Receptor", required=True)
    user_receptor_name = fields.Char(related="user_receptor_id.name", string="Nombre del usuario", readonly=True)
    user_receptor_email = fields.Char(related="user_receptor_id.email", string="Email", readonly=True)
    user_receptor_phone = fields.Char(related="user_receptor_id.phone", string="Telefono", readonly=True)

    valor = fields.Float("Valor")

    tipo_transaccion = fields.Selection([
            ('compra', 'Compra'),
            ('retiro', 'Retiro'),
            ('transferencia', 'transferencia'),
        ], string="Tipo de transaccion")
    state = fields.Selection([
            ('borrador', 'Borrador'),
            ('hecho', 'Hecho'),
        ], default="borrador", string="Estado")

    cuenta_emisor_id = fields.Many2one("if.cuenta", compute="get_cuenta_emisor_id")
    saldo_disponible_emisor = fields.Float(related="cuenta_emisor_id.saldo", string="Saldo disponible")

    cuenta_receptor_id = fields.Many2one("if.cuenta", compute="get_cuenta_receptor_id")
    saldo_disponible_receptor = fields.Float(related="cuenta_receptor_id.saldo", string="Saldo disponible Receptor")

    modo_pago = fields.Selection([
            ('coinpayment', 'Coin Payment'),
            ('saldo', 'Saldo'),
        ], default="coinpayment", string="Modo de pago")
    valor_inversion = fields.Float("Valor de la inversion", readonly=True, store=True, compute="get_valor_inversion")
    cantidad_acciones = fields.Integer("Cantidad de Acciones a comprar", default=1)
    precio_accion = fields.Float("Precio de la accion", compute="get_valor_inversion", store=True)

    @api.depends("modo_pago", "cantidad_acciones")
    def get_valor_inversion(self):
        precio_accion = float(self.env["ir.config_parameter"].get_param("precio_accion", default=None))
        self.precio_accion = precio_accion
        self.valor_inversion = self.cantidad_acciones * precio_accion

    @api.onchange('tipo_transaccion')
    def get_user_emisor_id(self):
        if self.tipo_transaccion == "compra":
            self.user_emisor_id = self._uid
            self.user_receptor_id = int(self.env["ir.config_parameter"].get_param("user_compra_retiro_id", default=None))

        if self.tipo_transaccion == "retiro":
            self.user_emisor_id = self._uid
            self.user_receptor_id = int(self.env["ir.config_parameter"].get_param("user_compra_retiro_id", default=None))

        if self.tipo_transaccion == "transferencia":
            self.user_emisor_id = self._uid

    @api.depends('user_emisor_id')
    def get_cuenta_emisor_id(self):
        try:
            # raise osv.UserError(self.user_emisor_id.cuenta_ids[0])
            self.cuenta_emisor_id = self.user_emisor_id.cuenta_ids[0]
        except:
            pass

    @api.depends('user_receptor_id')
    def get_cuenta_receptor_id(self):
        try:
            self.cuenta_receptor_id = self.user_receptor_id.cuenta_ids[0]
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
        if self.tipo_transaccion == "transferencia":
            if self.saldo_disponible_emisor < self.valor:
                raise UserError(_('Usted no tiene saldo disponible para realizar esta transferencia'))
            if self.state == "borrador":
                self.movimientos_line |= self.env['if.movimiento'].create(
                                        {
                                            'cuenta_id': self.cuenta_receptor_id.id,
                                            'entra': self.valor,
                                            'sale': 0,
                                            'transaccion_id': self.id,
                                        })
                self.movimientos_line |= self.env['if.movimiento'].create(
                                        {
                                            'cuenta_id': self.cuenta_emisor_id.id,
                                            'entra': 0,
                                            'sale': self.valor,
                                            'transaccion_id': self.id,
                                        })
                self.fecha = datetime.now()
                self.state = "hecho"
        if self.tipo_transaccion == "compra":
            if self.state == "borrador":
                if self.modo_pago == "coinpayment":
                    pass  # <---------------  codigo para coinpayment
                if self.modo_pago == "saldo":
                    if self.saldo_disponible_receptor < self.valor_inversion:
                        raise UserError(_('Usted no tiene saldo disponible para realizar esta transferencia'))

                    self.movimientos_line |= self.env['if.movimiento'].create(
                                            {
                                                'cuenta_id': self.cuenta_emisor_id.id,
                                                'entra': 0,
                                                'sale': self.valor_inversion,
                                                'transaccion_id': self.id,
                                            })
                    self.movimientos_line |= self.env['if.movimiento'].create(
                                            {
                                                'cuenta_id': self.cuenta_receptor_id.id,
                                                'entra': self.valor_inversion,
                                                'sale': 0,
                                                'transaccion_id': self.id,
                                            })
                    self.env["if.inversion"].create({
                            "compra_id": self.id,
                            "user_id": self.user_emisor_id.id,
                            "precio_accion": self.precio_accion,
                            "cantidad_acciones": self.cantidad_acciones,
                            "valor_total": self.valor_inversion,
                        })
                    self.fecha = datetime.now()
                    self.state = "hecho"

    # @api.multi
    # def validar(self):
