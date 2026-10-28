# CDT – Maintenance et installation d'équipements industriels

Projet de l'**Atelier du Génie Logiciel** – Licence 3 Génie Logiciel, Institut Ivoirien de Technologie (IIT) – année académique 2026-2027.

**Auteur :** Urie

---

## 1. Présentation de l'entreprise

Le **CDT (Centre de Démonstration et de Promotion de Technologies)**, basé à Abidjan en Côte d'Ivoire, conçoit, fabrique, importe, installe et entretient des équipements industriels pour ses clients. Environ 80 % de ses machines sont fabriquées localement ; les autres sont importées auprès de fournisseurs.

Le CDT conserve aussi des machines en immobilisation, non vendues, qui servent aux démonstrations et dont les pièces de rechange sont stockées.

Après la livraison d'un équipement et la formation de l'utilisateur, le service technique assure la maintenance : des visites périodiques chez les clients et des dépannages sur appel, soit plus de 6 sorties par mois. Le programme de maintenance est aujourd'hui établi sur papier, lors d'une réunion hebdomadaire.

## 2. Présentation du projet

### Problématique

Le CDT exprime le besoin d'un logiciel de suivi technique de ses clients, regroupant les clients accompagnés, leurs équipements, leurs installations et leurs interventions.

### Solution proposée

Développement d'un **module Odoo 18 personnalisé**, nommé `cdt_maintenance`, avec une base de données **PostgreSQL**. Il permet de :

- gérer les clients et le parc d'équipements installés ;
- suivre les dossiers d'installation, de la livraison à la réception ;
- planifier les visites périodiques et les interventions sur appel, avec priorité et urgence ;
- remplir des fiches d'intervention numériques et conserver l'historique des pannes ;
- gérer les pièces de rechange, les cotations, les contrats et les prestataires ;
- recevoir des alertes automatiques (visites, garanties, contrats, stock) ;
- piloter l'activité avec un tableau de bord, des rapports PDF et des exports Excel ;
- offrir aux clients un **portail** pour suivre leurs équipements et interventions et donner leur avis.

### Acteurs

Client (portail), commercial, technicien, chef de maintenance, responsable stock et achats. Tous utilisent la même application ; chacun voit les écrans correspondant à son groupe.

## 3. Maquette

Maquette de l'interface : [Maquette_CDT sur Figma Make](https://www.figma.com/make/7epC81A9wj15MAMq5VfSxr/Maquette_CDT?code-node-id=0-6&p=f&t=zCzl6gzVan6JsL17-0&fullscreen=1)

## 4. Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `cadrage/` | Cahier des charges (`cahier_des_charges_cdt.docx`) |
| `modelisation/` | Diagrammes UML (`diagrammes_uml_cdt.drawio`) : cas d'utilisation, classes, séquence, activité |

Les diagrammes s'ouvrent avec [draw.io](https://app.diagrams.net) (Fichier > Ouvrir depuis > Appareil) ; chaque diagramme est un onglet du fichier.

## 5. Technologies

Odoo 18 · Python 3.11+ · PostgreSQL · XML (vues et rapports QWeb) · OWL (tableau de bord) · xlsxwriter (exports Excel)