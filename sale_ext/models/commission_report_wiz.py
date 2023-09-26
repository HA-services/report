from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
from odoo.exceptions import UserError
from pytz import timezone, utc
from calendar import monthrange

import logging

_logger = logging.getLogger(__name__)

from io import StringIO
import io

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')

try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')

try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class Commission(models.TransientModel):
    _name = 'commission.report.xls'
    _description = 'Attendance Report'

    user_id = fields.Many2one('res.users', required=True)
    from_date = fields.Date('From Date', required=True, default=lambda self: fields.Datetime.now())
    to_date = fields.Date('To Date', required=True,
                          default=lambda *a: str(datetime.now() + relativedelta.relativedelta(days=7)))

    # ***** Excel Report *****#
    def make_excel(self, portal=False):
        # ***** Excel Related Statements *****#

        sale_order = self.env['sale.order'].search(
            [('date_order', '>=', self.from_date), ('date_order', '<=', self.to_date),
             ('user_id', '=', self.user_id.id)])
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Commission Report")

        style_table_header_top = xlwt.easyxf(
            "font:height 200; font: name Liberation Sans, bold on; align: horiz center;borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour white;")
        style_title = xlwt.easyxf(
            "font:height 200; font: name Liberation Sans, bold on; align: horiz center;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid,  fore_colour white;")
        style_title2 = xlwt.easyxf(
            "font:height 200; font: name Liberation Sans, bold on; align: horiz center;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour silver_ega;")
        style_table_header = xlwt.easyxf(
            "font:height 150; font: name Liberation Sans, bold on; align: horiz left;borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour cyan_ega;")
        style_table_totals = xlwt.easyxf(
            "font:height 150; font: name Liberation Sans, bold on; align: horiz left;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour cyan_ega;")
        style_date_col = xlwt.easyxf(
            "font:height 180; font: name Liberation Sans; align: horiz left;borders: left thin, right thin, top thin, bottom thin;")
        style_date_col2 = xlwt.easyxf(
            "font:height 180; font: name Liberation Sans; align: horiz right;borders: left thin, right thin, top thin, bottom thin;")

        current_user = self.env.user
        company = ""
        if current_user and current_user.company_id:
            company = current_user.company_id.name

        worksheet.write_merge(0, 1, 0, 6, 'Commission Report From ' + self.from_date.strftime(
            '%d-%b-%y') + ' To ' + self.to_date.strftime('%d-%b-%y') + ' For  Salesperson: ' + self.user_id.name,
                              style=style_table_header_top)
        # worksheet.write_merge(0, 1, 2, 3, company, style=style_table_header_top)
        # worksheet.write_merge(0, 1, 4, 10, self.primary_class_id.name, style=style_table_header_top)
        # worksheet.write_merge(2, 2, 2, 3, self.primary_class_id.primary_class_id.department_id.name, style=style_table_header_top)
        #
        # worksheet.write_merge(2, 2, 0, 1, self.primary_class_id.faculty_staff_id.name, style=style_table_header_top)
        # worksheet.write_merge(2, 2, 4, 10,
        #                       self.primary_class_id.primary_class_id.program_id.name + " , " + self.primary_class_id.batch_id.semester_id.name,
        #                       style=style_table_header_top)

        worksheet.row(1).height = 256 * 2
        worksheet.row(2).height = 256 * 2

        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 20
        worksheet.col(2).width = 256 * 20
        worksheet.col(3).width = 256 * 20

        worksheet.col(4).width = 256 * 20
        worksheet.col(5).width = 256 * 20
        worksheet.col(6).width = 256 * 20
        worksheet.col(7).width = 256 * 8
        worksheet.col(8).width = 256 * 8
        worksheet.col(9).width = 256 * 8

        worksheet.write_merge(4, 5, 0, 0, "S.No", style=style_title)
        worksheet.write_merge(4, 5, 1, 1, "Product", style=style_title)
        worksheet.write_merge(4, 5, 2, 2, "Unit Price", style=style_title)
        worksheet.write_merge(4, 5, 3, 3, "Quantity", style=style_title)
        worksheet.write_merge(4, 5, 4, 4, "Sub Total", style=style_title)
        worksheet.write_merge(4, 5, 5, 5, "Commission Rate(%)", style=style_title)
        worksheet.write_merge(4, 5, 6, 6, "Commission Amount", style=style_title)
        # worksheet.write_merge(4, 5, 3, 3, "Department", style=style_title)

        row = 4
        col = 3

        rw = 6
        sr_no = 1
        total_amount = 0
        for st in sale_order:
            for lin in st.order_line:
                worksheet.write(rw, 0, sr_no, style=style_date_col)
                worksheet.write(rw, 1, lin.product_id.name, style=style_date_col)
                worksheet.write(rw, 2, lin.product_uom_qty, style=style_date_col)
                worksheet.write(rw, 3, lin.price_unit, style=style_date_col)
                worksheet.write(rw, 4, lin.price_subtotal, style=style_date_col)
                worksheet.write(rw, 5, lin.commission, style=style_date_col)
                worksheet.write(rw, 6, lin.commission_amount, style=style_date_col)
                # worksheet.write(rw, 3, str(st.student_id.program_id.department_id.name) or "----", style=style_date_col)
                total_amount += lin.commission_amount
                rw += 1
                sr_no += 1

        coll = 3

        rowsss = 6

        worksheet.write_merge(rw + 2, rw + 4, 0, 6, "Total Commission: " + str(total_amount), style=style_title)
        # worksheet.write_merge(rw + 2, rw + 4, 3, 5, total_amount, style=style_date_col)
        # worksheet.write_merge(rw + 2, rw + 4, 6, 8, "Head of Department ", style=style_date_col)

        file_data = io.BytesIO()
        workbook.save(file_data)
        if portal:
            return file_data
        wiz_id = self.env['commission.data.save.wizard'].create({
            'data': base64.encodebytes(file_data.getvalue()),
            'name': 'Commission Report.xls'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Commission Report',
            'res_model': 'commission.data.save.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'target': 'new'
        }


class Commission_data_wizard(models.TransientModel):
    _name = "commission.data.save.wizard"
    _description = 'Commission Save Wizard'

    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)
