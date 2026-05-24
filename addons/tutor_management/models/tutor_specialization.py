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
    price = fields.Monetary(string='Price', default=500, required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency', default=lambda self: self.env.company.currency_id
    )

    _name_unique = models.Constraint(definition='unique(name)', message='The name must be unique!')
