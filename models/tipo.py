# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class tipo(models.Model):
    _name='optica_sv.tipo'
    name=fields.Char("Name")
    code=fields.Char("Code")