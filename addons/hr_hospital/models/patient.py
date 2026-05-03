import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['hr_hospital.medic.info', 'mail.thread', 'mail.activity.mixin']

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
        context={'active_test': False}) # ПАМЯТКА: для xml, чтоб видеть архив.записи

    def write(self, vals):
        patients_to_update = self.filtered(
            lambda val: 'doctor_id' in vals and val.doctor_id.id != vals.get('doctor_id')
        )

        result = super().write(vals)

        if patients_to_update:
            doctor_id = vals.get('doctor_id')
            assigned_date = self.env.context.get('assigned_date') or fields.Date.today()

            self.mapped('personal_doctor_ids').filtered(lambda val: val.active).write({'active': False})

            if doctor_id:
                history_vals = []
                for patient in self:
                    history_vals.append({
                        'patient_id': patient.id,
                        'doctor_id': doctor_id,
                        'assigned_date': assigned_date,
                        'active': True,
                    })

                if history_vals:
                    self.env['hr_hospital.doctor.history'].create(history_vals)

        return result
