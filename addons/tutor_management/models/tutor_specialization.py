import secrets

from odoo import fields, models


class TutorSpecialization(models.Model):
    _name = 'tutor.specialization'
    _description = 'Tutor Specialization'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10, required=True)
    tutor_ids = fields.One2many(comodel_name='tutor.tutor', inverse_name='id', string='Tutors', readonly=True)
    color = fields.Integer(
        string='Color Index',
        default=lambda self: secrets.randbelow(11) + 1,
    )

    _name_unique = models.Constraint(definition='unique(name)', message='The name must be unique!')
