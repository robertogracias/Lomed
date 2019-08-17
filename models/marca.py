# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class marca(models.Model):
    _name='optica_sv.marca' # nombre del modelo
    _inheret='product.template'
    name=fields.Char("Name")
    code=fields.Char("Code")