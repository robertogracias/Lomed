# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class casa(models.Model):
    _name='optica_sv.casa'
    name=fields.Char("Name")
    code=fields.Char("Code")