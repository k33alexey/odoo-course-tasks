from odoo import api, fields, models


class DoctorHistory(models.Model):
    """
    Model for tracking the historical assignment of doctors to patients.
    Records when a doctor was assigned to a patient and when the
    assignment ended or shifted.
    """

    _name = 'hr_hospital.doctor.history'
    _description = 'Doctor History'

    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient', string='Patient', required=True)
    assigned_date = fields.Date(string='Assigned Date', required=True, default=fields.Datetime.now)
    shift_date = fields.Date(string='Shift Date')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('patient_id', 'doctor_id', 'doctor_id.category_id', 'assigned_date')
    def _compute_display_name(self):
        """
        Generates a descriptive name for the history record.
        Example: 'John Doe - Dr. Smith 13.05.2026'
        """

        for doctor_history in self:
            patient_name = doctor_history.patient_id.full_name or self.env._('Unknown Patient')
            doctor_name = doctor_history.doctor_id.full_name or self.env._('Unknown Doctor')
            category = doctor_history.doctor_id.category_id.name or self.env._('No Category')
            date_str = doctor_history.assigned_date.strftime('%d.%m.%Y') if doctor_history.assigned_date else ''

            doctor_history.display_name = f'{patient_name} - {doctor_name} ({category}) {date_str}'

    @api.onchange('assigned_date', 'shift_date')
    def _onchange_dates(self):
        """
        Validates that the shift date is not earlier than the assignment date.
        If invalid, resets the shift date and triggers a warning in the UI.
        :return: A warning dictionary for the web client if validation fails.
        """

        for doctor_history in self:
            if doctor_history.assigned_date and doctor_history.shift_date:
                if doctor_history.shift_date < doctor_history.assigned_date:
                    doctor_history.shift_date = False
                    return {
                        'warning': {
                            'title': self.env._('Invalid shift date'),
                            'message': self.env._('Shift date cannot be earlier than assigned date.'),
                        }
                    }
        return {}
