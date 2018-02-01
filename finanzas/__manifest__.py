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
        'web',
    ],
    "data": [
            'vistas/movimiento_view.xml',
            'vistas/transaccion_view.xml',
            'sequence.xml'
	    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}