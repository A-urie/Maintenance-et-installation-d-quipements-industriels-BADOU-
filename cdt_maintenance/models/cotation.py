from odoo import api, fields, models
from odoo.exceptions import UserError


class CdtCotation(models.Model):
    _name = "cdt.cotation"
    _description = "Demande de cotation"
    _inherit = ["mail.thread"]
    _order = "date desc, id desc"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default="Nouveau")
    piece_id = fields.Many2one("cdt.piece", string="Pièce", required=True, tracking=True)
    quantite = fields.Float(string="Quantité", default=1.0, required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    ligne_ids = fields.One2many("cdt.cotation.ligne", "cotation_id", string="Offres")
    fournisseur_retenu_id = fields.Many2one(
        "res.partner", string="Fournisseur retenu", compute="_compute_retenu", store=True
    )
    montant_retenu = fields.Float(string="Montant retenu", compute="_compute_retenu", store=True)
    statut = fields.Selection(
        [
            ("brouillon", "En comparaison"),
            ("validee", "Validée"),
            ("recue", "Reçue"),
            ("annulee", "Annulée"),
        ],
        string="Statut",
        default="brouillon",
        required=True,
        tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = self.env["ir.sequence"].next_by_code("cdt.cotation") or "Nouveau"
        return super().create(vals_list)

    @api.depends("ligne_ids.retenue", "ligne_ids.total")
    def _compute_retenu(self):
        for rec in self:
            retenue = rec.ligne_ids.filtered("retenue")[:1]
            rec.fournisseur_retenu_id = retenue.fournisseur_id
            rec.montant_retenu = retenue.total if retenue else 0.0

    def action_retenir_moins_chere(self):
        for rec in self:
            if not rec.ligne_ids:
                raise UserError("Ajoutez d'abord au moins une offre de fournisseur.")
            moins_chere = min(rec.ligne_ids, key=lambda l: l.total)
            for ligne in rec.ligne_ids:
                ligne.retenue = ligne == moins_chere

    def action_valider(self):
        for rec in self:
            if len(rec.ligne_ids.filtered("retenue")) != 1:
                raise UserError("Retenez exactement une offre avant de valider la cotation.")
        self.write({"statut": "validee"})

    def action_recevoir(self):
        for rec in self:
            rec.piece_id.sudo().quantite_stock += rec.quantite
            rec.message_post(body="Commande reçue : %s unité(s) ajoutée(s) au stock." % rec.quantite)
        self.write({"statut": "recue"})

    def action_annuler(self):
        self.write({"statut": "annulee"})


class CdtCotationLigne(models.Model):
    _name = "cdt.cotation.ligne"
    _description = "Offre d'un fournisseur"

    cotation_id = fields.Many2one("cdt.cotation", string="Cotation", required=True, ondelete="cascade")
    fournisseur_id = fields.Many2one("res.partner", string="Fournisseur", required=True)
    prix_unitaire = fields.Float(string="Prix unitaire")
    delai_jours = fields.Integer(string="Délai (jours)")
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    retenue = fields.Boolean(string="Offre retenue")

    @api.depends("prix_unitaire", "cotation_id.quantite")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.prix_unitaire * rec.cotation_id.quantite