#/usr/bin/env python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalesOrderSource(models.Model):
    _name = 'sale.order.source'
    _description = "Sale order source: Model stores sale order source"

    name = fields.Char('Name')
    code = fields.Char('Code')

    provides_label = fields.Boolean('Does this marketplace provide shipping labels')

    relevant_sales = fields.One2many('sale.order', 'sale_order_source', string='Sales Orders')
    relevant_transporters = fields.Many2many('dbt.shipment.transporter', string='Transporters')


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "Bol custom sale order: Model stores 'sale order sources' to 'sale order'"

    sale_order_source = fields.Many2one('sale.order.source','Source Of Order')


class ShipmentTransporter(models.Model) :
    _inherit = "dbt.shipment.transporter"
    _description = "Dbt shipment transporter: Model stores shipment transporter"

    related_source = fields.Many2many('sale.order.source', string='Source Of Transportation')
