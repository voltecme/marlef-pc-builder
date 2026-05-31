from odoo import http
from odoo.http import request

class PCBuilderController(http.Controller):

    @http.route(['/pc-builder'], type='http', auth="public", website=True)
    def pc_builder_index(self, **post):
        # Fetch initial components (Motherboards as the anchor)
        motherboards = request.env['product.template'].sudo().search([
            ('is_pc_component', '=', True),
            ('component_type', '=', 'motherboard'),
            ('website_published', '=', True)
        ])
        values = {
            'motherboards': motherboards,
        }
        return request.render('marlef_pc_builder.pc_builder_page', values)

    @http.route(['/pc-builder/get_components'], type='json', auth="public", website=True)
    def get_components(self, component_type, filters=None):
        domain = [
            ('is_pc_component', '=', True),
            ('component_type', '=', component_type),
            ('website_published', '=', True)
        ]
        if filters:
            if 'socket_type' in filters and filters['socket_type']:
                domain.append(('socket_type', '=', filters['socket_type']))
            if 'ram_type' in filters and filters['ram_type']:
                domain.append(('ram_type', '=', filters['ram_type']))
        
        products = request.env['product.template'].sudo().search(domain)
        return [{
            'id': p.id,
            'name': p.name,
            'price': p.list_price,
            'image_url': f"/web/image/product.template/{p.id}/image_1024",
            'socket_type': p.socket_type,
            'ram_type': p.ram_type,
        } for p in products]

    @http.route(['/pc-builder/add_to_cart'], type='json', auth="public", website=True)
    def add_to_cart(self, product_ids):
        sale_order = request.website.sale_get_order(force_create=True)
        for product_id in product_ids:
            if product_id:
                sale_order._cart_update(product_id=int(product_id), add_qty=1)
        return True
