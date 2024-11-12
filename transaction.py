import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

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

        # Transactions
        self.transactions = []

        # Interface utilisateur
        self.create_login_frame()

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

    def login(self):
        """Vérifie les informations de connexion."""
        user = self.username.get()
        pwd = self.password.get()

        # Vérification simple des identifiants
        if user == "atd" and pwd == "titi":
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.create_transaction_frame()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

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
