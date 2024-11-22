import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import re
import json
import os

# Classe principale de l'application
class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Transactions")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f4f8")

        # Variables d'utilisateur
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.balance = 5000  # Montant fixe de départ
        self.receiver_username = tk.StringVar()
        self.transfer_amount = tk.DoubleVar()
        
        #Variables pour l'inscription
        self.first_name=tk.StringVar()
        self.last_name=tk.StringVar()
        self.phone_number = tk.StringVar()
        self.country_code =tk.StringVar(value="221")#valeur par defaut
        self.signup_password = tk.StringVar()
        self.confirm_password = tk.StringVar()
        # base de donnees des users dans le JSON
        self.users_fichier="BD.json"
        
        
        # Transactions
        self.transactions = self.load_transactions()

        # Interface utilisateur
        self.create_login_frame()
    
    
    def save_user(self, user_data):
        """Enregistre les données de l'utilisateur dans un fichier JSON."""
        if os.path.exists(self.users_fichier):
            with open(self.users_fichier, "r") as f:
                users = json.load(f)
        else:
            users = {}

        users[user_data['username']] = user_data

        with open(self.user_file, "w") as f:
            json.dump(users, f, indent=4)

    def check_user(self, username, password):
        """Vérifie les informations de connexion de l'utilisateur."""
        if not os.path.exists(self.user_file):
            return False

        with open(self.user_file, "r") as f:
            users = json.load(f)

        return users.get(username) and users[username]["password"] == password

    def create_signup_frame(self):
        self.clear_frame()
        ttk.Label(self.root, text="Inscription", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)
        ttk.Label(self.root, text="Nom:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.last_name, font=("Helvetica", 12)).pack()
        ttk.Label(self.root, text="Prénom:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.first_name, font=("Helvetica", 12)).pack()
        ttk.Label(self.root, text="Indicatif téléphonique:", style="TLabel").pack(pady=5)
        ttk.Combobox(self.root, textvariable=self.country_code, values=["+221", "+33", "+1", "+91", "+44"], font=("Helvetica", 12)).pack()
        ttk.Label(self.root, text="Numéro de téléphone:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.phone_number, font=("Helvetica", 12)).pack()
        ttk.Label(self.root, text="Mot de passe (6 chiffres):", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.signup_password, show="*", font=("Helvetica", 12)).pack()
        ttk.Label(self.root, text="Confirmer le mot de passe:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.confirm_password, show="*", font=("Helvetica", 12)).pack()
        signup_button = ttk.Button(self.root, text="S'inscrire", command=self.signup, style="TButton")
        signup_button.pack(pady=20)
        back_button = ttk.Button(self.root, text="Retour", command=self.create_login_frame, style="TButton")
        back_button.pack(pady=20)    
    
    def signup(self):
        if not re.fullmatch(r"\d{6}", self.signup_password.get()):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir exactement 6 chiffres.")
            return
        if self.signup_password.get() != self.confirm_password.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        user_data = {
            "username": self.phone_number.get(),
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "phone": f"{self.country_code.get()} {self.phone_number.get()}",
            "password": self.signup_password.get()
        }
        self.save_user(user_data)
        messagebox.showinfo("Succès", "Inscription réussie! Vous pouvez maintenant vous connecter.")
        self.create_login_frame()
    
    def login(self):
        """Vérifie les informations de connexion."""
        user = self.username.get()
        pwd = self.password.get()

        # Vérification simple des identifiants
        if self.check_user(user, pwd):
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.create_transaction_frame()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def load_transactions(self):
        transactions = []   
        try:
            with open("transactions.txt", "r") as f:
                for line in f:
                    transactions.append(line.strip())
        except FileNotFoundError:
            pass
        return transactions    
    
    def save_transaction(self, transaction):
        with open("transactions.txt", "a") as f:
            f.write(transaction + "\n")

    def create_login_frame(self):
        """Créer l'interface de connexion."""
        self.clear_frame()

        # Titre
        ttk.Label(self.root, text="Connexion", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)

        # Champs de saisie
        ttk.Label(self.root, text="Nom d'utilisateur:", style="TLabel").pack(pady=5)
        username_entry = ttk.Entry(self.root, textvariable=self.username, font=("Helvetica", 12))
        username_entry.pack()
        username_entry.focus()

        ttk.Label(self.root, text="Mot de passe:", style="TLabel").pack(pady=5)
        password_entry = ttk.Entry(self.root, textvariable=self.password, show="*", font=("Helvetica", 12))
        password_entry.pack()

        # Bouton de connexion
        login_button = ttk.Button(self.root, text="Se connecter", command=self.login, style="TButton")
        login_button.pack(pady=20)
        
        # Bouton de inscription
        signup_button = ttk.Button(self.root, text="S'inscrire", command=self.create_signup_frame, style="TButton")
        signup_button.pack()

   
    
    def create_transaction_frame(self):
        """Créer l'interface de transaction."""
        self.clear_frame()

        # Titre et solde
        ttk.Label(self.root, text="Nouvelle Transaction", font=("Helvetica", 18, "bold"), background="#f0f4f8").pack(pady=15)
        self.balance_label = ttk.Label(self.root, text=f"Solde : {self.balance} F", font=("Helvetica", 14), background="#f0f4f8", foreground="#333")
        self.balance_label.pack(pady=10)

        # Entrée du nom d'utilisateur du destinataire
        ttk.Label(self.root, text="Nom d'utilisateur du destinataire:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.receiver_username, font=("Helvetica", 12)).pack()

        # Entrée du montant du transfert
        ttk.Label(self.root, text="Montant à transférer:", style="TLabel").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.transfer_amount, font=("Helvetica", 12)).pack()

        # Bouton pour effectuer le transfert
        transfer_button = ttk.Button(self.root, text="Transférer", command=self.transfer_funds, style="TButton")
        transfer_button.pack(pady=15)

        # Liste des transactions
        ttk.Label(self.root, text="Historique des Transactions:", font=("Helvetica", 14, "bold"), background="#f0f4f8").pack(pady=10)
        self.transaction_list = tk.Listbox(self.root, width=50, height=8, font=("Helvetica", 10), bg="#e8eff5", bd=0, highlightthickness=0, relief="flat")
        self.transaction_list.pack(pady=10)
    
    def transfer_funds(self):
        """Effectue un transfert vers un autre utilisateur"""
        receiver = self.receiver_username.get()
        transfer_amount = self.transfer_amount.get()

        # Vérifier les conditions de transfert
        if not receiver:
            messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur pour le destinataire.")
            return
        if transfer_amount <= 0:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
            return
        if transfer_amount > self.balance:
            messagebox.showerror("Erreur", "Solde insuffisant pour effectuer le transfert.")
            return

        # Effectuer le transfert
        self.balance -= transfer_amount
        self.balance_label.config(text=f"Solde : {self.balance} F")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = f"{timestamp} - Transféré {transfer_amount:.2f} F à {receiver}"
        self.transactions.append(transaction)
        self.transaction_list.insert(tk.END, transaction)

        # Réinitialiser les champs
        self.receiver_username.set("")
        self.transfer_amount.set(0.0)
        messagebox.showinfo("Succès", f"Transfert de {transfer_amount} F à {receiver} réussi!")

    def clear_frame(self):
        """Efface les widgets de la fenêtre."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Création et lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()
