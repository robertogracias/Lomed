# -*- coding: utf-8 -*-

from odoo import models, fields , api 

class productotemplate(models.Model):
    _inherit='product.template'
    clase=fields.Char("clase")
    casa_id=fields.Many2one(comodel_name='optica_sv.casa', string='Casa')
    color_id=fields.Many2one(comodel_name='optica_sv.color', string='Color')
    marca_id=fields.Many2one(comodel_name='optica_sv.marca', string='Marca')
    material_id=fields.Many2one(comodel_name='optica_sv.material', string='Material')
    medida_id=fields.Many2one(comodel_name='optica_sv.medida', string='Medida')
    modelo_id=fields.Many2one(comodel_name='optica_sv.modelo', string='Modelo')
    tipo_id=fields.Many2one(comodel_name='optica_sv.tipo', string='Tipo')
    
class productocategory(models.Model):
    _inherit='product.category'
    excluir_cierre=fields.Boolean("Excluir del cierre")