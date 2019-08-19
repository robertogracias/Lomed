# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class material(models.Model):
    _name='optica_sv.material'
    name=fields.Char("Name")
    code=fields.Char("Code")