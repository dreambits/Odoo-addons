#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from odoo.addons.queue_job.job import job

_logger = logging.getLogger(__name__)


class DbtMarketplaceBase(models.Model):
    _name = 'dbt.marketplace.base'

    _debug = True

    name = fields.Char('Name')
    active = fields.Boolean('Active')
    connected = fields.Boolean('Connection Tested')

    latest_order_count = fields.Integer("New Order Count", compute="get_latest_order_count")

    enable_order_fetching = fields.Boolean('Enable Order fetching')
    enable_product_to_sync = fields.Boolean('Enable Product To Sync')
    enable_product_from_sync = fields.Boolean('Enable Product From Sync')
    enable_shipment_sync = fields.Boolean('Enable Shipment Sync')

    child_class_name = fields.Char('Name of child class')
    child_class_id = fields.Integer('id of child class record')

    color = fields.Integer(string='Color Index',
                           help="The color of the channel")

    def log(self, msg):
        if self._debug:
            _logger.info(msg)

    @api.depends('child_class_id','child_class_name')
    def get_latest_order_count(self):
        try:
            for rec in self:
                if rec.child_class_name and rec.child_class_id:
                    rec.latest_order_count = rec.env[rec.child_class_name].browse(
                            rec.child_class_id
                        ).bol_instance.latest_order_count
        except:
            traceback.print_exc()

    @api.multi
    def fetch_order_action(self):
        try:
            self.log("Inside fetch_orders for marketplace")
            self.log(self.enable_order_fetching)
            if self.enable_order_fetching and self.child_class_name and self.child_class_id:
                self.log("Function calling starts")
                self.log(self.child_class_name)
                self.log(self.child_class_id)
                self.log("Child class found")
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().fetch_orders()
        except:
            traceback.print_exc()

    @api.multi
    def sync_from_products_action(self):
        try:
            self.log("Inside sync_from_products_action for marketplace")
            self.log(self.enable_order_fetching)
            if self.enable_order_fetching and self.child_class_name and self.child_class_id:
                self.log("Function calling starts")
                self.log(self.child_class_name)
                self.log(self.child_class_id)
                self.log("Child class found")
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_from_products()
        except:
            traceback.print_exc()

    @api.multi
    def sync_to_products_action(self):
        try:
            self.log("Inside sync_to_products_action for marketplace")
            self.log(self.enable_order_fetching)
            if self.enable_order_fetching and self.child_class_name and self.child_class_id:
                self.log("Function calling starts")
                self.log(self.child_class_name)
                self.log(self.child_class_id)
                self.log("Child class found")
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_to_products()
        except:
            traceback.print_exc()

    @api.multi
    def sync_shipment_action(self):
        try:
            self.log("Inside sync_shipments_action for marketplace")
            self.log(self.enable_order_fetching)
            if self.enable_order_fetching and self.child_class_name and self.child_class_id:
                self.log("Function calling starts")
                self.log(self.child_class_name)
                self.log(self.child_class_id)
                self.log("Child class found")
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_shipments()
        except:
            traceback.print_exc()

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
