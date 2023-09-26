# -*- coding: utf-8 -*-
import pdb
import calendar

from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from pytz import timezone

from odoo import api, fields, models, _
import pytz
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    commission = fields.Float('Commission Rate', tracking=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    commission = fields.Float(related="product_tmpl_id.commission", string='Commission Rate', tracking=True, store=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    commission = fields.Float(compute="calculate_commission_rate", string='Commission Rate', tracking=True, store=True)
    commission_amount = fields.Float(string='Commission Amount', compute="calculate_commission", tracking=True,
                                     store=True)

    @api.depends('product_id', 'product_uom_qty', 'price_unit')
    def calculate_commission_rate(self):
        for rec in self:
            rec.commission = rec.product_id.commission

    @api.depends('product_id', 'commission', 'product_uom_qty', 'price_unit')
    def calculate_commission(self):
        for rec in self:
            rec.commission_amount = (rec.price_subtotal * rec.commission) / 100
