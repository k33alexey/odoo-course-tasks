import logging

from odoo import models, fields

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
    personal_doctor_ids = fields.One2many(
        'hr_hospital.doctor.history',
        'patient_id',
        string='Personal Doctor History',
        readonly=True,
        context={'active_test': False})

    def write(self, vals):
        if vals.get('doctor_id'):
            assigned_date = self.env.context.get('assigned_date') or fields.Date.today()

            for patient in self:
                active_personal_doctor_ids = patient.personal_doctor_ids.filtered(lambda x: x.active)

                if active_personal_doctor_ids:
                    active_personal_doctor_ids.write({'active': False})

                self.env['hr_hospital.doctor.history'].create({
                    'patient_id': patient.id,
                    'doctor_id': vals.get('doctor_id'),
                    'assigned_date': assigned_date,
                    'shift_date': assigned_date,
                    'active': True,
                })

        return super(HospitalPatient, self).write(vals)
