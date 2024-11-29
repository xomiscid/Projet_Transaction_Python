#Convertisseur de devises

#Description :
"""
Ce programme est une application graphique permettant de convertir des montants d'une devise à une autre 
en fonction des taux de conversion prédéfinis. Il inclut des fonctionnalités d'historique, d'archivage, et de suppression/restauration 
des conversions précédentes. L'interface est développée avec Tkinter.

"""

import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterApp:
    """
    Classe principale de l'application.
    Permet de gérer l'interface et les fonctionnalités du convertisseur de devises.
    """

    def __init__(self, root):
        # Initialisation de la fenêtre principale et des variables
        self.root = root
        self.root.title("Convertisseur de Devises")
        self.history = []  # Liste pour stocker l'historique des conversions
        self.archived = []  # Liste pour stocker les conversions archivées
        self.deleted = []  # Liste pour stocker les conversions supprimées

        # Définir les taux de conversion
        self.conversion_rates = {
            'EUR (Euro)': 1.0,
            'USD (Dollar américain)': 1.12,
            'CFA (Franc CFA)': 655.957,
            'MAD (Dirham marocain)': 10.6,
            'JPY (Yen japonais)': 129.53,
            'GBP (Livre sterling)': 0.85,
            'CAD (Dollar canadien)': 1.5
        }

        # Configuration du menu principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu déroulant pour les options (archives et corbeille)
        archive_menu = tk.Menu(menubar, tearoff=0)
        archive_menu.add_command(label="Voir les archives", command=self.show_archives)
        archive_menu.add_command(label="Voir la corbeille", command=self.show_deleted)
        menubar.add_cascade(label="Menu", menu=archive_menu)

        # Widgets pour la saisie et l'affichage
        self.amount_label = tk.Label(root, text="Montant à convertir:")
        self.amount_label.pack()

        # Champ de saisie pour le montant avec validation
        self.amount_entry = tk.Entry(root, validate="key")
        self.amount_entry['validatecommand'] = (root.register(self.validate_amount), '%P')
        self.amount_entry.pack()

        self.from_currency_label = tk.Label(root, text="De:")
        self.from_currency_label.pack()

        # Liste déroulante pour sélectionner la devise d'origine
        self.from_currency = ttk.Combobox(root, values=list(self.conversion_rates.keys()), state="readonly")
        self.from_currency.pack()
        self.from_currency.current(0)

        self.to_currency_label = tk.Label(root, text="Vers:")
        self.to_currency_label.pack()

        # Liste déroulante pour sélectionner la devise cible
        self.to_currency = ttk.Combobox(root, values=list(self.conversion_rates.keys()), state="readonly")
        self.to_currency.pack()
        self.to_currency.current(1)

        # Bouton pour effectuer la conversion
        self.convert_button = tk.Button(root, text="Convertir", command=self.convert)
        self.convert_button.pack()

        # Label et liste pour afficher l'historique
        self.history_label = tk.Label(root, text="Historique des conversions:")
        self.history_label.pack()

        self.history_listbox = tk.Listbox(root)
        self.history_listbox.pack()

        # Lier un double-clic pour archiver ou supprimer une conversion
        self.history_listbox.bind('<Double-1>', self.archive_or_delete)

    def validate_amount(self, new_value):
        """
        Valide la saisie dans le champ du montant.
        Permet uniquement les chiffres, un point (pour les décimales), ou une chaîne vide.
        """
        if new_value == "":  # Permet une chaîne vide
            return True
        try:
            # Permet uniquement des nombres valides (entiers ou flottants)
            float(new_value)
            return True
        except ValueError:
            return False

    def convert(self):
        """
        Effectue la conversion entre deux devises sélectionnées.
        Ajoute le résultat à l'historique.
        """
        if not self.amount_entry.get() or float(self.amount_entry.get()) <= 0:
            # Affiche un message d'erreur si le montant est invalide
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide (nombre positif).")
            return

        amount = float(self.amount_entry.get())  # Récupère le montant saisi
        from_currency = self.from_currency.get()  # Devise d'origine
        to_currency = self.to_currency.get()  # Devise cible

        if from_currency not in self.conversion_rates or to_currency not in self.conversion_rates:
            # Affiche un message d'erreur si les devises sont invalides
            messagebox.showerror("Erreur", "Une des devises sélectionnées n'est pas valide.")
            return

        rate = self.conversion_rates[to_currency] / self.conversion_rates[from_currency]  # Taux de conversion
        converted_amount = amount * rate  # Calcul du montant converti

        result_message = f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"  # Message de résultat
        self.history.append(result_message)  # Ajoute le résultat à l'historique
        self.history_listbox.insert(tk.END, result_message)  # Affiche le résultat dans la liste

    def show_archives(self):
        """
        Affiche une fenêtre séparée contenant les éléments archivés.
        Permet à l'utilisateur de consulter les conversions archivées.
        """
        archive_window = tk.Toplevel(self.root)  # Crée une nouvelle fenêtre
        archive_window.title("Archives")  # Définit le titre de la fenêtre
        
        archive_listbox = tk.Listbox(archive_window)  # Crée une liste pour afficher les archives
        archive_listbox.pack(fill=tk.BOTH, expand=True)  # Ajuste la taille pour occuper l'espace disponible
        
        for item in self.archived:  # Parcourt les archives
            archive_listbox.insert(tk.END, item)  # Ajoute chaque élément dans la liste
        
        # Lier un double-clic pour restaurer un élément archivé
        archive_listbox.bind('<Double-1>', self.restore_archive)

    def show_deleted(self):
        """
        Affiche une fenêtre séparée contenant les éléments supprimés.
        Permet à l'utilisateur de consulter et de restaurer les conversions supprimées.
        """
        deleted_window = tk.Toplevel(self.root)  # Crée une nouvelle fenêtre
        deleted_window.title("Corbeille")  # Définit le titre de la fenêtre
        
        deleted_listbox = tk.Listbox(deleted_window)  # Crée une liste pour afficher les éléments supprimés
        deleted_listbox.pack(fill=tk.BOTH, expand=True)  # Ajuste la taille pour occuper l'espace disponible
        
        for item in self.deleted:  # Parcourt les éléments supprimés
            deleted_listbox.insert(tk.END, item)  # Ajoute chaque élément dans la liste
        
        # Lier un double-clic pour restaurer un élément supprimé
        deleted_listbox.bind('<Double-1>', self.restore_deleted)

    def archive_or_delete(self, event):
        """
        Permet d'archiver ou de supprimer un élément sélectionné dans l'historique.
        L'utilisateur choisit l'action via une boîte de dialogue.
        """
        selected_index = self.history_listbox.curselection()  # Récupère l'index de l'élément sélectionné
        if not selected_index:  # Si aucun élément n'est sélectionné, ne rien faire
            return
        
        selected_item = self.history[selected_index[0]]  # Récupère l'élément sélectionné
        
        # Demande à l'utilisateur de choisir entre archiver et supprimer
        response = messagebox.askquestion("Action", 
            f"Voulez-vous archiver ou supprimer cet élément?\n\n(OUI = ARCHIVER et NON = SUPPRIMER)\n\n{selected_item}")
        
        if response == 'yes':  # Si l'utilisateur choisit "archiver"
            self.archived.append(selected_item)  # Ajoute l'élément aux archives
            self.history_listbox.delete(selected_index)  # Supprime l'élément de l'affichage
            self.history.remove(selected_item)  # Supprime l'élément de l'historique
            messagebox.showinfo("Info", "Élément archivé.")  # Affiche une confirmation
        else:  # Si l'utilisateur choisit "supprimer"
            self.deleted.append(selected_item)  # Ajoute l'élément à la corbeille
            self.history_listbox.delete(selected_index)  # Supprime l'élément de l'affichage
            self.history.remove(selected_item)  # Supprime l'élément de l'historique
            messagebox.showinfo("Info", "Élément supprimé.")  # Affiche une confirmation

    def restore_archive(self, event):
        """
        Restaure un élément sélectionné des archives vers l'historique.
        """
        selected_index = event.widget.curselection()  # Récupère l'index de l'élément sélectionné
        if not selected_index:  # Si aucun élément n'est sélectionné, ne rien faire
            return
        
        selected_item = event.widget.get(selected_index)  # Récupère l'élément sélectionné
        self.archived.remove(selected_item)  # Supprime l'élément des archives
        self.history.append(selected_item)  # Ajoute l'élément à l'historique
        self.history_listbox.insert(tk.END, selected_item) 
        # Ajoute l'élément à la liste de l'affichage
        messagebox.showinfo("Info", "Élément restauré des archives.")  # Affiche une confirmation

    def restore_deleted(self, event):
        """
        Restaure un élément sélectionné de la corbeille vers l'historique.
        """
        selected_index = event.widget.curselection()  # Récupère l'index de l'élément sélectionné
        if not selected_index:  # Si aucun élément n'est sélectionné, ne rien faire
            return
        
        selected_item = event.widget.get(selected_index)  # Récupère l'élément sélectionné
        self.deleted.remove(selected_item)  # Supprime l'élément de la corbeille
        self.history.append(selected_item)  # Ajoute l'élément à l'historique
        self.history_listbox.insert(tk.END, selected_item)  # Ajoute l'élément à la liste de l'affichage
        messagebox.showinfo("Info", "Élément restauré de la corbeille.")  # Affiche une confirmation


if __name__ == "__main__":
    # Point d'entrée principal du programme
    root = tk.Tk()  # Crée la fenêtre principale
    app = CurrencyConverterApp(root)  # Instancie l'application
    root.mainloop()  # Démarre la boucle principale de l'application