from odoo import models, fields, api
from datetime import datetime, timedelta

class PCBuilderDashboard(models.Model):
    _name = 'pc.builder.dashboard'
    _description = 'PC Builder Dashboard'

    @api.model
    def get_dashboard_data(self):
        """Fetch all dashboard data for the backpanel"""
        return {
            'total_builds': self._get_total_builds(),
            'builds_today': self._get_builds_today(),
            'total_revenue': self._get_total_revenue(),
            'popular_components': self._get_popular_components(),
            'compatibility_issues': self._get_compatibility_issues(),
            'recent_builds': self._get_recent_builds(),
            'component_stock_status': self._get_component_stock_status(),
        }

    @api.model
    def _get_total_builds(self):
        return self.env['pc.build'].search_count([])

    @api.model
    def _get_builds_today(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.env['pc.build'].search_count([
            ('create_date', '>=', today)
        ])

    @api.model
    def _get_total_revenue(self):
        builds = self.env['pc.build'].search([])
        return sum(build.total_price for build in builds)

    @api.model
    def _get_popular_components(self):
        """Get the most frequently selected components"""
        components = {}
        builds = self.env['pc.build'].search([])
        
        for build in builds:
            for component_type in ['motherboard', 'cpu', 'ram', 'gpu', 'case', 'psu']:
                field_name = f'{component_type}_id'
                component = getattr(build, field_name)
                if component:
                    key = f"{component_type}:{component.id}"
                    components[key] = components.get(key, 0) + 1
        
        # Sort by frequency
        sorted_components = sorted(components.items(), key=lambda x: x[1], reverse=True)[:10]
        return [{'name': k, 'count': v} for k, v in sorted_components]

    @api.model
    def _get_compatibility_issues(self):
        """Check for potential compatibility issues in builds"""
        issues = []
        builds = self.env['pc.build'].search([])
        
        for build in builds:
            if build.motherboard_id and build.cpu_id:
                if build.motherboard_id.socket_type != build.cpu_id.socket_type:
                    issues.append({
                        'build_id': build.id,
                        'issue': f"Socket mismatch: {build.motherboard_id.name} vs {build.cpu_id.name}"
                    })
            
            if build.motherboard_id and build.ram_id:
                if build.motherboard_id.ram_type != build.ram_id.ram_type:
                    issues.append({
                        'build_id': build.id,
                        'issue': f"RAM type mismatch: {build.motherboard_id.name} vs {build.ram_id.name}"
                    })
        
        return issues

    @api.model
    def _get_recent_builds(self, limit=10):
        """Get the most recent PC builds"""
        builds = self.env['pc.build'].search([], order='create_date desc', limit=limit)
        return [{
            'id': b.id,
            'name': b.name,
            'user': b.user_id.name,
            'total_price': b.total_price,
            'create_date': b.create_date,
        } for b in builds]

    @api.model
    def _get_component_stock_status(self):
        """Get stock status of all PC components"""
        components = self.env['product.template'].search([
            ('is_pc_component', '=', True)
        ])
        
        stock_status = []
        for comp in components:
            qty_available = sum(variant.qty_available for variant in comp.product_variant_ids)
            stock_status.append({
                'component': comp.name,
                'type': comp.component_type,
                'qty_available': qty_available,
                'status': 'In Stock' if qty_available > 0 else 'Out of Stock',
            })
        
        return stock_status
