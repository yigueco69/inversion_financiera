# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Inversion Financiera",
    "version": "1",
    "category": "Website",
    # "website": "https://laslabs.com/",
    "author": "RBS",
    "license": "LGPL-3",
    "depends": [
        "base",
        'web',
    ],
    "data": [
            # 'static/src/xml/buttton_post_view.xml',
            'vistas/inversion_view.xml',
            'vistas/movimiento_view.xml',
            'vistas/cuenta_view.xml',
            'vistas/retiro_view.xml',
            'vistas/compra_view.xml',
            'vistas/transferencia_view.xml',
            'vistas/res_users_view.xml',
            'sequence.xml',
            "models/config.xml",
            "ir_parameter.xml",
    ],

    # 'qweb': [
    #   'static/src/xml/widget.xml'
    # ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
