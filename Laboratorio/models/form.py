from odoo import api, models, fields, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__) 


class Formlomed(models.Model):
    _name = 'lomed.formoptica'
    partner_id = fields.Many2one(comodel_name='res.partner')
    name = fields.Char(string="Paciente")
    optica = fields.Char(string="Óptica")
    optica_id = fields.Integer()
    optica_copia = fields.Char(string="Optica copia")
    #date = fields.Char(string="Fecha")
    date1 = fields.Char(string="Fecha")
    #ref1 = fields.Char(string="#Orden")
    ref = fields.Char(string="#Orden")
    #OD  
    od_esfera = fields.Float(string="OD.Esfera")
    od_cilindro = fields.Float(string="OD.Cilindro")
    od_eje = fields.Float(string="OD.Eje")
    od_adicion= fields.Float(string="OD.adicion")
    od_prisma = fields.Float(string="OD.Prisma")
    #OI
    oi_esfera = fields.Float(string="OI.Esfera")
    oi_cilindro = fields.Float(string="OI.Cilindro")
    oi_eje = fields.Float(string="OI.Eje")
    oi_adicion= fields.Float(string="OI.adicion")
    oi_prisma = fields.Float(string="OI.Prisma")
    #form
    policar = fields.Char(string="Policarbonato")
    cr_49 = fields.Char(string="CR-49")
    anti= fields.Boolean(string="Antireflejo")
    clase = fields.Char(string="Clase de lentes") 
    color =fields.Float(string="Color")
    base =fields.Float(string="Base")
    #OD
    od_alt_oblea = fields.Float(string="Altura Oblea")
    od_alt_pupilar = fields.Float(string="Altura Pupilar")
    od_alt_lejos = fields.Float(string="D.P. Lejos")
    od_alt_cerca = fields.Float(string="D.P. Cerca")
    #OI
    oi_alt_oblea = fields.Float(string="Altura Oblea")
    oi_alt_pupilar = fields.Float(string="Altura Pupilar")
    oi_alt_lejos = fields.Float(string="D.P. Lejos")
    oi_alt_cerca = fields.Float(string="D.P. Cerca")
    #form 2
    aro = fields.Char(string="Aro")
    medida = fields.Char(string="Medida")  
    examino = fields.Char(string="Examino") 
    asesor = fields.Char(string="Asesor Visual")
    fecha_entrega = fields.Date(string="Fecha de entrega") 
    color2 = fields.Char(string="Color")
    a = fields.Float(string="A")
    b = fields.Float(string="B")
    c = fields.Float(string="C")
    d = fields.Float(string="D") 
    observaciones = fields.Char(string="Observaciones")
    state = fields.Selection(selection=[('Borrador', 'Borrador')
                                    ,('Aprobado', 'Aprobado')]
                                    , string='Estado',default='Borrador',store=True)
    producto_id = fields.Many2one(comodel_name='product.product')
    tipo_id = fields.Many2one(string="Tipo", comodel_name='lomed.opticatipo')
    material_id = fields.Many2one(string="Material", comodel_name='lomed.opticamaterial')
    color_id = fields.Many2one(string="Color", comodel_name='lomed.opticacolor')
    lente_id = fields.Many2one(string="Lente", comodel_name='lomed.opticalentenom')
    opticalentes_id = fields.Many2one(comodel_name='lomed.opticalentes')
    image = fields.Text(compute='calculo')
    barcode = fields.Char()
    variable = fields.Char(string="variable")
    activate = fields.Boolean()
    tipo_trabaajo = fields.Selection(selection=[('Requisicion', 'Requisicion')
                                    ,('Reclamo', 'Reclamo')
                                    ,('Montaje','Montaje')
                                    ,('Tallado','Tallado')
                                    ,('Mat Propio','Mat Propio')
                                    ,('Otros','Otros')]
                                    , string='Tipo de trabajo ',store=True)  
    ordenes = fields.One2many(comodel_name='sale.order',string="Ordenes", compute='orden')

    @api.multi
    @api.depends('ref')
    def orden(self):
        for r in self:
            list = self.env['sale.order'].search([('partner_id','=',r.ref)])
            r.ordenes = list            
    
   
    @api.one
    @api.depends('partner_id','name')
    def calculo(self):
        dia= ''
        today = datetime.now()
        variable = ''
        for r in self:
            antireflejo = r.anti
            tt = today.timetuple()
            if tt.tm_wday == 0:
                dia = 'LU'
            if tt.tm_wday == 1:
                dia='MA'
            if tt.tm_wday == 2:
                dia='MI'
            if tt.tm_wday == 3:
                dia= 'JU' 
            if tt.tm_wday == 4:
                dia = 'VI'
            if tt.tm_wday == 5:
                dia = 'SA'
            if tt.tm_wday == 6:
                dia = 'DO'
            if antireflejo == True:
                variable= dia + 'A'
            else:
                variable = dia
             
            text = " <div style=""display:flex;""> <div style=""float:left;margin:5px;""> "
            partner_id = self.env['res.partner'].search([('ref','=',r.ref)],limit=1)  
            text +="<ul style=""list-style:none;margin:0;padding:0;font-size:10px;font-weight:bold;letter-spacing:0.3em"" >"
            text += "<li>LOMED, S.A DE C.V</li>"
            if partner_id:
                text += "<li>"+ str(partner_id.name)+"</li>"
            text += "<li>"+ "Ref: " +str(r.ref)+"</li>"
            if r.name:
                text += "<li>"+r.name+"</li>"
            if r.optica_copia:
                text += "<li>"+r.optica_copia+"</li>" 
            text += "<li>"+str('{:%d / %m / %Y %H:%M:%S }'.format(datetime.now()))+"</li>"
            text +="</ul>"
            if not r.barcode:
                r.barcode = self.env['ir.sequence'].next_by_code('lomed.order') #Crear una secuencia en odoo        
            text += "<div style=""display:flex;""><div style=""float:left;""><img style='height:70px;widht:200px' src='https://barcode.tec-it.com/barcode.ashx?data="+r.barcode+"%0A&code=&multiplebarcodes=true&translate-esc=true&unit=Fit&dpi=96&imagetype=Gif&rotation=0&color=%23000000&bgcolor=%23ffffff&qunit=Mm&quiet=0' alt='Barcode Generator TEC-IT'/></div>"   
            text += "<div style=""float:left;""><p style=""font-family:Sans-Serif;font-weight:bold;font-size:20px;"">"+str(variable)+"</p></div></div>"
            text += " </div> <div style=""float:left;margin:5px;""> "
            text +="<ul style=""list-style:none;margin:0;padding:0;font-size:10px;font-weight:bold;letter-spacing:0.3em"" >"
            text += "<li>LOMED, S.A DE C.V</li>"
            if partner_id:
                text += "<li>"+ str(partner_id.name)+"</li>"
            text += "<li>"+"Ref: "+str(r.ref)+"</li>"
            if r.name:
                text += "<li>"+r.name+"</li>"
            if r.optica_copia:
                text += "<li>"+r.optica_copia+"</li>" 
            text += "<li>"+str('{:%d / %m / %Y %H:%M:%S }'.format(datetime.now()))+"</li>"
            text +="</ul>"
            if not r.barcode:
                r.barcode = self.env['ir.sequence'].next_by_code('lomed.order')         
            text += "<div style=""display:flex;""><div style=""float:left;""><img style='height:70px;widht:150px' src='https://barcode.tec-it.com/barcode.ashx?data="+r.barcode+"%0A&code=&multiplebarcodes=true&translate-esc=true&unit=Fit&dpi=96&imagetype=Gif&rotation=0&color=%23000000&bgcolor=%23ffffff&qunit=Mm&quiet=0' alt='Barcode Generator TEC-IT'/></div>"   
            text += "<div style=""float:left;""><p style=""font-family:Sans-Serif;font-weight:bold;font-size:20px;"">"+str(variable)+"</p></div></div>"
            text += "</div> </div> "
            r.image = text
         
    @api.multi
    def historial1(self):
        self.ensure_one()
        action_ref = self.env.ref('sale.view_quotation_tree')
        if not action_ref:
            return False
        action_data = action_ref.read()[0]
        _logger.info(action_data)
        _logger.info('Lomed')
        return action_data

