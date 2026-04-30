from odoo import models, fields


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr_hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor'

    doctor_id = fields.Many2one('hr_hospital.doctor', string='New Doctor', required=True)
    reassign_date = fields.Date(string='Shift date', default=fields.Date.today)

    def action_reassign(self):
        patient_ids = self.env.context.get('active_ids')
        if not patient_ids:
            return {'type': 'ir.actions.act_window_close'}

        patients = self.env['hr_hospital.patient'].browse(patient_ids)
        ctx = dict(self.env.context, reassign_date=self.reassign_date)

        for patient in self:
            patients.with_context(ctx).write({
                'doctor_id': patient.doctor_id.id,
            })

        return {'type': 'ir.actions.act_window_close'}
