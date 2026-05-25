{
    'name': "Tutor Management",
    'version': '19.0.1.0.7',
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
        'base',
        'mail',
        'phone_validation',
    ],
    'data': [
        # security
        'security/tutor_groups.xml',
        'security/tutor_security.xml',
        'security/ir.model.access.csv',
        # sequence
        'data/sequence_data.xml',
        # data

        # view
        'views/lesson_views.xml',
        'views/tutor_views.xml',
        'views/student_views.xml',
        'views/spec_views.xml',
        # wizard
        'wizards/tutor_reassign_wizard_views.xml',
        # menu
        'views/tutor_menu.xml',
        # report
        'report/tutor_report_views.xml'
    ],
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}