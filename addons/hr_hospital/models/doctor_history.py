from odoo import fields, models, api, _


class DoctorHistory(models.Model):
    _name = 'hr_hospital.doctor.history'
    _description = 'Doctor History'

    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    assigned_date = fields.Date(string='Assigned Date', required=True, default=fields.Datetime.now)
    shift_date = fields.Date(string='Shift Date')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('doctor_id', 'assigned_date')
    def _compute_display_name(self):
        for doctor_history in self:
            if doctor_history.doctor_id and doctor_history.assigned_date:
                doctor_history.display_name = f"{doctor_history.doctor_id.full_name} from {doctor_history.assigned_date}"

    @api.onchange('assigned_date', 'shift_date')
    def _onchange_dates(self):
        for doctor_history in self:
            if doctor_history.assigned_date and doctor_history.shift_date:
                if doctor_history.shift_date < doctor_history.assigned_date:
                    doctor_history.shift_date = False
                    return {
                        'warning': {
                            'title': _("Invalid shift date"),
                            'message': _("Shift date cannot be earlier than assigned date."),
                        }
                    }
