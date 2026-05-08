from odoo import models, fields, api, Command


class VisitReportWizard(models.TransientModel):
    _name = 'hr_hospital.visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(comodel_name='hr_hospital.doctor', string='Doctors')
    patient_ids = fields.Many2many(comodel_name='hr_hospital.patient', string='Patients')
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')
    only_done = fields.Boolean(string='Only Visit Done')
    disease_ids = fields.Many2many(comodel_name='hr_hospital.disease', string='Disease')

    @api.model
    def default_get(self, fields_list):
        result: dict = super().default_get(fields_list)

        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_ids and active_model:
            ids: list = active_ids if isinstance(active_ids, list) else [active_ids]

            if active_model == 'hr_hospital.doctor':
                result['doctor_ids'] = [Command.set(ids)]
            elif active_model == 'hr_hospital.patient':
                result['patient_ids'] = [Command.set(ids)]

        return result

    def action_generate_report(self):
        self.ensure_one()

        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))

        if self.date_from:
            domain.append(('visit_date', '>=', self.date_from))

        if self.date_to:
            domain.append(('visit_date', '<=', self.date_to))

        if self.only_done:
            domain.append(('state', '=', 'done'))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        return {
            'name': 'Visit Report',
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.visit',
            'view_mode': 'list',
            'domain': domain,
            'context': {'search_default_group_by_disease': 1},
        }
