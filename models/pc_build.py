from odoo import models, fields, api

class PCBuild(models.Model):
    _name = 'pc.build'
    _description = 'PC Configuration'

    name = fields.Char(string="Build Name", required=True, default="New PC Build")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    session_id = fields.Char(string="Session ID")
    
    # Component selections
    motherboard_id = fields.Many2one('product.product', string="Motherboard", domain=[('component_type', '=', 'motherboard')])
    cpu_id = fields.Many2one('product.product', string="CPU", domain=[('component_type', '=', 'cpu')])
    ram_id = fields.Many2one('product.product', string="RAM", domain=[('component_type', '=', 'ram')])
    storage_id = fields.Many2one('product.product', string="Storage", domain=[('component_type', '=', 'storage')])
    gpu_id = fields.Many2one('product.product', string="GPU", domain=[('component_type', '=', 'gpu')])
    case_id = fields.Many2one('product.product', string="Case", domain=[('component_type', '=', 'case')])
    psu_id = fields.Many2one('product.product', string="PSU", domain=[('component_type', '=', 'psu')])
    cooler_id = fields.Many2one('product.product', string="CPU Cooler", domain=[('component_type', '=', 'cooler')])
    fan_id = fields.Many2one('product.product', string="Case Fan", domain=[('component_type', '=', 'fan')])
    controller_id = fields.Many2one('product.product', string="Fan Controller", domain=[('component_type', '=', 'controller')])
    cable_id = fields.Many2one('product.product', string="Extra Cable", domain=[('component_type', '=', 'cable')])
    assembly_id = fields.Many2one('product.product', string="Assembly Service", domain=[('component_type', '=', 'assembly')])

    total_price = fields.Float(string="Total Price", compute="_compute_total_price")

    @api.depends('motherboard_id', 'cpu_id', 'ram_id', 'storage_id', 'gpu_id', 'case_id', 'psu_id', 'cooler_id', 'fan_id', 'controller_id', 'cable_id', 'assembly_id')
    def _compute_total_price(self):
        for build in self:
            price = 0.0
            components = [
                build.motherboard_id, build.cpu_id, build.ram_id, build.storage_id,
                build.gpu_id, build.case_id, build.psu_id, build.cooler_id,
                build.fan_id, build.controller_id, build.cable_id, build.assembly_id
            ]
            for comp in components:
                if comp:
                    price += comp.lst_price
            build.total_price = price
