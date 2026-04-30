import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True)
    birth_date = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Personal doctor', tracking=True)
    policy_number = fields.Char(string='Policy Number', size=20)
    visit_ids = fields.One2many(
        'hr_hospital.visit',
        'patient_id',
        string='Visit History',
        readonly=True)