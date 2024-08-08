# -*- coding: utf-8 -*-

from odoo import models, fields, api


class jewelleryAddons(models.Model):
        _inherit = ['product.template']




        #metal discription
        metal_type=fields.Many2one(comodel_name='metal.master',string='Metal Name')
        metal_pieces=fields.Integer(string='Metal Pieces',default=0)
        metal_weight=fields.Float(string='Gross Metal Weight',digits=(1,3),default=0)
        metal_color=fields.Char(string='Metal Color/Finish')
        metal_rate=fields.Float(related='metal_type.rate',default=0)
        metal_gross_weight=fields.Float( string="Gross Weight",digits=(1,3))
        metal_net_weight=fields.Float(string="Net Weight/Metal Weight")
        product_text1=fields.Char(Placeholder="text for discription")
        product_text2=fields.Char(Placeholder="text for discription")
        product_text3=fields.Char(Placeholder="text for discription")
        product_text4=fields.Char(Placeholder="text for discription")
        product_text5=fields.Char(Placeholder="text for discription")
        product_text6=fields.Char(Placeholder="text for discription")
        show_price=fields.Boolean(string= "Show Break-Up",default=False)
        sku=fields.Char(string="SKU")
        
        #stone discription
        #stone_detail_ids=fields.Many2many('stone.description',string='Stone Description')
        stone_detail_ids = fields.One2many('stone.description', 'form_id', string='Stone Description')
        

        #making discription
        making_cost=fields.Float(string='Making Cost in %',min=0,default=0)
        
        calculation=fields.Char(compute='_compute_total_metal',default=0,invisible=True)
        
        multipier=fields.Integer(string="Multipier",default=55)
        stone_value_code=fields.Float('Stone Value Code',digits=(1,3),default=0)
    
        def action_set_cost_price(self):
            for rec in self:
                price=rec.calculation
                self.env['product.template'].browse(rec.id).write({'standard_price':price})
                self.env['product.template'].browse(rec.id).write({'list_price':price})
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
 
        metal_cost_total=fields.Float(compute='_compute_total_metal',default=0)
        @api.model
        def _compute_total_metal(self):
            for rec in self:
                value=round((float(rec.metal_rate)*float(rec.metal_weight))*(round((rec.making_cost)/100,4)),2)
                #Metal
                metal_detail={
                    'Gold Purity':rec.metal_type.purity.name,
                    'Gold Weight':rec.metal_weight,
                    'Gross Weight':rec.metal_net_weight,
                }
                price_breakup={
                    'Gold Value':str('₹{:,.2f}'.format(rec.metal_weight*rec.metal_rate)),
                    'Other Elements':str('₹{:,.2f}'.format(55*rec.stone_value_code)),
                    'Making Charge '+str(rec.making_cost)+"%":str('₹{:,.2f}'.format(value)),
                    'Taxes' :"GST"
                }
                stone_detail={}
                for i in rec.stone_detail_ids:
                    key_string1=str(i.stone_type.name)+' Weight'
                    key_string2=str(i.stone_type.name)+' Color'
                    key_string3=str(i.stone_type.name)+' Clarity'
                    stone_detail[key_string1]=i.stone_weight
                    stone_detail[key_string2]=i.stone_color
                    stone_detail[key_string3]=i.stone_Clarity
        
                #On_website_description
                css_string="""<style>
                                table {
                                    border-collapse: collapse;
                                    width: 100%;
                                    color: #5f6265;
                                    }
                                tr {
                                color: #5f6265;
                                }
                                </style>"""
                description_string="<table>"
                for index,(key, value) in enumerate(metal_detail.items()):
                    if value=="" or value==" " or value==None or value==0:
                        continue
                    unitS=""
                    if str(key).__contains__("Weight"):
                        unitS=" gms"
                    if index==0:
                        description_string=description_string+"<tr>"+"<td>&#x2022;"+str(value)+"K Gold"+"</td>""</tr>"
                        continue
                    temp="<tr>"+"<td>&#x2022;"+str(key)+": "+str(value)+unitS+" "+"</td>""</tr>"
                    description_string=description_string+temp

                for index,(key, value) in enumerate(stone_detail.items()):
                    if value=="" or value==" " or value==None or value==0:
                        continue
                    unitS=""
                    if str(key).__contains__("Weight"):
                        unitS=" Ct"
                    temp="<tr>"+"<td>&#x2022;"+str(key)+": "+str(value)+unitS+" "+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text1!="" and rec.product_text1!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text1)+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text2!="" and rec.product_text2!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text2)+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text3!="" and rec.product_text3!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text3)+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text4!="" and rec.product_text4!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text4)+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text5!="" and rec.product_text5!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text5)+"</td>""</tr>"
                    description_string=description_string+temp
                if rec.product_text6!="" and rec.product_text6!=False:
                    temp="<tr>"+"<td>&#x2022;"+str(rec.product_text6)+"</td>""</tr>"
                    description_string=description_string+temp

                description_string=description_string+"</table>"
                
                if rec.show_price==True:
                    description_string=description_string+"<br>"+"<table  style='border:1px '><tr><th><h6>PRICE BREAKUP<h6></th></tr>"
                    for index,(key, value) in enumerate(price_breakup.items()):
                        if value=="" or value==" " or value==None:
                            continue
                        unitS=""
                        if str(key).__contains__("Weight"):
                            unitS=" gms"
                        temp="<tr>"+"<td style='font-color: #5f6265'>&#x2022;"+str(key)+" "+"</td>"+"<td>"+str(value)+unitS+" "+"</td>""</tr>"
                        description_string=description_string+temp
                    description_string=description_string+"</table>"
                rec.description_ecommerce=css_string+description_string

                #Multipier
                multipier_code_value=self.env['purity.units'].search([('name','=','MULTIPIER')])
                mul_code=55
                for i in multipier_code_value:
                    mul_code=self.env['purity.units'].browse(i.id).rate
                    break
                
                stone_code_multiple=mul_code*rec.stone_value_code
                rec.metal_cost_total=float(str(float(stone_code_multiple)+(float(rec.metal_rate)*float(rec.metal_weight))))
               
                #standaard price
                product_id=self.env['product.template'].search([('name','=',str(rec.name))])
                for i in product_id:
                    value=round((i.metal_cost_total)*(1+round((i.making_cost)/100,2)),2)
                    self.env['product.template'].browse(i.id).write({'standard_price':0})
                
                value=round((float(rec.metal_rate)*float(rec.metal_weight))*(1+round((rec.making_cost)/100,4)),2)+stone_code_multiple
                rec.calculation=value
        
                   
        def action_confirm(self):
            super(jewelleryAddons,self).action_confirm()


class stoneDiscription(models.Model):
    _name = 'stone.description'
    _description = 'Stone Discription'
    _rec_name='rec_name'

    stone_type=fields.Many2one('stone.master',string='Stone Name')
    stone_quantity=fields.Integer(string='Pcs',default=0)
    stone_weight=fields.Float(string='Stone Weight',digits=(1,3),default=0)
    stone_Clarity=fields.Char(string='Clarity')
    stone_discription=fields.Char(string='Stone Discription')
    stone_color=fields.Char(string="Color")
    rec_name=fields.Char(compute='_compute_rec_name',string='Stone Detail')
    form_id = fields.Many2one('product.template', 'Form Id', ondelete='cascade', required=True)
	
      
    @api.depends('stone_type')
    def _compute_rec_name(self):
        for rec in self:
            if (rec.stone_type.rec_name== False):
                rec.rec_name="" 
            else:
                rec.rec_name=str(rec.stone_type.rec_name)
    
    