from odoo.addons.account.controllers.portal import PortalAccount
from odoo import api, fields, models
import base64
from collections import OrderedDict
from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.account.controllers.download_docs import _get_zip_headers
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class PortalAccountAddon(PortalAccount):
    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type == 'pdf' and download and invoice_sudo.state == 'posted':
            # Download the official attachment(s) or a Pro Forma invoice
            attachments = invoice_sudo._get_invoice_legal_documents()
            if len(attachments) > 1:
                filename = invoice_sudo._get_invoice_report_filename(extension='zip')
                zip_content = attachments.sudo()._build_zip_from_attachments()
                headers = _get_zip_headers(zip_content, filename)
                return request.make_response(zip_content, headers)
            headers = self._get_http_headers(invoice_sudo, report_type, attachments.raw, download)
            return request.make_response(attachments.raw, list(headers.items()))

        elif report_type in ('html', 'pdf', 'text'):
            has_generated_invoice = bool(invoice_sudo.invoice_pdf_report_id)
            request.update_context(proforma_invoice=not has_generated_invoice)
            return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)

        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)

        pdf = request.env['account.move'].sudo().browse(invoice_id).new_invoice
        if pdf:
            file = base64.b64decode(pdf)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(file))]
            return request.make_response(file, headers=pdfhttpheaders)
        else:
            return request.redirect('/my')
            
        return request.render("account.portal_invoice_page", values)
    
