{
    'name': "Hospital Management",
    'version': '19.0.1.2.1',
    'category': 'Healthcare',
    'summary': "Manage doctors, patients, diseases and hospital visits",
    'description': "",
    'author': "Oleksii Kalinin",
    'website': "https://github.com/k33alexey/odoo-school",
    'license': "OPL-1",
    'depends': [
        'base',
        'mail',
        'phone_validation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/disease_data.xml',
        'data/doctor_category_data.xml',
        'views/hr_hospital_menu.xml',
        'views/doctor_views.xml',
        'views/doctor_category_views.xml',
        'views/doctor_history_views.xml',
        'views/disease_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml'
    ],
    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/visit_demo.xml',
        'demo/doctor_history_demo.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}