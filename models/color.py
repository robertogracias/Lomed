# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class color(models.Model):
    _name='optica_sv.color'
    name=fields.Char("Name")
    code=fields.Char("Code")