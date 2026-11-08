from odoo import api, fields, models


class CdtPiece(models.Model):
    _name = "cdt.piece"
    _description = "Pièce de rechange"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Désignation", required=True, tracking=True)
    reference = fields.Char(string="Référence", required=True, copy=False)
    origine = fields.Selection(
        [
            ("stock", "Stock"),
            ("immobilisation", "Machine d'immobilisation"),
            ("fabrication", "Fabrication locale"),
            ("importation", "Importation"),
        ],
        string="Origine",
        default="stock",
        required=True,
    )
    quantite_stock = fields.Float(string="Quantité en stock", tracking=True)
    seuil_alerte = fields.Float(string="Seuil d'alerte", default=2.0)
    cout_unitaire = fields.Float(string="Coût unitaire")
    en_alerte = fields.Boolean(string="Sous le seuil", compute="_compute_en_alerte", store=True)

    _sql_constraints = [
        ("reference_unique", "unique(reference)", "Cette référence de pièce existe déjà."),
    ]

    @api.depends("quantite_stock", "seuil_alerte")
    def _compute_en_alerte(self):
        for rec in self:
            rec.en_alerte = rec.quantite_stock <= rec.seuil_alerte