# -*- coding: utf-8 -*-

{
    "name": "Optica SV",
    "category": 'Sales',
    "summary": """
       Localizacion de Opticas .""",
    "description": """
	   Registra la orden de produccion para un laboratorio optico

    """,
    "sequence": 1,
    "author": "Strategi-k",
    "website": "http://strategi-k.com",
    "version": '12.0.0.4',
    "depends": ['sale','stock','sale_stock'],
    "data": [
        'security/ir.model.access.csv'
        ,'views/sale_order.xml',
        'views/marca.xml',
        'views/casa.xml',
        'views/color.xml',
        'views/material.xml',
        'views/medida.xml',
        'views/product.xml',
        'views/modelo.xml',
        'views/tipo.xml',
        'views/anticipo.xml'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,

}
