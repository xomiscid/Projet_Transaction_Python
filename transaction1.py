from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
import qrcode
import subprocess
import matplotlib.pyplot as plt
import os
import re

from kivy.core.window import Window

# Définir la couleur de fond (exemple : gris clair)
Window.clearcolor = ('slategray')

# Classe principale de l'application
class TransactionApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.username = ""
        self.balance = 5000
        self.qr_code_path = ""
        self.users_file = "BD.txt"

        # Commence par la page d'accueil
        self.create_welcome_screen()

        # Commence par la page d'accueil
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Création de la page d'accueil avec une image et un bouton."""
        self.clear_widgets()

        # Ajouter une image centrée
        self.add_widget(Image(
            source="/home/amabouakhamis/FINAL_FINTECH/fintech_logo3.png",
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1.0, 0.4)  # Ajuster la taille de l'image pour qu'elle ne prenne pas trop de place
        ))

        # Ajouter un bouton "Entrer"
        enter_button = Button(
            text="Entrer",
            font_size=24,
            size_hint=(0.3, 0.1),  # Ajuster la taille du bouton pour un meilleur espacement
            pos_hint={'center_x': 0.5},
            on_press=self.create_login_screen
        )
        self.add_widget(enter_button)

    def create_login_screen(self, instance=None):
        """Création de l'écran de connexion."""
        self.clear_widgets()

        self.add_widget(Label(
            text="Connexion",
            font_size=32,
            size_hint=(1, 0.1)  # Réduire la taille du label pour un affichage plus équilibré
        ))

        self.username_input = TextInput(
            hint_text="Numéro de téléphone",
            multiline=False,
            size_hint=(0.7, 0.1),  # Ajuster la taille de l'input
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.username_input)
        self.password_input = TextInput(
            hint_text="Mot de passe",
            password=True,
            multiline=False,
            size_hint=(0.7, 0.1),  # Ajuster la taille de l'input
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.password_input)

        button_layout = BoxLayout(size_hint=(1, 0.2), padding=3, spacing=3)
        login_button = Button(
            text="Connexion",
            size_hint=(0.2, 0.2),
            on_press=self.login
        )
        signup_button = Button(
            text="Inscription",
            size_hint=(0.2, 0.2),
            on_press=self.create_signup_screen
        )
        button_layout.add_widget(login_button)
        button_layout.add_widget(signup_button)
        self.add_widget(button_layout)

    def create_signup_screen(self, instance=None):
        self.clear_widgets()

        self.add_widget(Label(text="Inscription", font_size=30, size_hint=(1, 0.2)))
        self.first_name_input = TextInput(hint_text="Prenom", multiline=False, size_hint=(0.9, 0.1),
                                          pos_hint={'center_x': 0.5})
        self.add_widget(self.first_name_input)
        self.last_name_input = TextInput(hint_text="Nom", multiline=False, size_hint=(0.9, 0.1),
                                         pos_hint={'center_x': 0.5})
        self.add_widget(self.last_name_input)
        self.phone_number_input = TextInput(hint_text="Numéro de téléphone", multiline=False, size_hint=(0.9, 0.1),
                                            pos_hint={'center_x': 0.5})
        self.add_widget(self.phone_number_input)
        self.password_input = TextInput(hint_text="Mot de passe", password=True, multiline=False, size_hint=(0.9, 0.1),
                                        pos_hint={'center_x': 0.5})
        self.add_widget(self.password_input)
        self.confirm_password_input = TextInput(hint_text="Confirmer le mot de passe", password=True, multiline=False,
                                                size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5})
        self.add_widget(self.confirm_password_input)

        button_layout = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        signup_button = Button(text="S'inscrire", size_hint=(0.5, 1), on_press=self.signup)
        back_button = Button(text="Retour", size_hint=(0.5, 1), on_press=lambda x: self.create_login_screen())
        button_layout.add_widget(signup_button)
        button_layout.add_widget(back_button)
        self.add_widget(button_layout)

    def create_transaction_screen(self):
        """Affiche l'écran des transactions."""
        self.clear_widgets()

        # En-tête avec le menu
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        options_spinner = Spinner(
            text="Menu",
            values=["profil", "Modifier le mot de passe","Mon historique", "Voir graphique des transferts","Help","Deconnexion"],
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5}
        )
        options_spinner.bind(text=self.handle_menu_selection)
        header_layout.add_widget(Label(text="", size_hint=(0.7, 1)))  # Espace vide
        header_layout.add_widget(options_spinner)
        self.add_widget(header_layout)

        # Section QR Code agrandi
        qr_code_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.4), padding=10)
        qr_code_label = Label(font_size=20, size_hint=(1, 0.2))

        if self.qr_code_path and os.path.exists(self.qr_code_path):
            qr_code_image = Image(source=self.qr_code_path, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5})
        else:
            qr_code_image = Label(text="Pas de QR Code disponible", size_hint=(0.8, 0.8))

        # Montant affiché sous le QR code (corrigé pour ajouter `balance_label`)
        self.balance_label = Label(
            text=f"Solde : {self.balance} F",
            font_size=16,
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5}
        )
        qr_code_layout.add_widget(qr_code_label)
        qr_code_layout.add_widget(qr_code_image)
        qr_code_layout.add_widget(self.balance_label)
        self.add_widget(qr_code_layout)

        # Champs pour le transfert
        self.receiver_username_input = TextInput(
            hint_text="Numero de l'utilisateur destinataire", size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.receiver_username_input)

        self.transfer_amount_input = TextInput(
            hint_text="Montant à transférer", size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.transfer_amount_input)

        # Bouton pour effectuer le transfert
        transfer_button = Button(
            text="Transférer",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            on_press=self.transfer_funds
        )
        self.add_widget(transfer_button)

        # Bouton Convertisseur
        converter_button = Button(
            text="Convertisseur de devises",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            on_press=self.open_conversion_app
        )
        self.add_widget(converter_button)

        # Historique des transactions
        history_label = Label(text="Historique des Transactions", font_size=18, size_hint=(1, 0.1))
        self.add_widget(history_label)

        scroll_view = ScrollView(size_hint=(1, 0.4))
        self.transaction_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.transaction_list.bind(minimum_height=self.transaction_list.setter('height'))
        scroll_view.add_widget(self.transaction_list)
        self.add_widget(scroll_view)


    def open_conversion_app(self, instance):
        """Ouvre l'application CONVERSION.py."""
        try:
            subprocess.Popen(['python3', 'CONVERSION.py'])
        except Exception as e:
            self.show_popup("Erreur", f"Impossible d'ouvrir l'application de conversion: {e}")

    def add_transaction(self, transaction):
        """Ajoute une transaction à l'historique."""
        # Crée un label pour chaque transaction
        transaction_label = Label(text=transaction, size_hint_y=None, height=30)
        self.transaction_list.add_widget(transaction_label)

        # Met à jour la hauteur du BoxLayout pour que le ScrollView s'ajuste
        self.transaction_list.height += transaction_label.height  # Augmenter la hauteur totale du BoxLayout

    def handle_menu_selection(self, spinner, text):
        """Gère les actions en fonction de la sélection dans le menu."""
        if text == "profil":
            self.show_profil()
        elif text == "Modifier le mot de passe":
            self.change_password()
        elif text == "Voir graphique des transferts":
            self.show_transfer_graph()
        elif text =="Help":
            self.show_help()
        elif text == "Mon historique":
            self.show_transaction_history()
        elif text == "Deconnexion":
            self.disconnect()

    def disconnect(self):
        """Déconnecte l'utilisateur et retourne à l'écran de connexion."""
        # Réinitialiser les informations utilisateur
        self.username = ""
        self.balance = 0
        self.qr_code_path = ""

        # Afficher un message de confirmation
        self.show_popup("Info", "deconnexion avec succès.", self.create_login_screen)

    def show_transaction_history(self):
        """Affiche l'historique des transactions (envoyées et reçues) pour l'utilisateur connecté."""
        user_phone = self.username  # Numéro de l'utilisateur connecté

        # Vérifier si le fichier de transactions existe
        if not os.path.exists("transactions.txt"):
            self.show_popup("Info", "Aucune transaction trouvée.")
            return

        # Lire les transactions depuis le fichier
        transactions = []
        with open("transactions.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    sender, amount, receiver = parts
                    # Ajouter à l'historique si l'utilisateur est impliqué
                    if sender == user_phone or receiver == user_phone:
                        if sender == user_phone:
                            transactions.append(f"Envoyé : {amount} F à {receiver}")
                        if receiver == user_phone:
                            transactions.append(f"Reçu : {amount} F de {sender}")

        # Vérifier si l'historique est vide
        if not transactions:
            self.show_popup("Info", "Aucune transaction trouvée pour cet utilisateur.")
            return

        # Afficher les transactions dans une fenêtre défilante
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        for transaction in transactions:
            layout.add_widget(Label(text=transaction, size_hint_y=None, height=30))

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(layout)

        popup_content = BoxLayout(orientation="vertical")
        popup_content.add_widget(scroll_view)
        close_button = Button(text="Fermer", size_hint=(1, 0.1))
        close_button.bind(on_press=lambda x: popup.dismiss())
        popup_content.add_widget(close_button)

        popup = Popup(title="Historique des Transactions", content=popup_content, size_hint=(0.9, 0.9))
        popup.open()

    def show_help(self):
        """Affiche une fenêtre d'aide pour guider l'utilisateur."""
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Titre
        content.add_widget(Label(
            text="Aide et Support",
            font_size=24,
            bold=True,
            size_hint_y=None,
            height=40
        ))

        # Texte descriptif
        help_text = (
            "Bienvenue dans l'application de transfert !\n\n"
            "1. Connexion : Utilisez votre numéro et mot de passe.\n"
            "2. Inscription : Créez un compte avec vos informations.\n"
            "3. Transferts : Entrez le numéro du destinataire et le montant.\n"
            "4. Historique : Consultez vos transactions récentes.\n"
            "5. Solde : Vérifiez votre solde actuel sous le QR Code.\n"
            "6. QR Code : Partagez vos informations avec ce code unique.\n"
            "7. Convertisseur : Changez entre devises (USD, EUR, XOF).\n\n"
            "Besoin d'aide supplémentaire ? Contactez le support."
        )
        content.add_widget(Label(text=help_text, size_hint_y=None, height=400))

        # Bouton pour fermer
        close_button = Button(text="Fermer", size_hint_y=None, height=40)
        close_button.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_button)

        # Popup
        popup = Popup(title="Aide", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def show_profil(self):
        """Affiche le profil de l'utilisateur."""
        
        # Layout principal pour le profil
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        
        # Titre du profil
        title = Label(text="Profil", font_size=24, bold=True, size_hint_y=None, height=40)
        layout.add_widget(title)
        
        # Récupérer les informations de l'utilisateur
        user_found = False
        with open("BD.txt", "r") as f:
            for line in f:
                user_info = line.strip().split(',')
                if user_info[0] == self.username:  # Remplacez `self.username` par la variable contenant le numéro ou identifiant de l'utilisateur
                    user_found = True
                    layout.add_widget(Label(text=f"Nom : {user_info[1]}", size_hint_y=None, height=30))
                    layout.add_widget(Label(text=f"Prénom : {user_info[2]}", size_hint_y=None, height=30))
                    layout.add_widget(Label(text=f"Numéro de téléphone : {user_info[0]}", size_hint_y=None, height=30))
                    break

        if not user_found:
            layout.add_widget(Label(text="Utilisateur non trouvé.", size_hint_y=None, height=30))

        # Utiliser un ScrollView pour gérer les débordements si les informations sont nombreuses
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        # Afficher les informations dans une popup
        popup = Popup(title="Profil", content=scroll_view, size_hint=(0.8, 0.5))
        popup.open()

    def change_password(self):
        """Affiche une popup pour modifier le mot de passe."""
        content = BoxLayout(orientation='vertical', spacing=10)
        old_pwd = TextInput(hint_text="Ancien mot de passe", password=True)
        new_pwd = TextInput(hint_text="Nouveau mot de passe", password=True)
        confirm_pwd = TextInput(hint_text="Confirmer le mot de passe", password=True)

        submit_button = Button(text="Modifier", size_hint=(1, 0.2))
        content.add_widget(old_pwd)
        content.add_widget(new_pwd)
        content.add_widget(confirm_pwd)
        content.add_widget(submit_button)

        popup = Popup(title="Modifier le mot de passe", content=content, size_hint=(0.8, 0.5))
        submit_button.bind(
            on_press=lambda x: self.save_new_password(old_pwd.text, new_pwd.text, confirm_pwd.text, popup))
        popup.open()

    def save_new_password(self, old_pwd, new_pwd, confirm_pwd, popup):
        """Vérifie et met à jour le mot de passe de l'utilisateur dans la base de données."""
        if not os.path.exists(self.users_file):
            self.show_popup("Erreur", "Base de données introuvable.")
            return

        # Charger les utilisateurs depuis la base de données
        users = []
        user_found = False
        with open(self.users_file, "r") as file:
            for line in file:
                user_info = line.strip().split(',')
                if user_info[0] == self.username:  # Correspondance avec l'utilisateur connecté
                    if user_info[3] != old_pwd:  # Vérifier l'ancien mot de passe
                        self.show_popup("Erreur", "Ancien mot de passe incorrect.")
                        return
                    if new_pwd != confirm_pwd:  # Vérifier la confirmation
                        self.show_popup("Erreur", "Les mots de passe ne correspondent pas.")
                        return
                    # Remplacer par le nouveau mot de passe
                    user_info[3] = new_pwd
                    user_found = True
                users.append(user_info)

        if not user_found:
            self.show_popup("Erreur", "Utilisateur non trouvé.")
            return

        # Sauvegarder les modifications dans le fichier
        with open(self.users_file, "w") as file:
            for user in users:
                file.write(','.join(user) + '\n')

        self.show_popup("Succès", "Mot de passe modifié avec succès !")
        popup.dismiss()
    def show_transfer_graph(self):
        """Affiche un graphique des transferts pour l'utilisateur connecté."""
        user_phone = self.username  # Utilisez `self.username` pour récupérer l'utilisateur connecté
        transfers = []

        # Lire l'historique des transactions
        try:
            with open("transactions.txt", "r") as f:
                for line in f:
                    # Vérifier si la ligne contient un transfert valide pour l'utilisateur connecté
                    parts = line.strip().split()
                    if len(parts) == 3:  # Chaque ligne doit avoir 3 parties : expéditeur, montant, destinataire
                        sender, amount, receiver = parts
                        amount = float(amount)  # Conversion du montant en float

                        # Si l'expéditeur correspond à l'utilisateur connecté, ajouter à la liste des transferts
                        if sender == user_phone:
                            transfers.append(amount)

        except FileNotFoundError:
            self.show_popup("Erreur", "Aucun fichier de transactions trouvé.")
            return

        # Vérifiez si des transferts existent
        if not transfers:
            self.show_popup("Info", "Aucun transfert trouvé pour cet utilisateur.")
            return

        # Afficher le graphique
        try:
            plt.figure(figsize=(8, 4))
            plt.bar(range(len(transfers)), transfers, color='blue')
            plt.xlabel("Transferts")
            plt.ylabel("Montants (F)")
            plt.title("Graphique des Transferts")
            plt.show()
        except Exception as e:
            self.show_popup("Erreur", f"Impossible d'afficher le graphique : {e}")

    def show_popup(self, title, message, callback=None):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))

        def on_popup_close(instance):
            popup.dismiss()
            if callback:
                callback()

        close_button.bind(on_press=on_popup_close)
        popup.open()

    def login(self, instance):
        """Vérifie les informations de connexion et connecte l'utilisateur."""
        user_phone = self.username_input.text.strip()
        user_pwd = self.password_input.text.strip()

        # Vérification des champs vides
        if not user_phone or not user_pwd:
            self.show_popup("Erreur", "Veuillez remplir tous les champs.")
            return

        if not os.path.exists(self.users_file):
            self.show_popup("Erreur", "Aucun utilisateur enregistré.")
            return

        with open(self.users_file, "r") as f:
            for line in f:
                user_info = line.strip().split(',')
                if user_info[0] == user_phone and user_info[3] == user_pwd:
                    # Connexion réussie
                    self.username = user_phone
                    self.balance = float(user_info[4])  # Récupération automatique du solde
                    self.qr_code_path = self.generate_qr_code(user_phone)
                    self.show_popup("Succès", "Connexion réussie!", self.create_transaction_screen)
                    return

        self.show_popup("Erreur", "Numéro de téléphone ou mot de passe incorrect.")

    def signup(self, instance):
        """Vérifie les informations d'inscription et enregistre l'utilisateur."""
        user_data = {
            "phone": self.phone_number_input.text.strip(),
            "first_name": self.first_name_input.text.strip(),
            "last_name": self.last_name_input.text.strip(),
            "password": self.password_input.text.strip(),
            "confirm_password": self.confirm_password_input.text.strip()
        }

        if not re.fullmatch(r"\d{6}", user_data["password"]):
            self.show_popup("Erreur", "Le mot de passe doit contenir exactement 6 chiffres.")
            return


        # Vérification des champs vides
        if not all(user_data.values()):
            self.show_popup("Erreur", "Veuillez remplir tous les champs.")
            return

        if user_data["password"] != user_data["confirm_password"]:
            self.show_popup("Erreur", "Les mots de passe ne correspondent pas.")
            return

        # Vérification si l'utilisateur existe déjà
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                for line in f:
                    existing_user = line.strip().split(',')
                    if existing_user[0] == user_data['phone']:  # Vérifie si le numéro de téléphone existe déjà
                        self.show_popup("Erreur", "Cet utilisateur existe déjà.")
                        return

        self.save_user(user_data)
        self.show_popup("Succès", "Inscription réussie!", self.create_login_screen)

    def transfer_funds(self, instance):
        """Effectue un transfert de fonds et met à jour le solde de l'expéditeur et du destinataire."""
        receiver = self.receiver_username_input.text.strip()

        # Vérification si le destinataire existe dans la base de données
        if not self.is_user_in_database(receiver):
            self.show_popup("Erreur", "Destinataire non trouvé dans la base de données.")
            return

        try:
            # Lecture et validation du montant
            amount = float(self.transfer_amount_input.text)
            if amount <= 0:
                self.show_popup("Erreur", "Le montant doit être supérieur à zéro.")
                return

            # Chargement des utilisateurs depuis BD.txt
            users = []
            with open(self.users_file, "r") as file:
                for line in file:
                    users.append(line.strip().split(','))

            # Recherche des utilisateurs
            sender_data = None
            receiver_data = None
            for user in users:
                if user[0] == self.username:
                    sender_data = user
                if user[0] == receiver:
                    receiver_data = user

            if not sender_data:
                self.show_popup("Erreur", "Utilisateur expéditeur non trouvé.")
                return

            if not receiver_data:
                self.show_popup("Erreur", "Utilisateur destinataire non trouvé.")
                return

            sender_balance = float(sender_data[4])
            receiver_balance = float(receiver_data[4])

            # Vérification des fonds suffisants
            if amount > sender_balance:
                self.show_popup("Erreur", "Fonds insuffisants.")
                return

            # Mise à jour des soldes
            sender_balance -= amount
            receiver_balance += amount
            sender_data[4] = str(sender_balance)
            receiver_data[4] = str(receiver_balance)

            # Sauvegarde des nouveaux soldes dans BD.txt
            with open(self.users_file, "w") as file:
                for user in users:
                    file.write(','.join(user) + '\n')

            # Mise à jour du label de solde
            self.balance = sender_balance
            self.balance_label.text = f"Solde : {self.balance} F"

            # Enregistrer la transaction dans transactions.txt
            with open("transactions.txt", "a") as f:
                f.write(f"{self.username} {amount} {receiver}\n")

            # Ajouter la transaction à l'historique
            transaction = f"Transfert de {amount:.2f} F de {self.username} à {receiver}."
            self.add_transaction(transaction)

            self.show_popup("Succès", f"Transfert de {amount} F à {receiver} réussi !")

        except ValueError:
            self.show_popup("Erreur", "Veuillez entrer un montant valide.")

    def is_user_in_database(self, username):
        """Vérifie si un utilisateur est dans la base de données (BD.txt)."""
        if not os.path.exists(self.users_file):
            return False

        with open(self.users_file, "r") as f:
            for line in f:
                user_info = line.strip().split(',')
                if user_info[0] == username:
                    return True
        return False

    def open_converter_popup(self, instance):
        """Ouvre le popup de convertisseur de devises."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Convertisseur", font_size=24, size_hint=(1, 0.2)))

        # Entrée pour le montant à convertir
        amount_input = TextInput(hint_text="Montant à convertir", multiline=False, size_hint=(1, 0.2))
        content.add_widget(amount_input)

        # Sélecteurs de devises
        currency_from = Spinner(
            text="Devise de départ",
            values=["USD", "EUR", "XOF"],
            size_hint=(1, 0.2)
        )
        content.add_widget(currency_from)

        currency_to = Spinner(
            text="Devise de destination",
            values=["USD", "EUR", "XOF"],
            size_hint=(1, 0.2)
        )
        content.add_widget(currency_to)

        # Résultat de la conversion
        result_label = Label(text="Résultat: ", size_hint=(1, 0.2), font_size=18)
        content.add_widget(result_label)

        # Bouton de conversion
        def perform_conversion(instance):
            try:
                amount = float(amount_input.text)
                from_currency = currency_from.text
                to_currency = currency_to.text

                if from_currency == "Devise de départ" or to_currency == "Devise de destination":
                    result_label.text = "Erreur: Sélectionnez les devises."
                    return

                result = self.convert_currency(amount, from_currency, to_currency)
                result_label.text = f"Résultat: {result:.2f} {to_currency}"
            except ValueError:
                result_label.text = "Erreur: Veuillez entrer un montant valide."

        convert_button = Button(text="Convertir", size_hint=(1, 0.2))
        convert_button.bind(on_press=perform_conversion)
        content.add_widget(convert_button)

        # Affichage du popup
        popup = Popup(title="Convertisseur", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def convert_currency(self, amount, from_currency, to_currency):
        """Convertit un montant d'une devise à une autre."""
        # Taux de change prédéfinis (exemple)
        rates = {
            "USD": {"USD": 1, "EUR": 0.92, "XOF": 600},
            "EUR": {"USD": 1.09, "EUR": 1, "XOF": 655},
            "XOF": {"USD": 0.00167, "EUR": 0.00153, "XOF": 1},
        }

        if from_currency not in rates or to_currency not in rates[from_currency]:
            raise ValueError("Conversion non prise en charge.")

        return amount * rates[from_currency][to_currency]

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,  # Augmente la taille des cases du QR code
            border=6  # Augmente la bordure du QR code
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        path = f"{data}_qrcode.png"
        img.save(path)
        return path

    def save_user(self, user_data):
        with open(self.users_file, "a") as f:
            f.write(
                f"{user_data['phone']},{user_data['first_name']},{user_data['last_name']},{user_data['password']},5000\n")

    def show_popup(self, title, message, callback=None):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        close_button.bind(on_press=popup.dismiss)
        if callback:
            close_button.bind(on_press=lambda instance: callback())
        popup.open()

class FintechApp(App):
    def build(self):
        return TransactionApp()


if __name__ == "__main__":
    FintechApp().run()