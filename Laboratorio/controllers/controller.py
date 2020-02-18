from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class Registro(http.Controller):
    #SELECT A UTILIZAR
    @http.route('/select/clientes',  type='http', auth="none", website=True)
    def fiaes_select_country(self, **kwargs):
        _logger.info('Conexion controller')
        return_string = ""
        countries = request.env['res.partner'].sudo().search([])
        separador= ""
        if countries:
            return_string += "{ 'collection' :[" 
            for cliente in countries:
                if cliente.ref:
                    return_string  += separador + "{'id':" + str(cliente.id) +",'code':'" + cliente.ref +"','nombre':'"+ cliente.name +"'}"
                    separador = ","
            return_string  += "]}"
            
            new_string= str(return_string).replace("'",'"')
            
        return new_string


    
    
