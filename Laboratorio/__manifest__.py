# -*- coding: utf-8 -*-

{
    "name": "lomed_laboratorio",
    "category": '',
    "summary": """
     Mantenimiento lomed .""",
    "description": """
	   form script
    """,
    "sequence": 3,
    "author": "Strategi-k",
    "website": "http://strategi-k.com",
    "version": '12.0.0.4',
    "depends": [ 'sale'
          ],
    
    "data": [
        'security/ir.model.access.csv'
        ,'views/form.xml'
        ,'views/mantenimiento.xml'
        ,'views/sale.xml'
             ],

    'qweb': [
        
        ],
    "installable": True,
    "application": True,
    "auto_install": False,

}