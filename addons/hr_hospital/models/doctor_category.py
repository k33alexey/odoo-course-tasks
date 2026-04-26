from odoo import fields, models


class DoctorCategory(models.Model):
    _name = 'hr_hospital.doctor.category'
    _description = 'Doctor Category'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', required=True)
    doctor_ids = fields.One2many(
        'hr_hospital.doctor',
        'id',
        string='Doctors',
        readonly=True)

    _name_unique = models.Constraint(
        'unique(name)',
        'The name must be unique!')
