# -*- coding: utf-8 -*-
##############################################################################


from odoo import api, models, fields, _
from datetime import datetime, timedelta
from datetime import date
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID


class Sucursal(models.Model):
    _inherit = 'stock.location'
    secuencia_factura=fields.Many2many(comodel_name='ir.sequence', string='Secuencia de facturas')
    secuencia_ccf=fields.Many2many(comodel_name='ir.sequence', string='Secuencia de CCF')
    secuencia_recibos=fields.Many2many(comodel_name='ir.sequence', string='Secuencia de Recibos')
    cuenta_analitica=fields.Many2many(comodel_name='account.analytic.account', string='Cuenta Analitica')

class UserOptica(models.Model):
    _inherit = 'res.users'
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta')
    tarifas=fields.Many2many(comodel_name='product.pricelist', string='Tarifas permitidas')


class PaymentSV(models.Model):
    _inherit = 'account.payment'
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
    cuenta_analitica=fields.Many2many(comodel_name='account.analytic.account', string='Cuenta Analitica',default=lambda self: self.env.user.sucursal_id.cuenta_analitica.id)
    cierre_id=fields.Many2one(comodel_name='optica_sv.cierre', string='Cierre')

class FacturaSV(models.Model):
    _inherit = 'account.invoice'
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
    cuenta_analitica=fields.Many2many(comodel_name='account.analytic.account', string='Cuenta Analitica',default=lambda self: self.env.user.sucursal_id.cuenta_analitica.id)
    monto_letras=fields.Char('Monto en letras',compute='_fill_invoice',store=True)
    excento=fields.Float('excento',compute='_fill_invoice',store=True)
    gravado=fields.Float('gravado',compute='_fill_invoice',store=True)
    nosujeto=fields.Float('nosujeto',compute='_fill_invoice',store=True)
    retenido=fields.Float('retenido',compute='_fill_invoice',store=True)
    percibido=fields.Float('percibido',compute='_fill_invoice',store=True)
    iva=fields.Float('iva',compute='_fill_invoice',store=True)
    cierre_id=fields.Many2one(comodel_name='optica_sv.cierre', string='Cierre')

    @api.one
    @api.depends('amount_total','invoice_line_ids')
    def _fill_invoice(self):
        self.excento=0
        self.gravado=0
        self.nosujeto=0
        self.retenido=0
        self.percibido=0
        self.iva=0

        for line in self.invoice_line_ids:
            line.account_analytic_id=self.cuenta_analitica
            if line.invoice_line_tax_ids:
                self.gravado=self.gravado+line.price_subtotal
            else:
                self.excento=self.excento+line.price_subtotal
        for tline in self.tax_line_ids:
            if tline.tax_id.tax_group_id.name=='retencion':
                self.retenido=self.retenido+tline.amount
            if tline.tax_id.tax_group_id.name=='iva':
                self.iva=self.iva+tline.amount
            if tline.tax_id.tax_group_id.name=='percepcion':
                self.percibido=self.percibido+tline.amount

class SaleOrderOptica(models.Model):
    _inherit = 'sale.order'
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
    cierre_id=fields.Many2one(comodel_name='optica_sv.cierre', string='Cierre')
    oi_esfera = fields.Float("OI. Esfera", required=False)
    oi_cilindro = fields.Float("OI. Cilindro", required=False)
    oi_eje = fields.Float("OI. Eje", required=False)
    oi_adicion = fields.Float("OI. Adicion", required=False)
    oi_prisma = fields.Float("OI. Prisma", required=False)
    oi_oblea = fields.Float("OI. Altura Oblea", required=False)
    oi_pupilar = fields.Float("OI. Altura Pupilar", required=False)
    oi_nasopupilar_cerca = fields.Float("OI. Distancia Nasopupilar Cerca", required=False)
    oi_nasopupilar_lejos = fields.Float("OI. Distancia Nasopupilar Lejos", required=False)
    oi_nasopupilar = fields.Float('OI. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar', required=False)

    od_esfera = fields.Float("OD. Esfera", required=False)
    od_cilindro = fields.Float("OD. Cilindro", required=False)
    od_eje = fields.Float("OD. Eje", required=False)
    od_adicion = fields.Float("OD. Adicion", required=False)
    od_prisma = fields.Float("OD. Prisma", required=False)
    od_oblea = fields.Float("OD. Altura Oblea", required=False)
    od_pupilar = fields.Float("OD. Altura Pupilar", required=False)
    od_nasopupilar_cerca = fields.Float("OD. Distancia Nasopupilar Cerca", required=False)
    od_nasopupilar_lejos = fields.Float("OD. Distancia Nasopupilar Lejos", required=False)
    od_nasopupilar = fields.Float('OD. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar')
    od_nasopupilar = fields.Float('OD. Distancia Nasopupilar Lejos',compute='_compute_nasopupilar')
    es_lente = fields.Boolean("Es Lente")
    base = fields.Float("Base", required=False)
    medida_a = fields.Float("A", required=False)
    medida_b = fields.Float("B", required=False)
    medida_c = fields.Float("C", required=False)
    medida_d = fields.Float("D", required=False)


    @api.one
    @api.depends('oi_nasopupilar_cerca', 'oi_nasopupilar_cerca')
    def _compute_nasopupilar(self):
        self.oi_nasopupilar=self.oi_nasopupilar_cerca+self.oi_nasopupilar_lejos
        self.od_nasopupilar=self.od_nasopupilar_cerca+self.od_nasopupilar_lejos

    antireflejo=fields.Boolean("Antireflejo", required=False)
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

