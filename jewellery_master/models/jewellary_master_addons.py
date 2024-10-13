# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests


class jewelleryAddons(models.Model):
        _inherit = ['product.template']




        #metal discription
        metal_type=fields.Many2one(comodel_name='metal.master',string='Metal Name')
        metal_pieces=fields.Integer(string='Metal Pieces',default=0)
        metal_weight=fields.Float(string='Gross Metal Weight',digits=(1,3),default=0) #Net Weight
        metal_color=fields.Char(string='Metal Color/Finish')
        metal_rate=fields.Float(related='metal_type.rate',digits=(1,2),default=0)
        metal_gross_weight=fields.Float( string="Gross Weight",digits=(1,3))
        metal_net_weight=fields.Float(string="Gross Weight",digits=(1,3)) # Gross Weight
        product_text1=fields.Char(Placeholder="text for discription")
        product_text2=fields.Char(Placeholder="text for discription")
        product_text3=fields.Char(Placeholder="text for discription")
        product_text4=fields.Char(Placeholder="text for discription")
        product_text5=fields.Char(Placeholder="text for discription")
        product_text6=fields.Char(Placeholder="text for discription")
        show_price=fields.Boolean(string= "Show Break-Up",default=False)
        show_bis=fields.Boolean(string= "Show Hallmark",default=True)
        sku=fields.Char(string="SKU")
        @api.constrains('sku')
        def _check_sku_unique(self):
            sku_counts = self.search_count([('sku', '=', self.sku), ('id', '!=', self.id)])
            if sku_counts  > 0:
                raise ValidationError("Sku already exists!")
        
        #stone discription
        #stone_detail_ids=fields.Many2many('stone.description',string='Stone Description')
        stone_detail_ids = fields.One2many('stone.description', 'form_id', string='Stone Description')
        

        #making discription
        making_cost=fields.Float(string='Making Cost in %',min=0,default=0)
        making_cost_per_gram=fields.Float(string='Making Cost per gram',min=0,default=0)
        
        calculation=fields.Char(compute='_compute_total_metal',default=0,invisible=True)
        
        #multipier=fields.Integer(string="Multipier",compute='_compute_total_metal',default=55,readonly=True)
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
                sm=""
                other_element='Stone/Diamond Value'
                if rec.categ_id.id==7:
                    sm='DMUL'
                    other_element='Stone/Diamond Value'
                elif rec.categ_id.id==8:
                    sm='PMUL'
                    other_element='Stone/Diamond Value'
                else:
                    sm='GMUL'
                multipier_code_value=self.sudo().env['purity.units'].search([('name','=',str(sm))])
                mul_code=55.0
                for i in multipier_code_value:
                    mul_code=float(self.sudo().env['purity.units'].browse(i.id).unit)
                    break
                value=round((float(rec.metal_rate)*float(rec.metal_weight))*(round((rec.making_cost)/100,4)),2)+int(float(rec.making_cost_per_gram)*float(mul_code))
                #Metal
                metal_detail={
                    'Gold Purity':rec.metal_type.purity.name,
                    'Gross Weight':round(float(rec.metal_net_weight),3),
                    'Net Weight':round(float(rec.metal_weight),3),
                }
                gst_value=0.0
                if rec.taxes_id:
                    gst_value=round(round(int(str(rec.taxes_id.name[0]))/100,2)*(rec.list_price),2)

                sm=""
                other_element='Stone/Diamond Value'
                if rec.categ_id.id==7:
                    sm='DMUL'
                    other_element='Stone/Diamond Value'
                elif rec.categ_id.id==8:
                    sm='PMUL'
                    other_element='Stone/Diamond Value'
                else:
                    sm='GMUL'
                    other_element="Stone Value"
                multipier_code_value=self.sudo().env['purity.units'].search([('name','=',str(sm))])
                mul_code=55.0
                for i in multipier_code_value:
                    mul_code=float(self.sudo().env['purity.units'].browse(i.id).unit)
                    break

                making_string=str(rec.making_cost)+str(" %")
                if rec.making_cost==0 or rec.making_cost==False or rec.making_cost==None:
                    making_string=""
                price_breakup={
                    'Gold Value':str('₹{:}'.format(int(rec.metal_weight*rec.metal_rate))),
                    str(other_element):str('₹{:}'.format(int(mul_code*rec.stone_value_code))),
                    'Making Charge '+str(making_string):str('₹{:}'.format(int(value))),
                    'GST' : str('₹{:}'.format(int(gst_value)+1))
                }
                if rec.categ_id.id==7:
                    price_breakup={
                    str(other_element):str('₹{:}'.format(int(mul_code*rec.stone_value_code))),
                    'Gold Value':str('₹{:}'.format(int(rec.metal_weight*rec.metal_rate))),
                    'Making Charge '+str(making_string):str('₹{:}'.format(int(value))),
                    'GST' : str('₹{:}'.format(int(gst_value)+1))
                }

                stone_detail={}
                for i in rec.stone_detail_ids:
                    key_string1=str(i.stone_type.name)
                    key_string2=str(i.stone_type.name)
                    key_string3=str(i.stone_type.name)
                    key_string1=key_string1.capitalize()
                    key_string2=key_string2.capitalize()
                    key_string3=key_string3.capitalize()
                    key_string1=str(key_string1)+' Weight'
                    key_string2=str(key_string2)+' Color'
                    key_string3=str(key_string3)+' Clarity'
                    stone_detail[key_string1]=round(float(i.stone_weight),3)
                    stone_detail[key_string2]=i.stone_color
                    stone_detail[key_string3]=i.stone_Clarity
        
                #On_website_description
                #tr {color: #5f6265;}
                css_string="""<style>
                                table {
                                    border-collapse: collapse;
                                    width: 100%;
            
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
                        Gold_Name=""
                        for i in rec.metal_type.name:
                            Gold_Name=Gold_Name+i
                        Gold_Name=Gold_Name.capitalize()
                        Gold_Purity_Symbol=rec.metal_type.purity.unit
                        if rec.categ_id.id==12 or rec.categ_id.id==11:
                            description_string=description_string+"<tr>"+"<td>&#x2022;"+str(value)+str(Gold_Purity_Symbol)+" "+str(Gold_Name)+" "+"</td>""</tr>"
                        else:
                            description_string=description_string+"<tr>"+"<td>&#x2022;"+str(value)+str(Gold_Purity_Symbol)+" "+str(Gold_Name)+" "+"Jewellery"+"</td>""</tr>"
                        continue
                    temp="<tr>"+"<td>&#x2022;"+str(key)+": "+str('{:.3f}'.format(value))+unitS+" "+"</td>""</tr>"
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
                        if value=="" or value=="₹0" or value==None or value==0 or value== False or value==" ":
                            continue
                        unitS=""
                        if str(key).__contains__("Weight"):
                            unitS=" gms"
                        #style='font-color: #5f6265'
                        temp="<tr>"+"<td>&#x2022;"+str(key)+" "+"</td>"+"<td>"+str(value)+unitS+" "+"</td>""</tr>"
                        description_string=description_string+temp
                    description_string=description_string+"</table>"
                rec.description_ecommerce=css_string+description_string

                sm=""
                if rec.categ_id.id==7:
                    sm='DMUL'
                elif rec.categ_id.id==8:
                    sm='PMUL'
                else:
                    sm='GMUL'
                multipier_code_value=self.sudo().env['purity.units'].search([('name','=',str(sm))])
                mul_code=55.0
                for i in multipier_code_value:
                    mul_code=float(self.sudo().env['purity.units'].browse(i.id).unit)
                    break
                
                stone_code_multiple=mul_code*rec.stone_value_code
                rec.metal_cost_total=float(str(float(stone_code_multiple)+(float(rec.metal_rate)*float(rec.metal_weight))))
               
                #standaard price
                product_id=self.env['product.template'].search([('name','=',str(rec.name))])
                for i in product_id:
                    value=round((i.metal_cost_total)*(1+round((i.making_cost)/100,2)),2)
                    self.env['product.template'].browse(i.id).write({'standard_price':0})
                
                value=round((float(rec.metal_rate)*float(rec.metal_weight))*(1+round((rec.making_cost)/100,4)),2)+stone_code_multiple+int(float(rec.making_cost_per_gram)*float(mul_code))
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
    
    