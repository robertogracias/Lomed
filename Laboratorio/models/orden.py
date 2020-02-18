from odoo import api, models, fields, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID

class ordenTrabajo(models.Model):
    _inherit= 'sale.order'
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
    
    