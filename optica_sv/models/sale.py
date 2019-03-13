# -*- coding: utf-8 -*-
##############################################################################


from odoo import api, models, fields, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID


class UserOptica(models.Model):
    _inherit = 'res.users'    
    sucursal=fields.Many2one(comodel_name='stock.warehouse', string='Sucrusal de venta')
    tarifas=fields.Many2many(comodel_name='product.pricelist', string='Tarifas permitidas')

class SaleOrderOptica(models.Model):
    _inherit = 'sale.order'
    oi_esfera = fields.Float("OI. Esfera", required=True)
    oi_cilindro = fields.Float("OI. Cilindro", required=True)
    oi_eje = fields.Float("OI. Eje", required=True)
    oi_adicion = fields.Float("OI. Adicion", required=True)
    oi_prisma = fields.Float("OI. Prisma", required=True)
    oi_oblea = fields.Float("OI. Altura Oblea", required=True)
    oi_pupilar = fields.Float("OI. Altura Pupilar", required=True)
    oi_nasopupilar_cerca = fields.Float("OI. Distancia Nasopupilar Cerca", required=True)
    oi_nasopupilar_lejos = fields.Float("OI. Distancia Nasopupilar Lejos", required=True)
    oi_nasopupilar = fields.Float('OI. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar', required=True)
    
    od_esfera = fields.Float("OD. Esfera", required=True)
    od_cilindro = fields.Float("OD. Cilindro", required=True)
    od_eje = fields.Float("OD. Eje", required=True)
    od_adicion = fields.Float("OD. Adicion", required=True)
    od_prisma = fields.Float("OD. Prisma", required=True)
    od_oblea = fields.Float("OD. Altura Oblea", required=True)
    od_pupilar = fields.Float("OD. Altura Pupilar", required=True)
    od_nasopupilar_cerca = fields.Float("OD. Distancia Nasopupilar Cerca", required=True)
    od_nasopupilar_lejos = fields.Float("OD. Distancia Nasopupilar Lejos", required=True)
    od_nasopupilar = fields.Float('OD. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar')
    od_nasopupilar = fields.Float('OD. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar')
    es_lente = fields.Boolean("Es Lente")
    base = fields.Float("Base", required=False)
    medida_a = fields.Float("A", required=True)
    medida_b = fields.Float("B", required=True)
    medida_c = fields.Float("C", required=True)
    medida_d = fields.Float("D", required=True)
    
    
    @api.one
    @api.depends('oi_nasopupilar_cerca', 'oi_nasopupilar_cerca')
    def _compute_nasopupilar(self):
        self.oi_nasopupilar=self.oi_nasopupilar_cerca+self.oi_nasopupilar_lejos
        self.od_nasopupilar=self.od_nasopupilar_cerca+self.od_nasopupilar_lejos
    
    antireflejo=fields.Boolean("Antireflejo", required=True)
    material=fields.Selection(selection=[('Policarbonato', 'Policarbonato'),('CR-39', 'CR-39'),('Vidrio', 'Vidrio'),('ThinLite', 'Thin&Lite'),('Otro', 'Otro')], string='Material')
    tipo_lente=fields.Selection(selection=[('Sencilla', 'Vision Sencilla'),('Multifocal', 'Multifocal'),('Bifocal', 'Bifocal')], string='Tipo de lente')
    tipo_lente_sencilla=fields.Selection(selection=[('VSterminado', 'VS terminado'),('VSsemiterminado', 'VS SemiTerminado'),('Advance360', 'Advance 360'),('VSExcellens', 'VS Excellens'),('CryzalFogID', 'Cryzal Fog ID'),('CryzalBlueCapture', 'Cryzal Blue Capture')], string='Tipo de Lente Vision Sencilla')
    tipo_lente_bifocal=fields.Selection(selection=[('ftop', 'ftop'),('ftopinvisible', 'Ftop Invisible'),('kriptop', 'kriptop')], string='Tipo de lente bifocal')
    tipo_lente_multifocal=fields.Selection(selection=[('Progresivo natural', 'Progresivo Natura')
                                                        ,('Ovation', 'Ovation')
                                                        ,('Progresivo Novel', 'Progresivo Novel')
                                                        ,('Progresivo Marca Propia', 'Progresivo Marca Propia')
                                                        ,('Varilux Confort', 'Varilux Confort')
                                                        ,('Varilux Confort 3.0', 'Varilux Confort 3.0')
                                                        ,('Varilux Confor Short', 'Varilux Confor Short')
                                                        ,('Varilux Confort 3.0 Short', 'Varilux Confort 3.0 Short')
                                                        ,('Varilux Physio', 'Varilux Physio')
                                                        ,('Varilux Physio 3.0', 'Varilux Physio 3.0')
                                                        ,('Varilux Physio Short', 'Varilux Physio Short')
                                                        ,('Varilux Physio 3.0 Short', 'Varilux Physio 3.0 Short')
                                                        ,('Otro', 'Otro')]
                                                        , string='Tipo de lente multifocal')
    color=fields.Selection(selection=[('Blanco', 'Blanco')
                                        ,('Polarizado Gris', 'Polarizado Gris')
                                        ,('Polarizado Cafe', 'Polarizado Cafe')
                                        ,('Transition Gris', 'Transition Gris')
                                        ,('Transition Cafe', 'Transition Cafe')
                                        ,('Transition Safiro', 'Transition Safiro')
                                        ,('Transition Amatista', 'Ovation')
                                        ,('Entintado', 'Ovation')]
                                        , string='Color')
    tipo_aro=fields.Selection(selection=[('Cerrado', 'Cerrado')
                                        ,('Ranurado', 'Ranurado')
                                        ,('Al Aire', 'Al Aire')]
                                        , string='Tipo de Aro')
                                        

    
