import secrets

from odoo import fields, models


class DoctorCategory(models.Model):
    """
    Model for managing medical specialties and professional categories.
    Used to classify doctors and apply specific business logic based on
    their professional level (e.g., distinguishing mentors from interns).
    """

    _name = 'hr_hospital.doctor.category'
    _description = 'Doctor Category'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10, required=True)
    doctor_ids = fields.One2many(comodel_name='hr_hospital.doctor', inverse_name='id', string='Doctors', readonly=True)
    color = fields.Integer(
        string='Color Index',
        default=lambda self: secrets.randbelow(11) + 1,
    )

    _name_unique = models.Constraint(definition='unique(name)', message='The name must be unique!')
