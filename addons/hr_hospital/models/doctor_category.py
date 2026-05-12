import secrets

from odoo import fields, models


class DoctorCategory(models.Model):
    _name = 'hr_hospital.doctor.category'
    _description = 'Doctor Category'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', required=True)
    doctor_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='id',
        string='Doctors',
        readonly=True)
    color = fields.Integer(
        string='Color Index',
        default=lambda self: secrets.randbelow(11) + 1,
    )

    _name_unique = models.Constraint(
        definition='unique(name)',
        message='The name must be unique!')
