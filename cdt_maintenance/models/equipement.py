from odoo import fields, models


class CdtEquipement(models.Model):
    _name = "cdt.equipement"
    _description = "Équipement installé"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(string="Référence", required=True, tracking=True)
    numero_serie = fields.Char(string="Numéro de série", tracking=True)
    type_equipement = fields.Char(string="Type d'équipement")
    client_id = fields.Many2one("res.partner", string="Client", tracking=True)
    date_installation = fields.Date(string="Date d'installation")
    fin_garantie = fields.Date(string="Fin de garantie")
    frequence_maintenance = fields.Integer(
        string="Fréquence de maintenance (mois)",
        default=2,
        help="Nombre de mois entre deux visites périodiques.",
    )
    etat = fields.Selection(
        [
            ("brouillon", "Brouillon"),
            ("installe", "Installé"),
            ("en_maintenance", "En maintenance"),
            ("retire", "Retiré"),
        ],
        string="État",
        default="brouillon",
        required=True,
        tracking=True,
    )
    active = fields.Boolean(default=True)
    intervention_ids = fields.One2many("cdt.intervention", "equipement_id", string="Interventions")
    demande_ids = fields.One2many("cdt.demande", "equipement_id", string="Demandes")
    intervention_count = fields.Integer(string="Interventions", compute="_compute_counts")
    demande_count = fields.Integer(string="Demandes", compute="_compute_counts")

    _sql_constraints = [
        ("numero_serie_unique", "unique(numero_serie)", "Ce numéro de série existe déjà."),
    ]

    def _compute_counts(self):
        for rec in self:
            rec.intervention_count = len(rec.intervention_ids)
            rec.demande_count = len(rec.demande_ids)

    def action_voir_interventions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Historique des interventions",
            "res_model": "cdt.intervention",
            "view_mode": "list,form",
            "domain": [("equipement_id", "=", self.id)],
            "context": {"default_equipement_id": self.id},
        }

    def action_voir_demandes(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Historique des demandes",
            "res_model": "cdt.demande",
            "view_mode": "list,form",
            "domain": [("equipement_id", "=", self.id)],
            "context": {"default_equipement_id": self.id},
        }

    def action_installer(self):
        self.write({"etat": "installe"})

    def action_mettre_en_maintenance(self):
        self.write({"etat": "en_maintenance"})

    def action_retirer(self):
        self.write({"etat": "retire"})