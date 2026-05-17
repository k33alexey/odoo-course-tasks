import logging
import secrets

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalDisease(models.Model):
    """
    Model for managing hospital disease classifications.
    Supports hierarchical structures (parent-child) and integrates
    with International Classification of Diseases (ICD) logic.
    """

    _name = 'hr_hospital.disease'
    _description = 'Disease'
    _parent_store = True

    name = fields.Char(string='Disease Name', required=True, translate=True)
    code = fields.Char(string='ICD Code')
    color = fields.Integer(
        string='Color Index',
        default=lambda self: secrets.randbelow(11) + 1,
    )
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(
        comodel_name='hr_hospital.disease', string='Parent Disease', ondelete='cascade', index=True
    )
    child_ids = fields.One2many(comodel_name='hr_hospital.disease', inverse_name='parent_id', string='Child Diseases')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        """
        Ensures the hierarchy remains a tree structure by preventing
        recursive loops where a disease becomes its own ancestor.
        :raises ValidationError: If a cycle is detected in the hierarchy.
        """

        if self._has_cycle():
            raise ValidationError(self.env._('Error! You cannot create recursive hierarchy.'))

    @api.depends('name', 'parent_id')
    def _compute_display_name(self):
        """
        Generates a breadcrumb-style display name for hierarchical diseases.
        Example: 'Infections / Bacterial Infections / Tuberculosis'
        """

        for disease in self:
            if disease.parent_id:
                disease.display_name = f'{disease.parent_id.display_name} / {disease.name}'
            else:
                disease.display_name = disease.name
