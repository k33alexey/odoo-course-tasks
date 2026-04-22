{
    'name': "Hospital Management",
    'version': '19.0.1.0.3',
    'category': 'Healthcare',
    'summary': "Manage doctors, patients, diseases and hospital visits",
    'description': "",
    'author': "Oleksii Kalinin",
    'website': "https://github.com/k33alexey/odoo-school",
    'license': "OPL-1",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/disease.xml',
        'views/hr_hospital_menu.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml'
    ],
    'demo': [
        'demo/doctor.xml',
        'demo/patient.xml',
        'demo/visit.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}