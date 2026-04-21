import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(string='Specialization')

    @api.depends('name', 'specialty')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.specialty})" if rec.specialty else rec.name
