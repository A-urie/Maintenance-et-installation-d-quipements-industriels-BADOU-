from odoo import api, fields, models


class CdtInterventionPiece(models.Model):
    _name = "cdt.intervention.piece"
    _description = "Pièce utilisée dans une intervention"

    intervention_id = fields.Many2one("cdt.intervention", string="Intervention", required=True, ondelete="cascade")
    piece_id = fields.Many2one("cdt.piece", string="Pièce", required=True)
    quantite = fields.Float(string="Quantité", default=1.0)
    cout_unitaire = fields.Float(string="Coût unitaire", compute="_compute_cout", store=True, readonly=False)

    @api.depends("piece_id")
    def _compute_cout(self):
        for rec in self:
            rec.cout_unitaire = rec.piece_id.cout_unitaire