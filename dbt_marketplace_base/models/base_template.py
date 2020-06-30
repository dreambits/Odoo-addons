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

    latest_order_count = fields.Integer("New Order Count", compute="get_latest_order_count")

    enable_order_fetching = fields.Boolean('Enable Order Fetching')
    enable_product_to_sync = fields.Boolean('Enable Product To Sync')
    enable_product_from_sync = fields.Boolean('Enable Product From Sync')
    enable_shipment_sync = fields.Boolean('Enable Shipment Sync')

    child_class_name = fields.Char('Name of child class')
    child_class_id = fields.Integer('Id of child class record')

    color = fields.Integer(string='Color Index',
                           help="The color of the channel")

    def log(self, msg):
        """
        @brief      To log when _debug is set to true.

        @param      self  The object
        @param      msg   The message

        """
        if self._debug:
            _logger.info(msg)

    @api.depends('child_class_id','child_class_name')
    def get_latest_order_count(self):
        """
        To get latest order count.
        It will set the latest order count from child class object.
        """
        self.log("Inside get_latest_order_count for marketplace")
        try:
            for rec in self:
                if rec.child_class_name and rec.child_class_id:
                    rec.latest_order_count = rec.env[rec.child_class_name].browse(
                            rec.child_class_id
                        ).get_latest_order_count()
        except:
            traceback.print_exc()

    def fetch_order_action(self):
        """
        This function will help to fetch order from child class.
        """
        try:
            self.log("Inside fetch_orders for marketplace")
            if self.enable_order_fetching and self.child_class_name and self.child_class_id:
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().fetch_orders()
                self.get_latest_order_count()
                if hasattr(self.env.user,"notify_info") and self.env.user.notify_info:
                    self.env.user.notify_info("Sync started for orders from bol to odoo")
        except:
            traceback.print_exc()

    def sync_from_products_action(self):
        """
        This function will help to fetch products from Marketplace from child class.
        """
        try:
            self.log("Inside sync_from_products_action for marketplace")
            if self.enable_product_from_sync and self.child_class_name and self.child_class_id:
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_from_products()
                if hasattr(self.env.user,"notify_info") and self.env.user.notify_info:
                    self.env.user.notify_info("Sync started for products from bol to odoo")
        except:
            traceback.print_exc()

    def sync_to_products_action(self):
        """
        This function will help to fetch products to Marketplace from child class.
        """
        try:
            self.log("Inside sync_to_products_action for marketplace")
            if self.enable_product_to_sync and self.child_class_name and self.child_class_id:
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_to_products()
                if hasattr(self.env.user,"notify_info") and self.env.user.notify_info:
                    self.env.user.notify_info("Sync started for products from odoo to bol")
        except:
            traceback.print_exc()

    def sync_shipment_action(self):
        """
        This function will help to sync shipment from child class.
        """
        try:
            self.log("Inside sync_shipments_action for marketplace")
            if self.enable_shipment_sync  and self.child_class_name and self.child_class_id:
                self.env[self.child_class_name].browse(
                    self.child_class_id).with_delay().sync_shipments()
                if hasattr(self.env.user,"notify_info") and self.env.user.notify_info:
                    self.env.user.notify_info("Sync started for shipment from bol to odoo")
        except:
            traceback.print_exc()

    @job
    def fetch_orders(self):
        """
        This function must be overridden in child class to sync.
        """
        raise NotImplementedError('Must be overridden in child class')

    @job
    def sync_to_produts(self):
        """
        This function must be overridden in child class to update products to Marketplace.
        """
        raise NotImplementedError('Must be overridden in child class')

    @job
    def sync_from_products(self):
        """
        This function must be overridden in child class to fetch products from Marketplace.
        """
        raise NotImplementedError('Must be overridden in child class')

    @job
    def sync_shipments(self):
        """
        This function must be overridden in child class to sync shipments from Marketplace.
        """
        raise NotImplementedError('Must be overridden in child class')

    def view_all_orders(self):
        """
        @brief      The functions needed to open appropriate window for view actions of dashboard

        @param      self  The object

        @return     related action for all orders
        """
        self.log("Inside view all orders: marketplace")
        # raise NotImplementedError('Must be overridden in child class')
        if self.child_class_name and self.child_class_id:
            return self.env[self.child_class_name].browse(
                self.child_class_id).view_all_orders()

    def view_pending_orders(self):
        """
        @brief      The functions needed to open appropriate window for view actions of dashboard

        @param      self  The object

        @return     related action for pending orders
        """
        # raise NotImplementedError('Must be overridden in child class')
        if self.child_class_name and self.child_class_id:
            return self.env[self.child_class_name].browse(
                self.child_class_id).view_pending_orders()

    def view_shipment(self):
        """
        @brief      The functions needed to open appropriate window for view actions of dashboard

        @param      self  The object

        @return     related action for shipments
        """
        # raise NotImplementedError('Must be overridden in child class')
        self.log("Inside view shipment: marketplace")
        if self.child_class_name and self.child_class_id:
            return self.env[self.child_class_name].browse(
                self.child_class_id).view_shipment()

    def view_latest_orders(self):
        """
        @brief      The functions needed to open appropriate window for view actions of dashboard

        @param      self  The object

        @return     related action for latest orders
        """
        self.log("Inside view latest orders: marketplace")
        if self.child_class_name and self.child_class_id:
            return self.env[self.child_class_name].browse(
                self.child_class_id).view_latest_orders()
