# -*- coding: utf-8 -*-
###############################################################################
#
#    Compezant Software Solution Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Compezant Software Solution Pvt. Ltd.(<https://www.Compezant.com>)
#    Author: Arya Vishwakarma
###############################################################################
from odoo import api, fields, models


class PurityUnit(models.Model):
    _name = 'purity.units'
    _description='Purity Master'
    _rec_name='rec_name'

    name=fields.Char(string="Value",placeholder="Set a name like 22",required=True)
    unit=fields.Char(string="Unit",placeholder="Set a Unit like Carat or Percentage(%)")
    rec_name=fields.Char(compute='_compute_rec_name')
    
    @api.model
    def _compute_rec_name(self):
        for rec in self:
            if rec.unit==False:
                rec.rec_name=str(rec.name)
            else:
                rec.rec_name=str(rec.name)+' '+str(rec.unit)
    
    @api.model
    def create_form(self, name, unit,rec_name):
        """ create the request from the users to backend for teams"""
        self.create({
            'name': name,
            'unit': unit,
            'rec_name': rec_name
        })
