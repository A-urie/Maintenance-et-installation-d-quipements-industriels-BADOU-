from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CdtIntervention(models.Model):
    _name = "cdt.intervention"
    _description = "Intervention"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_planifiee desc, id desc"

    name = fields.Char(string="Référence", required=True, copy=False, tracking=True)
    demande_id = fields.Many2one("cdt.demande", string="Demande", ondelete="set null")
    equipement_id = fields.Many2one("cdt.equipement", string="Équipement", required=True, tracking=True)
    client_id = fields.Many2one(related="equipement_id.client_id", string="Client", store=True, readonly=True)
    technicien_ids = fields.Many2many("res.users", string="Techniciens")
    date_planifiee = fields.Datetime(string="Date planifiée", tracking=True)
    date_debut = fields.Datetime(string="Début")
    date_fin = fields.Datetime(string="Fin")
    duree = fields.Float(string="Durée (heures)", compute="_compute_duree", store=True)
    cause_panne = fields.Text(string="Cause de la panne")
    travaux = fields.Text(string="Travaux réalisés")
    cout = fields.Float(string="Coût")
    validation_client = fields.Boolean(string="Validée par le client")
    statut = fields.Selection(
        [
            ("planifiee", "Planifiée"),
            ("en_cours", "En cours"),
            ("terminee", "Terminée"),
            ("annulee", "Annulée"),
        ],
        string="Statut",
        default="planifiee",
        required=True,
        tracking=True,
    )

    @api.depends("date_debut", "date_fin")
    def _compute_duree(self):
        for rec in self:
            if rec.date_debut and rec.date_fin:
                rec.duree = (rec.date_fin - rec.date_debut).total_seconds() / 3600.0
            else:
                rec.duree = 0.0

    @api.constrains("date_debut", "date_fin")
    def _check_dates(self):
        for rec in self:
            if rec.date_debut and rec.date_fin and rec.date_fin < rec.date_debut:
                raise ValidationError("La date de fin doit être après la date de début.")

    def action_demarrer(self):
        self.write({"statut": "en_cours", "date_debut": fields.Datetime.now()})

    def action_cloturer(self):
        self.write({"statut": "terminee", "date_fin": fields.Datetime.now()})