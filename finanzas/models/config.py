# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.exceptions import UserError
from openerp import fields, api, models
# from openerp.tools.translate import _


class config_settings(models.Model):
    _name = 'if.settings'
    _inherit = 'res.config.settings'
    _rec_name = 'user_compra_retiro_id'
    user_compra_retiro_id = fields.Many2one("res.users", string='Usuario administrador', help="Usuario virtual para la compra y retiro de inversion")
    precio_accion = fields.Float(string='Precio de Accion')
    # user_admin_
    # ftp_propiedad = fields.Char(string='Direccion del Servidor FTP')

    @api.one
    def set_user_compra_retiro_id(self):
        self.env["ir.config_parameter"].set_param("user_compra_retiro_id", self.user_compra_retiro_id.id or '')

    # @api.one
    def get_default_user_compra_retiro_id(self, context=None):
        user_compra_retiro_id = self.env["ir.config_parameter"].get_param("user_compra_retiro_id", default=None)
        # raise UserError(user_compra_retiro_id is not None)
        if user_compra_retiro_id is not None:
            return {'user_compra_retiro_id': int(user_compra_retiro_id)}
        return {'user_compra_retiro_id': user_compra_retiro_id}

    @api.one
    def set_precio_accion(self):
        self.env["ir.config_parameter"].set_param("precio_accion", self.precio_accion or '')

    # @api.one
    def get_default_precio_accion(self, context=None):
        precio_accion = self.env["ir.config_parameter"].get_param("precio_accion", default=None)

        if precio_accion is not None:
            return {'precio_accion': float(precio_accion)}
        return {'precio_accion': precio_accion}

        # return {'precio_accion': float(precio_accion)}

    # def get_default_user_compra_retiro_id(self, context=None):
    #     # pass
    #     try:
    #         user_compra_retiro_id = self.env["ir.config_parameter"].get_param("user_compra_retiro_id", default=None)
    #         if user_compra_retiro_id is not None:
    #             return {'user_compra_retiro_id': int(user_compra_retiro_id)}
    #     except:
    #         return {'user_compra_retiro_id': 11}
    # @api.one
    # def set_ftp_propiedad(self):
    #     self.env["ir.config_parameter"].set_param("ftp.propiedad", self.ftp_propiedad or '')

    # def get_default_ftp_propiedad(self, context=None):
    #     ftp = self.env["ir.config_parameter"].get_param("ftp.propiedad", default=None)
    #     return {'ftp_propiedad': ftp or False}

    # def _get_alias_domain(self, cr, uid, ids, name, args, context=None):
    #     domain = self.env["ir.config_parameter"].get_param("mail.catchall.domain", context=context)
    #     return dict.fromkeys(ids, domain or "")
