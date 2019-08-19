# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class modelo(models.Model):
    _name='optica_sv.modelo'
    name=fields.Char("Name")
    code=fields.Char("Code")