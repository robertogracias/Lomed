# -*- coding: utf-8 -*-
##############################################################################


from odoo import api, models, fields, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID
from numero_letras import numero_a_letras, numero_a_moneda


class Sucursal(models.Model):
	_inherit = 'stock.location'
	secuencia_factura=fields.Many2many(comodel_name='ir.sequence', string='Secuencia de facturas')
	secuenelds.Many2many(comodel_name='ir.sequence', string='Secuencia de CCF')
	secuencia_recicia_ccf=fibos=fields.Many2many(comodel_name='ir.sequence', string='Secuencia de Recibos')
	cuenta_analitica=fields.Many2many(comodel_name='account.analytic.account', string='Cuenta Analitica')

class UserOptica(models.Model):
    _inherit = 'res.users'    
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta')
    tarifas=fields.Many2many(comodel_name='product.pricelist', string='Tarifas permitidas')

class FacturaSV(models.Model):
    _inherit = 'account.invoice'    
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
    monto_letras=fields.Char('Monto en letras',compute='_fill_invoice',store=true)
    excento=fields.Float('excento',compute='_fill_invoice',store=true)
    gravado=fields.Float('gravado',compute='_fill_invoice',store=true)
    nosujeto=fields.Float('nosujeto',compute='_fill_invoice',store=true)
    retenido=fields.Float('retenido',compute='_fill_invoice',store=true)
    percibido=fields.Float('percibido',compute='_fill_invoice',store=true)
    iva=fields.Float('iva',compute='_fill_invoice',store=true)
    
    @api.one
    @api.depends('amount','invoice_line_ids')
    def _fill_invoice(self):
		total=0;
		excento=0;
		gravado=0;
		nosujeto=0;
		retenido=0;
		percibido=0;
		iva=0;
		for line in self.invoice_line_ids:
			if line.invoice_line_tax_ids:
				gravado=gravado+line.price_subtotal
			else:
				excento=excento+line.price_subtotal
		for tline in self.tax_line_ids:
			if tline.tax_id.tax_group_id.name='retencion':
				retenido=retenido+tline.amount;
			if tline.tax_id.tax_group_id.name='iva':
				iva=iva+tline.amount;
			if tline.tax_id.tax_group_id.name='percepcion':
				percibido=percibido+tline.amount;
		monto_letras=numero_a_letras(self.amount_total)	
    

class SaleOrderOptica(models.Model):
    _inherit = 'sale.order')
    sucursal_id=fields.Many2one(comodel_name='stock.warehouse', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
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
                                        ,('Transition Amatista', 'Transition Amatista')
                                        ,('Entintado', 'Entintado')]
                                        , string='Color')
    tipo_aro=fields.Selection(selection=[('Cerrado', 'Cerrado')
                                        ,('Ranurado', 'Ranurado')
                                        ,('Al Aire', 'Al Aire')]
                                        , string='Tipo de Aro')
                                        

    
