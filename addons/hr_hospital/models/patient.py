import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Full Name', required=True)
    birth_date = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male')
    visit_ids = fields.One2many(
        'hr_hospital.visit',
        'patient_id',
        string='Visit History',
        readonly=True)
