# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class productotemplate(models.Model):
    _inherit='product.template'
    clase=fields.Char("clase")
    
   