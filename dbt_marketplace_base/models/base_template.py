#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.addons.queue_job.job import job

_logger = logging.getLogger(__name__)


class DbtMarketplaceBase(models.Model):
    _name = 'dbt.marketplace.base'

    _debug = True

    name = fields.Char('Name')
    active = fields.Boolean('Active')
    connected = fields.Boolean('Connection Tested')

    latest_order_count = fields.Integer("New Order Count")

    enable_order_fetching = fields.Boolean('Enable Order fetching')
    enable_product_to_sync = fields.Boolean('Enable Product To Sync')
    enable_product_from_sync = fields.Boolean('Enable Product From Sync')
    enable_shipment_sync = fields.Boolean('Enable Shipment Sync')

    child_class_name = fields.Char('Name of child class')
    child_class_id = fields.Integer('id of child class record')

    # order_fetch_function = fields.Char('Order Fetch Function')
    # product_to_sync_function = fields.Char('Product To Sync Function')
    # product_from_sync_function = fields.Char('Product From Sync Function')
    # shipment_sync_function = fields.Char('Shipment Sync Function')

    color = fields.Integer(string='Color Index',
                           help="The color of the channel")

    # @api.model
    # def write(self, vals):
    #     self.log(vals)
    #     record = super(DbtMarketplaceBase, self).write(vals)
    #     return record

    def log(self, msg):
        if self._debug:
            _logger.info(msg)

    @api.multi
    def fetch_order_action(self):
        self.log("Inside fetch_orders for marketplace")
        self.log(self.enable_order_fetching)
        if self.enable_order_fetching and self.child_class_name and self.child_class_id:
            self.log("Function calling starts")
            self.log(self.child_class_name)
            self.log(self.child_class_id)
            self.log("Child class found")
            self.env[self.child_class_name].browse(
                self.child_class_id).with_delay().fetch_orders()

    @job
    def fetch_orders(self):
        raise NotImplementedError('Must be overrided in child class')

    @job
    def sync_to_produts(self):
        raise NotImplementedError('Must be overrided in child class')

    @job
    def sync_from_products(self):
        raise NotImplementedError('Must be overrided in child class')

    @job
    def sync_shipments(self):
        raise NotImplementedError('Must be overrided in child class')

    ## The functions needed to open appropriate window for view actions of dashboard ##
    def view_all_orders(self):
        self.log("Inside view all orders: base")
        # raise NotImplementedError('Must be overrided in child class')
        if self.child_class_name and self.child_class_id:
            return self.env[self.child_class_name].browse(
                self.child_class_id).view_all_orders()

    def view_pending_orders(self):
        raise NotImplementedError('Must be overrided in child class')

    def view_shipment(self):
        raise NotImplementedError('Must be overrided in child class')        