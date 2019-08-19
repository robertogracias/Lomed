# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class medida(models.Model):
    _name='optica_sv.medida'
    name=fields.Char("Name")
    code=fields.Char("Code")