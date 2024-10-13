from odoo import models, fields, api
import json
from odoo import http
from odoo.http import request
import requests
import asyncio
import urllib


class invoiceAddons(models.Model):
    _inherit = ['account.move']

    #By Compezant
    new_invoice = fields.Binary(string='New Invoice')
    new_invoice_number=fields.Char(string="New Invoice No:", default="CINV0001", placeholder="CNV00001")
    tracking_id=fields.Char(string="Tracking ID ")
    tracking_url=fields.Char(string="url",compute='get_tracking_detail')
    '''
    delivery_date=fields.Char(string="Delivery Date",compute='delivery_date_calculation')
    track_status=fields.Selection(
        selection=[
            ('yet_to_Despatch', 'Yet to Despatch'),
            ('SCREATED', 'Shipment is Created'),
            ('SCHECKIN', 'Shipment picked up'),
            ('SLINREC', 'Checked into the hub'),
            ('SLINORIN', 'Departured from origin HUB'),
            ('SLINDEST', 'Arrived at destination HUB'),
            ('SDELASN', 'Shipment out for deliver'),
            ('SDELVD', 'Shipment is delivered')
        ],
        string="track status",
        required=True,
        default='yet_to_Despatch',
        help="Track Status.")
    current_location=fields.Char(string="Current Location",default="Delhi")
    last_date=fields.Char(string="Last Date")

    def delivery_date_calculation(self):
        for rec in self:
            url = "https://sequel247.com/api/track"
            track_id="30304040"
            if rec.tracking_id!= None:
                track_id=str(rec.tracking_id)
            # Data to be sent
            data = {
                "token": "974a83c8c20e7ddb1e49f8abe4382299",
                "docket" : track_id
            }

            # A POST request to the API
            response = requests.post(url, json=data)
            # Print the response
            if str(response.json()['status'])=="false":
                rec.delivery_date='Yet to despatch'
                rec.track_status='yet_to_Despatch'
                rec.current_location="Delhi"
                rec.last_date=""
            else:
                rec.delivery_date=str(response.json()['data']["estimated_delivery"])
                if response.json()['data']["tracking"][-1]["location"]!=None or response.json()['data']["tracking"][-1]["location"]!=False:
                    rec.current_location=str(response.json()['data']["tracking"][-1]["location"])
                rec.last_date=str(response.json()['data']["tracking"][-1]["date_time"])
                if str(response.json()['data']["shipment_status"])=="SCREATED":
                    rec.track_status='SCREATED'
                elif str(response.json()['data']["shipment_status"])=="SPU":
                    rec.track_status='SCHECKIN'
                elif str(response.json()['data']["shipment_status"])=="SCHKINORIGN":
                    rec.track_status='SLINREC'
                elif str(response.json()['data']["shipment_status"])=="SLINORIN":
                    rec.track_status='SLINORIN'
                elif str(response.json()['data']["shipment_status"])=="SLINDEST":
                    rec.track_status='SLINDEST'
                elif str(response.json()['data']["shipment_status"])=="SDELASN":
                    rec.track_status='SDELASN'
                else:
                    rec.track_status='SDELVD'

    '''
    def get_tracking_detail(self):
        for rec in self:
            rec.tracking_url="https://sequel247.com/track/"+str(rec.tracking_id)
        