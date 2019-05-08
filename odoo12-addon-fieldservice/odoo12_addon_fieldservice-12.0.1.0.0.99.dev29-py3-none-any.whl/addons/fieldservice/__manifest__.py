# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Field Service',
    'summary': 'Manage Field Service Locations, Workers and Orders',
    'version': '12.0.1.0.0',
    'category': 'Field Service',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/field-service',
    'depends': [
        'base_geolocalize',
        'mail',
        'web_timeline',
        'resource',
        'contacts',
    ],
    'data': [
        'data/ir_sequence.xml',
        'data/mail_message_subtype.xml',
        'data/module_category.xml',
        'data/fsm_stage.xml',
        'data/fsm_team.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'report/fsm_order_report_template.xml',
        'views/res_config_settings.xml',
        'views/fsm_territory.xml',
        'views/fsm_branch.xml',
        'views/fsm_district.xml',
        'views/fsm_region.xml',
        'views/fsm_stage.xml',
        'views/fsm_tag.xml',
        'views/res_partner.xml',
        'views/fsm_location.xml',
        'views/fsm_person.xml',
        'views/fsm_order.xml',
        'views/fsm_route.xml',
        'views/fsm_schedule.xml',
        'views/fsm_category.xml',
        'views/fsm_equipment.xml',
        'views/fsm_template.xml',
        'views/fsm_team.xml',
        'views/menu.xml',
        'wizard/fsm_wizard.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'application': True,
    'license': 'AGPL-3',
    'development_status': 'Beta',
    'maintainers': [
        'wolfhall',
        'max3903',
    ],
}
