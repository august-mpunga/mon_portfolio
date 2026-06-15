import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT (Fichier .env)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

# Clé secrète récupérée depuis l'environnement ou valeur de secours
app.secret_key = os.environ.get('SECRET_KEY', 'une_cle_secrete_de_secours_vba_excel_2026')

# ----------------- ROUTES -----------------

# Page 1 : Accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page 2 : À Propos & Services
@app.route('/a-propos')
def services():
    return render_template('services.html')

# Page 3 : Page produit - Logiciel Stock
@app.route('/logiciel-stock')
def stock():
    return render_template('stock.html')

# Page 4 : Contact (Formulaire et traitement)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('name')
        email_client = request.form.get('email')
        objet = request.form.get('subject')
        message_contenu = request.form.get('message')
        
        # Construction du message pour SendGrid
        message = Mail(
            from_email=os.environ.get('FROM_EMAIL'),
            to_emails=os.environ.get('TO_EMAIL'),
            subject=f"[Portfolio PRO] {objet}",
            plain_text_content=f"Tu as reçu un nouveau message depuis ton portfolio :\n\n"
                               f"Nom du client : {nom}\n"
                               f"Email du client : {email_client}\n"
                               f"Objet : {objet}\n\n"
                               f"Message :\n{message_contenu}"
        )
        
        try:
            # Envoi via l'API HTTP (Passe à travers le pare-feu de Render)
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(message)
            flash("Votre message a été transmis avec succès ! August vous répondra très rapidement.", "success")
        except Exception as e:
            flash("Une erreur est survenue lors de l'envoi. Veuillez réessayer ou utiliser les réseaux sociaux.", "error")
            print(f"Erreur d'envoi SendGrid : {e}")
            
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
