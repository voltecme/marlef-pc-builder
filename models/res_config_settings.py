from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    venus_tech_api_key = fields.Char(string="Venus.tech API Key", config_parameter='marlef_pc_builder.venus_tech_api_key')
    venus_tech_api_url = fields.Char(string="Venus.tech API URL", config_parameter='marlef_pc_builder.venus_tech_api_url', default="https://api.venus.tech/v1")
    
    ai_3d_generator_api_key = fields.Char(string="AI 3D Generator API Key", config_parameter='marlef_pc_builder.ai_3d_generator_api_key')
    
    enable_whatsapp_auth = fields.Boolean(string="Enable WhatsApp Auth", config_parameter='marlef_pc_builder.enable_whatsapp_auth')
    whatsapp_api_key = fields.Char(string="WhatsApp API Key", config_parameter='marlef_pc_builder.whatsapp_api_key')