#crear al objeto atributo one2many sale.order compute devolverle el listado de las ordenes del cliente 

            
    @api.multi
    def historial(self):
        self.ensure_one()
        compose_form = self.env.ref('Laboratorio_optico.lomed_form_tree', False)
        ctx = dict(
            default_activo_id=self.id,
        )
        return {
            'name': 'new',
            'type': 'ir.actions.act_window',
            'view_type': 'list',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'views': [(compose_form.id, 'tree')],
            'target': 'new',
            'view_id': 'compose_form.id',
            'flags': {'action_buttons': True},
            'context': ctx
        }
        
    @api.multi
    def aprobado(self):
        for r in self:
            r.state='Aprobado'
            compra = self.env['lomed.opticalentes'].search([('tipo_id','=',r.tipo_id.id),('material_id','=',r.material_id.id),('color_id','=',r.color_id.id),('lente_id','=',r.lente_id.id)],limit=1)
            if compra: 
                partner_id = self.env['res.partner'].search([('ref','=',r.ref)],limit=1)  
                dic={}
                dic['name'] = self.env['ir.sequence'].next_by_code('lomed.order')
                dic['partner_id'] = partner_id.id
                dic['date_order'] =  datetime.now()
                dic['od_esfera']=r.od_esfera
                dic['od_cilindro']=r.od_cilindro
                dic['od_eje']=r.od_eje
                dic['od_adicion']=r.od_adicion
                dic['od_prisma']=r.od_prisma
                dic['oi_esfera']=r.oi_esfera
                dic['oi_cilindro']=r.oi_cilindro
                dic['oi_eje']=r.oi_eje
                dic['oi_adicion']=r.oi_adicion
                dic['oi_prisma']=r.oi_prisma
                dic['policar']=r.policar
                dic['cr_49']=r.cr_49
                dic['anti']=r.anti
                dic['clase']=r.clase
                dic['color']=r.color
                dic['base']=r.base
                dic['od_alt_oblea']=r.od_alt_oblea
                dic['od_alt_pupilar']=r.od_alt_pupilar
                dic['od_alt_lejos']=r.od_alt_lejos
                dic['od_alt_cerca']=r.od_alt_cerca
                dic['oi_alt_oblea']=r.oi_alt_oblea
                dic['oi_alt_pupilar']=r.oi_alt_pupilar
                dic['oi_alt_lejos']=r.oi_alt_lejos
                dic['aro']=r.aro
                dic['medida']=r.medida
                dic['examino']=r.examino
                dic['asesor']=r.asesor
                dic['fecha_entrega']=r.fecha_entrega
                dic['color2']=r.color2
                dic['a']=r.a
                dic['b']=r.b
                dic['c']=r.c
                dic['d']=r.d
                dic['observaciones']=r.observaciones 
                trabajo= self.env['sale.order'].create(dic)
                line = self.env['sale.order.line'].create({'name': compra.des, 'order_id': trabajo.id,'price_unit': compra.producto_id.list_price,'product_id':compra.producto_id.id}) 
                
            model_obj = self.env['ir.model.data']
            data_id = model_obj._get_id('Laboratorio_optico','lomed_form_1')
            view_id = model_obj.browse(data_id).res_id
            return {
                'type': 'ir.actions.act_window',
                'name': _('String'),
                'res_model': 'lomed.formoptica',
                'view_type' : 'form',
                'view_mode' : 'form', 
                'view_id' : view_id,
                'target' : 'current',
                'nodestroy' : True,
             }
            
    class lomedTipo(models.Model):
        _name = 'lomed.opticatipo'
        name = fields.Char(string="Name")
        
    class lomedMaterial(models.Model):
        _name = 'lomed.opticamaterial'
        name = fields.Char(string="Name")
        tipo_id = fields.Many2one(string="Tipo", comodel_name='lomed.opticatipo')   
        
    class lomedColor(models.Model):
        _name = 'lomed.opticacolor'
        name = fields.Char(string="Name")
        material_id = fields.Many2one(string="Material", comodel_name='lomed.opticamaterial')
        
    class lomedlentenom(models.Model):
        _name = 'lomed.opticalentenom'
        name = fields.Char(string="Name")
        color_id = fields.Many2one(string="Color", comodel_name='lomed.opticacolor')
        
    class lomedLente(models.Model):
        _name = 'lomed.opticalentes'
        name = fields.Char(string="Name")         
        tipo_id = fields.Many2one(string="Tipo", comodel_name='lomed.opticatipo')
        material_id = fields.Many2one(string="Material", comodel_name='lomed.opticamaterial')
        color_id = fields.Many2one(string="Color", comodel_name='lomed.opticacolor')
        lente_id = fields.Many2one(string="Lente", comodel_name='lomed.opticalentenom')
        producto_id = fields.Many2one(comodel_name='product.product')
        des = fields.Char(string="Descripcion")     
   