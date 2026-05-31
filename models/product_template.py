from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_pc_component = fields.Boolean(string="Is PC Component", default=False)
    component_type = fields.Selection([
        ('motherboard', 'Motherboard'),
        ('cpu', 'CPU'),
        ('ram', 'RAM'),
        ('storage', 'Storage'),
        ('gpu', 'GPU'),
        ('case', 'Case'),
        ('psu', 'PSU'),
        ('cooler', 'CPU Cooler'),
        ('fan', 'Case Fan'),
        ('controller', 'Fan Controller'),
        ('cable', 'Extra Cable'),
        ('assembly', 'Assembly Service')
    ], string="Component Type")

    # Compatibility Fields
    socket_type = fields.Char(string="Socket Type")  # For CPU/Motherboard
    ram_type = fields.Selection([
        ('ddr3', 'DDR3'),
        ('ddr4', 'DDR4'),
        ('ddr5', 'DDR5')
    ], string="RAM Type")  # For RAM/Motherboard
    
    # 3D Model data
    three_d_model_url = fields.Char(string="3D Model URL")
    png_no_background = fields.Binary(string="PNG (No Background)")
