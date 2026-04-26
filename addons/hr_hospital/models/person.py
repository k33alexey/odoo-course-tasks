from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.tools import email_normalize_all
from odoo.exceptions import UserError
from odoo.addons.mail.tools import mail_validation
from odoo.addons.phone_validation.tools import phone_validation


class Person(models.AbstractModel):
    _name = 'hr_hospital.abstract.person'

    _rec_name = 'full_name'
    _description = 'Person'
    _inherit = [
        'image.mixin',
    ]

    last_name = fields.Char(string='Last Name', required=True)
    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name', required=False)
    phone = fields.Char()
    email = fields.Char()
    phone_state = fields.Selection([
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect')], string='Phone Quality', compute="_compute_phone_state", store=True)
    email_state = fields.Selection([
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect')], string='Email Quality', compute="_compute_email_state", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male')
    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=False)
    full_name = fields.Char(
        string='Full name',
        compute='_compute_full_name',
        store=True,
        index=True)
    country_id = fields.Many2one('res.country', string='Country')
    language_id = fields.Many2one('res.lang', string='Language')

    @api.depends('birth_date')
    def _compute_age(self):
        today_date = fields.Date.today()
        for person in self:
            person.age = relativedelta(today_date, person.birth_date).years if person.birth_date else 0

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_full_name(self):
        for person in self:
            person.full_name = ' '.join(filter(None, [person.last_name, person.first_name, person.middle_name]))

    @api.depends('phone', 'country_id.code')
    def _compute_phone_state(self):
        for person in self:
            phone_status = False
            if person.phone:
                country_code = person.country_id.code if person.country_id and person.country_id.code else None
                try:
                    if phone_validation.phone_parse(person.phone, country_code):
                        phone_status = 'correct'
                except UserError:
                    phone_status = 'incorrect'
            person.phone_state = phone_status

    @api.depends('email')
    def _compute_email_state(self):
        for person in self:
            email_state = False
            if person.email:
                email_state = 'incorrect'
                for email in email_normalize_all(person.email):
                    if mail_validation.mail_validate(email):
                        email_state = 'correct'
                        break
            person.email_state = email_state

    @api.onchange('phone', 'country_id')
    def _onchange_phone_validation(self):
        if self.phone:
            self.phone = self._phone_format(fname='phone', force_format='INTERNATIONAL') or self.phone
