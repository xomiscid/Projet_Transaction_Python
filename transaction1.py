import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from datetime import datetime
import qrcode  # Pour la génération de QR code
from PIL import Image, ImageTk  # Pour afficher le QR code avec tkinter
import os

# Classe principale de l'application
class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Transactions")
        self.root.geometry("800x800")
        self.root.configure(bg="#f0f4f8")

        # Variables d'utilisateur
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.balance = 5000  # Montant fixe de départ
        self.receiver_username = tk.StringVar()
        self.transfer_amount = tk.DoubleVar()

        # Variables pour l'inscription
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.signup_password = tk.StringVar()
        self.confirm_password = tk.StringVar()

        # Chemin du fichier de base de données
        self.users_file = "BD.txt"

        # État du thème
        self.is_dark = False

        # Interface utilisateur
        self.create_login_frame()

        # Bouton pour changer de thème
        self.theme_button = ttk.Button(self.root, text="Changer de thème", command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    def toggle_theme(self):
        """Bascule entre le mode clair et le mode sombre."""
        if self.is_dark:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()

    def apply_dark_mode(self):
        """Applique le mode sombre à l'interface."""
        self.root.configure(bg='Black')
        for widget in self.root.winfo_children():
            widget.configure(bg='Black', fg='White')
        self.is_dark = True

    def apply_light_mode(self):
        """Applique le mode clair à l'interface."""
        self.root.configure(bg='White')
        for widget in self.root.winfo_children():
            widget.configure(bg='White', fg='Black')
        self.is_dark = False

    def generate_qr_code(self, phone_number):
        """Génère un QR code basé sur le numéro de téléphone."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(phone_number)
        qr.make(fit=True)

        qr_img = qr.make_image(fill="black", back_color="white")
        qr_img_path = f"{phone_number}_qrcode.png"
        qr_img.save(qr_img_path)
        return qr_img_path

    def save_user(self, user_data):
        """Enregistre les données de l'utilisateur dans un fichier texte."""
        with open(self.users_file, "a") as f:
            f.write(f"{user_data['phone']},{user_data['first_name']},{user_data['last_name']},{user_data['password']}\n")

    def login(self):
        """Vérifie les informations de connexion."""
        user_phone = self.username.get()
        user_pwd = self.password.get()

        if not os.path.exists(self.users_file):
            messagebox.showerror("Erreur", "Aucun utilisateur enregistré.")
            return

        with open(self.users_file, "r") as f:
            for line in f:
                user_info = line.strip().split(',')
                if user_info[0] == user_phone and user_info[3] == user_pwd:
                    messagebox.showinfo("Succès", "Connexion réussie!")
                    # Générer le QR code après la connexion
                    self.qr_code_path = self.generate_qr_code(user_phone)
                    self.create_transaction_frame()
                    return

        messagebox.showerror("Erreur", "Numéro de téléphone ou mot de passe incorrect.")

    def create_transaction_frame(self):
        """Créer l'interface de transaction."""
        self.clear_frame()
        ttk.Label(self.root, text="FINTECH", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)

        # Afficher le QR code généré
        if hasattr(self, 'qr_code_path') and os.path.exists(self.qr_code_path):
            qr_img = Image.open(self.qr_code_path)
            qr_img.resize((150, 150), Image.LANCZOS)  # Utiliser LANCZOS au lieu d'ANTIALIAS
            self.qr_code_image = ImageTk.PhotoImage(qr_img)

            self.qr_code_label = ttk.Label(self.root, image=self.qr_code_image)
            self.qr_code_label.pack(pady=10)  # Afficher le QR code ici, avant le solde
        else:
            messagebox.showwarning("QR Code manquant", "Le QR code n'a pas pu être trouvé.")

        self.balance_label = ttk.Label(self.root, text=f"Solde : {self.balance} F", font=("Helvetica", 14), background="#f0f4f8")
        self.balance_label.pack(pady=10)

        ttk.Label(self.root, text="Nom d'utilisateur du destinataire:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.receiver_username).pack()
        ttk.Label(self.root, text="Montant à transférer:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.transfer_amount).pack()

        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=15)

        transfer_button = ttk.Button(frame_buttons, text="Transférer", command=self.transfer_funds)
        transfer_button.grid(row=0, column=0, padx=5)

        convert_button = ttk.Button(frame_buttons, text="Convertisseur", command=self.open_converter)
        convert_button.grid(row=0, column=1, padx=5)

        ttk.Label(self.root, text="Historique des Transactions:").pack(pady=10)
        self.transaction_list = tk.Listbox(self.root, width=50, height=8)
        self.transaction_list.pack(pady=10)

    def create_login_frame(self):
        """Créer l'interface de connexion."""
        self.clear_frame()
        ttk.Label(self.root, text="Connexion", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)

        ttk.Label(self.root, text="Numéro de téléphone:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.username).pack()
        ttk.Label(self.root, text="Mot de passe:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.password, show="*").pack()

        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=15)

        login_button = ttk.Button(frame_buttons, text="Se connecter", command=self.login)
        login_button.grid(row=0, column=0, padx=5)

        signup_button = ttk.Button(frame_buttons, text="S'inscrire", command=self.create_signup_frame)
        signup_button.grid(row=0, column=1, padx=5)

    def create_signup_frame(self):
        """Créer l'interface d'inscription."""
        self.clear_frame()
        ttk.Label(self.root, text="Inscription", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)

        ttk.Label(self.root, text="Prénom:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.first_name).pack()
        ttk.Label(self.root, text="Nom:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.last_name).pack()
        ttk.Label(self.root, text="Numéro de téléphone:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.phone_number).pack()
        ttk.Label(self.root, text="Mot de passe:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.signup_password, show="*").pack()
        ttk.Label(self.root, text="Confirmer le mot de passe:").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.confirm_password, show="*").pack()

        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=15)

        signup_button = ttk.Button(frame_buttons, text="S'inscrire", command=self.signup)
        signup_button.grid(row=0, column=0, padx=5)

        login_button = ttk.Button(frame_buttons, text="Se connecter", command=self.create_login_frame)
        login_button.grid(row=0, column=1, padx=5)

    def signup(self):
        """Enregistre les données de l'utilisateur."""
        user_data = {
            "phone": self.phone_number.get(),
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "password": self.signup_password.get()
        }

        if self.signup_password.get() != self.confirm_password.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        self.save_user(user_data)
        messagebox.showinfo("Succès", "Inscription réussie!")
        self.create_login_frame()

    def clear_frame(self):
        """Efface le contenu de la fenêtre."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def transfer_funds(self):
        """Transfère des fonds à un autre utilisateur."""
        receiver_username = self.receiver_username.get()
        transfer_amount = self.transfer_amount.get()

        if transfer_amount > self.balance:
            messagebox.showerror("Erreur", "Montant insuffisant.")
            return

        self.balance -= transfer_amount
        self.balance_label['text'] = f"Solde : {self.balance} F"

        # Enregistrer la transaction dans l'historique
        self.transaction_list.insert(tk.END, f"Transfert de {transfer_amount} F à {receiver_username}")

    def open_converter(self):
        """Ouvre la fenêtre de conversion."""
        converter_window = tk.Toplevel(self.root)
        converter_window.title("Convertisseur")

        # Interface de conversion
        ttk.Label(converter_window, text="Convertisseur", font=("Helvetica", 18, "bold")).pack(pady=15)

        ttk.Label(converter_window, text="Montant à convertir:").pack(pady=5)
        ttk.Entry(converter_window).pack()

        ttk.Label(converter_window, text="Devise de départ:").pack(pady=5)
        ttk.Combobox(converter_window).pack()

        ttk.Label(converter_window, text="Devise de destination:").pack(pady=5)
        ttk.Combobox(converter_window).pack()

        ttk.Button(converter_window, text="Convertir").pack(pady=15)

# Création et lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()