class cierrepago(models.Model):
    _name = 'optica_sv.cierre_pago'
    _description = 'Cierre diario de Diario'
    name=fields.Char("Descripcion del cierre")
    cierre_id=fields.Many2one(comodel_name='optica_sv.cierre', string='Cierre')
    journal_id=fields.Many2one(comodel_name='account.journal', string='Metodo de pago')
    monto=fields.Float("Monto")


class cierresv(models.Model):
    _name = 'optica_sv.cierre'
    _description = 'Cierre diario de LOMED'
    name=fields.Char("Descripcion del cierre")
    comentario=fields.Char("Comentarios del cierre")
    fecha=fields.Date("Fecha del cierre")
    cierrepago_ids=fields.One2many('optica_sv.cierre_pago','cierre_id','Metodos de pago')
    factura_ids=fields.One2many('account.invoice','cierre_id','Facturas')
    venta_ids=fields.One2many('sale.order','cierre_id','Ordenes')
    pago_ids=fields.One2many('account.payment','cierre_id','Pagos')
    sucursal_id=fields.Many2one(comodel_name='stock.location', string='Sucursal de venta',default=lambda self: self.env.user.sucursal_id.id)
    state=fields.Selection(selection=[('Borrador', 'Borrador')
                                        ,('Calculado', 'Calculado')
                                        ,('Cerrado', 'Cerrado')]
                                        , string='Estado')
    total_venta=fields.Float("Total de Ordenes")
    total_facturado=fields.Float("Total de Facturado")
    total_pagado=fields.Float("Total de Pagos")
    #Marcando como cerrado el dia
    def cerrar(self):
        for record in self:
            record.state='Cerrado'

    def liberar(self):
        for record in self:
            orders=self.env['sale.order'].search([('cierre_id','=',record.id)])
            for order in orders:
                order.write({'cierre_id':False})
            facturas=self.env['account.invoice'].search([('cierre_id','=',record.id)])
            for factura in facturas:
                factura.write({'cierre_id':False})
            pagos=self.env['account.payment'].search([('cierre_id','=',record.id)])
            for pago in pagos:
                pago.write({'cierre_id':False})
            cierres=self.env['optica_sv.cierre_pago'].search([('cierre_id','=',record.id)])
            for cierre in cierres:
                cierre.unlink()
            total_venta=0
            total_facturado=0
            total_pagado=0

    def calcular(self):
        for record in self:
            current=record.fecha
            dia=int(datetime.strftime(current, '%d'))
            mes=int(datetime.strftime(current, '%m'))
            anio=int(datetime.strftime(current, '%Y'))
            #resetenado los valores
            total_venta=0
            total_facturado=0
            total_pagado=0
            record.liberar()
            #listando las ordenes de este diari
            hoy_1=datetime(anio,mes,dia,0,0,1)
            hoy_2=datetime(anio,mes,dia,23,59,59)
            hoy_1=hoy_1+timedelta(hours=6)
            hoy_2=hoy_2+timedelta(hours=6)
            orders=self.env['sale.order'].search(['&',('sucursal_id','=',record.sucursal_id.id),('confirmation_date','>=',hoy_1),('confirmation_date','<=',hoy_2)])
            #raise ValidationError("hay ordenes: %s" %orders)
            for order in orders:
                #raise ValidationError("hay ordenes: %s" %order.cierre_id)
                if not order.cierre_id:
                    order.write({'cierre_id':record.id})
                    total_venta=total_venta+order.amount_total
            facturas=self.env['account.invoice'].search(['&',('sucursal_id','=',record.sucursal_id.id),('date_invoice','>=',hoy_1),('date_invoice','<=',hoy_2)])
            for factura in facturas:
                if not factura.cierre_id:
                    factura.write({'cierre_id':record.id})
                    total_facturado=total_facturado+factura.amount_total
            pagos=self.env['account.payment'].search(['&',('sucursal_id','=',record.sucursal_id.id),('payment_date','>=',hoy_1),('payment_date','<=',hoy_2)])
            for pago in pagos:
                if not pago.cierre_id:
                    pago.write({'cierre_id':record.id})
                    total_pagado=total_pagado+pago.amount
            diarios=self.env['account.journal'].search([('id','>',0)])
            for diario in diarios:
                total_diario=0.0
                pagos2=self.env['account.payment'].search(['&',('cierre_id','=',record.id),('journal_id','=',diario.id)])
                for pago2 in pagos2:
                    total_diario=total_diario+pago2.amount
                if total_diario>0:
                    self.env['optica_sv.cierre_pago'].create({'name':diario.name,'cierre_id':record.id,'journal_id':diario.id,'monto':total_diario})
            #raise ValidationError("hay ordenes: %s" %total_venta)
            record.write({'total_venta':total_venta,'total_facturado':total_facturado,'total_pagado':total_pagado})
