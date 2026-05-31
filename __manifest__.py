{
    'name': 'Marlef x PC Builder',
    'version': '1.0',
    'category': 'Website/Website',
    'summary': 'Powerful PC Configurator with AI 3D visualization and backpanel control.',
    'description': """
        Marlef x PC Builder Odoo Module
        ===============================
        A comprehensive PC building solution for Odoo eCommerce.
        Features:
        - Step-by-step PC part selection.
        - Compatibility engine (Socket, RAM type, etc.).
        - AI-powered 3D visualization (PNG to 3D).
        - Stock synchronization with venus.tech.
        - Powerful backpanel for management.
    """,
    'author': 'Marlef Plaza',
    'website': 'https://marlef.com',
    'depends': ['website', 'website_sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/pc_builder_templates.xml',
        'views/pc_builder_views.xml',
        'views/pc_builder_menus.xml',
        'data/pc_builder_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'marlef_pc_builder/static/src/scss/pc_builder.scss',
            'marlef_pc_builder/static/src/js/pc_builder.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
