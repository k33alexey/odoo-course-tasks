{
    'name': "Hospital Management",
    'version': '1.0',
    'category': 'Healthcare',
    'summary': "Manage doctors, patients, diseases and hospital visits",
    'description': "",
    'author': "Oleksii Kalinin",
    'website': "https://github.com/k33alexey/odoo-school",
    'license': "OPL-1",
    'depends': ['base'],
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}