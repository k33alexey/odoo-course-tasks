{
    'name': "Tutor Management",
    'version': '19.0.1.0.1',
    'summary': 'Manage tutors, students, specializations, and lessons',
    'category': 'Education',
    'description':
        """
        ======================================================================================
        This module provides a comprehensive system for managing tutoring operations,
        focusing on tutor-student interactions, lesson tracking, and subject specializations.
        ======================================================================================
        """,
    'author': "Oleksii Kalinin",
    'website': "https://github.com/k33alexey/odoo-school",
    'license': "OPL-1",
    'depends': [
        'mail',
        'phone_validation',
    ],
    'data': [
        'security/tutor_groups.xml',
        'security/tutor_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}