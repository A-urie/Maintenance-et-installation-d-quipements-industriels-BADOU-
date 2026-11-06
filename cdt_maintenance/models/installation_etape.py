from odoo import fields, models

ETAPES = [
    ("preparation", "Préparation du site"),
    ("livraison", "Livraison"),
    ("montage", "Montage"),
    ("essais", "Essais"),
    ("mise_en_service", "Mise en service"),
    ("formation", "Formation de l'utilisateur"),
]


class CdtInstallationEtape(models.Model):
    _name = "cdt.installation.etape"
    _description = "Étape d'installation"
    _order = "sequence, id"

    installation_id = fields.Many2one("cdt.installation", string="Dossier", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Ordre", default=10)
    name = fields.Selection(ETAPES, string="Étape", required=True)
    date_reelle = fields.Date(string="Date réelle")
    statut = fields.Selection(
        [("a_faire", "À faire"), ("en_cours", "En cours"), ("terminee", "Terminée")],
        string="Statut",
        default="a_faire",
        required=True,
    )
    note = fields.Char(string="Remarque")