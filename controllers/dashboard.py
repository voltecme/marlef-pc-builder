from odoo import http
from odoo.http import request

class PCBuilderDashboardController(http.Controller):

    @http.route(['/pc-builder/dashboard'], type='http', auth="user", website=True)
    def dashboard(self, **post):
        """Main backpanel dashboard"""
        dashboard_model = request.env['pc.builder.dashboard'].sudo()
        dashboard_data = dashboard_model.get_dashboard_data()
        
        values = {
            'dashboard_data': dashboard_data,
        }
        return request.render('marlef_pc_builder.dashboard_page', values)

    @http.route(['/pc-builder/api/dashboard_data'], type='json', auth="user", website=True)
    def get_dashboard_data_api(self):
        """API endpoint for real-time dashboard data"""
        dashboard_model = request.env['pc.builder.dashboard'].sudo()
        return dashboard_model.get_dashboard_data()

    @http.route(['/pc-builder/api/component_compatibility'], type='json', auth="user", website=True)
    def check_compatibility(self, motherboard_id, cpu_id=None, ram_id=None):
        """Check component compatibility"""
        compatibility_issues = []
        
        motherboard = request.env['product.template'].sudo().browse(int(motherboard_id))
        
        if cpu_id:
            cpu = request.env['product.template'].sudo().browse(int(cpu_id))
            if motherboard.socket_type and cpu.socket_type:
                if motherboard.socket_type != cpu.socket_type:
                    compatibility_issues.append({
                        'type': 'socket_mismatch',
                        'message': f"CPU socket {cpu.socket_type} does not match motherboard socket {motherboard.socket_type}"
                    })
        
        if ram_id:
            ram = request.env['product.template'].sudo().browse(int(ram_id))
            if motherboard.ram_type and ram.ram_type:
                if motherboard.ram_type != ram.ram_type:
                    compatibility_issues.append({
                        'type': 'ram_type_mismatch',
                        'message': f"RAM type {ram.ram_type} does not match motherboard type {motherboard.ram_type}"
                    })
        
        return {
            'is_compatible': len(compatibility_issues) == 0,
            'issues': compatibility_issues,
        }

    @http.route(['/pc-builder/api/builds'], type='json', auth="user", website=True)
    def get_builds(self, limit=20, offset=0):
        """Get paginated list of PC builds"""
        builds = request.env['pc.build'].sudo().search([], order='create_date desc', limit=limit, offset=offset)
        return [{
            'id': b.id,
            'name': b.name,
            'user': b.user_id.name,
            'total_price': b.total_price,
            'create_date': b.create_date.strftime('%Y-%m-%d %H:%M:%S'),
        } for b in builds]

    @http.route(['/pc-builder/api/build/<int:build_id>'], type='json', auth="user", website=True)
    def get_build_details(self, build_id):
        """Get detailed information about a specific build"""
        build = request.env['pc.build'].sudo().browse(build_id)
        if not build.exists():
            return {'error': 'Build not found'}
        
        return {
            'id': build.id,
            'name': build.name,
            'user': build.user_id.name,
            'total_price': build.total_price,
            'components': {
                'motherboard': build.motherboard_id.name if build.motherboard_id else None,
                'cpu': build.cpu_id.name if build.cpu_id else None,
                'ram': build.ram_id.name if build.ram_id else None,
                'storage': build.storage_id.name if build.storage_id else None,
                'gpu': build.gpu_id.name if build.gpu_id else None,
                'case': build.case_id.name if build.case_id else None,
                'psu': build.psu_id.name if build.psu_id else None,
                'cooler': build.cooler_id.name if build.cooler_id else None,
                'fan': build.fan_id.name if build.fan_id else None,
                'controller': build.controller_id.name if build.controller_id else None,
                'cable': build.cable_id.name if build.cable_id else None,
                'assembly': build.assembly_id.name if build.assembly_id else None,
            },
            'create_date': build.create_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
