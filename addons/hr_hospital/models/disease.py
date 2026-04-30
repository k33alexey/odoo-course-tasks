import logging
import random

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'
    _parent_store = True

    name = fields.Char(string='Disease Name', required=True)
    code = fields.Char(string='ICD Code')
    color = fields.Integer(
        string='Color Index',
        default=lambda self: random.randint(1, 11))
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(
        'hr_hospital.disease',
        string='Parent Disease',
        ondelete='cascade',
        index=True)
    child_ids = fields.One2many(
        'hr_hospital.disease',
        'parent_id',
        string='Child Diseases')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if self._has_cycle():
            raise ValidationError(_('Error! You cannot create recursive hierarchy.'))

    @api.depends('name')
    def _compute_display_name(self):
        for disease in self:
            if disease.parent_id:
                disease.display_name = f"{disease.parent_id.display_name} / {disease.name}"
            else:
                disease.display_name = disease.name
