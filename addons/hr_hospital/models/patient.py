import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    """
    Model for managing patient profiles and their medical relationships.
    Integrates with Odoo's mail thread for communication history and
    automatically maintains a log of personal doctor assignments.
    """

    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['hr_hospital.medic.info', 'mail.thread', 'mail.activity.mixin']

    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Personal doctor', tracking=True)
    policy_number = fields.Char(string='Policy Number', size=20, help='Policy number of the patient')
    visit_ids = fields.One2many(
        comodel_name='hr_hospital.visit',
        inverse_name='patient_id',
        string='Visit History',
    )
    personal_doctor_ids = fields.One2many(
        comodel_name='hr_hospital.doctor.history',
        inverse_name='patient_id',
        string='Personal Doctor History',
        readonly=True,
        context={'active_test': False},  # ПАМЯТКА: для xml, чтоб видеть архив.записи
    )

    def write(self, vals):
        """
        Overrides the standard write method to automatically update
        the doctor assignment history. When 'doctor_id' changes, it
        archives the old assignment and creates a new history record.
        :param vals: dictionary of fields to update.
        :return: bool result of the write operation.
        """

        if 'doctor_id' not in vals:
            return super().write(vals)

        doctor_id = vals.get('doctor_id')
        patients_to_update = self.filtered(lambda val: 'doctor_id' in vals and val.doctor_id.id != doctor_id)

        result = super().write(vals)

        if patients_to_update:
            assigned_date = self.env.context.get('assigned_date') or fields.Date.today()

            patients_to_update.mapped('personal_doctor_ids').filtered('active').write({'active': False})

            if doctor_id:
                history_vals = [
                    {
                        'patient_id': patient.id,
                        'doctor_id': doctor_id,
                        'assigned_date': assigned_date,
                        'active': True,
                    }
                    for patient in patients_to_update
                ]

                if history_vals:
                    self.env['hr_hospital.doctor.history'].create(history_vals)

        return result

    def action_view_hospital_visits(self):
        """
        Action to display a list of all visits associated with this patient.
        Provides a filtered view of the 'hr_hospital.visit' model.
        :return: dict representing the ir.actions.act_window.
        """

        self.ensure_one()

        return {
            'name': self.env._(source='Visits of %(name)s', name=self.full_name),
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {
                'default_patient_id': self.id,
            },
            'target': 'current',
        }
