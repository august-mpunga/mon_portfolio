import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT (Fichier .env)
# On essaie de charger dotenv. Si ça échoue (en production sur Render), 
# ce n'est pas grave car Render fournit déjà les variables.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

# En production, on essaie de lire une clé secrète sécurisée, sinon on garde une valeur par défaut
# La clé sera lue depuis ton fichier .env en local
app.secret_key = os.environ.get('SECRET_KEY', 'une_cle_secrete_de_secours_vba_excel_2026')

# Configuration de Flask-Mail pour Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'augustinmpunga30@gmail.com'

# SÉCURISATION : Le mot de passe est récupéré depuis ton fichier .env
# (ou depuis les variables d'environnement de Render)
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'augustinmpunga30@gmail.com'

mail = Mail(app)

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
        
        # Construction de l'email
        msg = Message(
            subject=f"[Portfolio PRO] {objet}",
            recipients=['augustinmpunga30@gmail.com'],
            body=f"Tu as reçu un nouveau message depuis ton portfolio :\n\n"
                 f"Nom du client : {nom}\n"
                 f"Email du client : {email_client}\n"
                 f"Objet : {objet}\n\n"
                 f"Message :\n{message_contenu}"
        )
        
        try:
            mail.send(msg)
            flash("Votre message a été transmis avec succès ! August vous répondra très rapidement.", "success")
        except Exception as e:
            flash("Une erreur est survenue lors de l'envoi. Veuillez réessayer ou utiliser les réseaux sociaux.", "error")
            print(f"Erreur d'envoi : {e}")
            
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

if __name__ == '__main__':
    # SÉCURISATION : En local sur ton PC, ça tourne en debug. 
    # Sur le web, le serveur de production ignorera ce bloc.
    app.run(debug=True)
