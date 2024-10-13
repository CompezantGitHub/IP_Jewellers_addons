# -*- coding: utf-8 -*-
import odoo.http as http

class Academy(http.Controller):
    @http.route('/tracking/<int:tracking_id>', auth='public')
    def index(self,tracking_id, **kw):
        return http.request.render('jewellery_master.sequel_page', {
            'id':tracking_id,
        })