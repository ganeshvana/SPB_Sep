# -*- coding: utf-8 -*-
from odoo import models,fields,api, _

class HSNInvoice(models.TransientModel):
    _name = 'wizard.invoice.report'
    _description = 'HSN invoice report'

    invoice_ids = fields.Many2many('account.invoice')

    @api.model
    def default_get(self, fields):
        res = super(HSNInvoice, self).default_get(fields)
        invoice_ids = self.env['account.invoice'].browse(self._context.get('active_ids'))
        res.update({'invoice_ids': invoice_ids and invoice_ids.ids or False})
        return res

    @api.multi
    def print_report(self):
        return self.env.ref('hsn_invoice_report.action_hsn_invoice_report').report_action(self)

class HSNXlsx(models.AbstractModel):
    _name = 'report.hsn_invoice_report.invoice_hsn_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'HSN Invoice Reprt'

    def _get_report_lines(self, lines):
        data = {}
        for line in lines:
            if line.product_id.l10n_in_hsn_code in data.keys():
                data[line.product_id.l10n_in_hsn_code] |= line
            else:
                if line.product_id.l10n_in_hsn_code:
                    data[line.product_id.l10n_in_hsn_code] = line 
                else:
                    data['no_hsn_%s' % line.id] = line
        return data

    def generate_xlsx_report(self, workbook, data, order):
        for rec in order:
            sheet = workbook.add_worksheet('Eway Bill Report')
            format3 = workbook.add_format({'font_size': 12, 'bg_color': '#328ba8','bold': True})
            format1 = workbook.add_format({'font_size': 10, 'bg_color': '#ffcce6','bold': True,'border': 1})
            format2 = workbook.add_format({'font_size': 10, 'bg_color': '#ffffff','border': 1})
            format4 = workbook.add_format({'font_size': 10, 'bg_color': '#ffffff','border': 1, 'num_format': 'mm/dd/yy'})
            sheet.set_column('A15:A16',20)
            sheet.set_column('B17:B18',15)
            sheet.set_column('C19:C20',20)
            sheet.set_column('D21:D22',18)
            sheet.set_column('E23:E24',15)
            sheet.set_column('F25:F26',12)
            sheet.write(0, 2, 'Ebill Invoice Report', format3)
            sheet.write(1, 0, 'Invoice Number', format1)
            sheet.write(1, 1, 'Invoice Date', format1)
            sheet.write(1, 2, 'Customer Name', format1)
            sheet.write(1, 3, 'HSN Code', format1)
            sheet.write(1, 4, 'Total Qty', format1)
            sheet.write(1, 5, 'Taxable Value', format1)
            row = 2
            datas = []
            for invoice in order.invoice_ids:
                datas += list(self._get_report_lines(invoice.invoice_line_ids.filtered(lambda x : x.invoice_id.state == 'open')).values())
            for line in datas:
                sheet.write(row, 0, line.mapped('invoice_id.number')[0], format2)
                sheet.write(row, 1, line.mapped('invoice_id.date')[0], format4)
                sheet.write(row, 2, line.mapped('invoice_id.partner_id.name')[0], format2)
                sheet.write(row, 3, line.mapped('product_id.l10n_in_hsn_code')[0], format2)
                sheet.write(row, 4, sum(line.mapped('quantity')), format2)
                sheet.write(row, 5, sum(line.mapped('price_subtotal')), format2)
                row += 1
