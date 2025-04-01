from odoo import models, fields, api
import qrcode
from io import BytesIO
import base64

class ContactQRCode(models.Model):
    _name = "contact.qrcode"
    _description = "Gestion des cartes de visites"
    #_inherit = "res.partner" 

    name = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    telephone = fields.Char(string="Téléphone", required=True)
    entreprise = fields.Char(string="Entreprise", required=True)
    poste = fields.Char(string="Poste", required=True)
    adresse = fields.Char(string="Adresse", required=True)
    email = fields.Char(string="Email", required=True)
    qr_code = fields.Binary("QR Code", attachment=True, readonly=True)

    def _generate_qr_code(self):
        """Génère le QR Code pour chaque enregistrement"""
        for record in self:
            vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{record.prenom} {record.name}
TEL:{record.telephone}
EMAIL:{record.email}
ORG:{record.entreprise}
TITLE:{record.poste}
ADR:;;{record.adresse}
END:VCARD"""

            qr = qrcode.QRCode(
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4,
            )
            qr.add_data(vcard)
            qr.make(fit=True)

            img = qr.make_image(fill="black", back_color="white")

            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())

            record.qr_code = qr_image  

    @api.model
    def create(self, values):
        """Créer l'enregistrement et générer immédiatement le QR Code"""
        record = super(ContactQRCode, self).create(values)
        record._generate_qr_code()  
        return record

    def write(self, values):
        """Met à jour les champs et régénère le QR Code si un champ est modifié"""
        result = super(ContactQRCode, self).write(values)
        
        if any(field in values for field in ["name", "prenom", "telephone", "entreprise", "poste", "adresse", "email"]):
            self._generate_qr_code()  

        return result
