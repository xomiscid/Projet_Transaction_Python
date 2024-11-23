import tkinter as tk

class ThemeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Theme Switcher")
        self.root.geometry("400x300")
        
        # Initialize theme state
        self.is_dark = False
        
        # Create label
        self.label = tk.Label(self.root, text="Welcome to Light Mode")
        self.label.pack(pady=20)
        
        # Create toggle button
        self.toggle_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_mode)
        self.toggle_button.pack(pady=20)
        
        # Apply initial light mode
        self.apply_light_mode()
    
    def toggle_mode(self):
        if self.is_dark:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
    
    def apply_dark_mode(self):
        self.root.configure(bg='black')
        self.label.configure(bg='black', fg='white', text="Welcome to Dark Mode")
        self.toggle_button.configure(bg='gray', fg='white')
        self.is_dark = True
    
    def apply_light_mode(self):
        self.root.configure(bg='white')
        self.label.configure(bg='white', fg='black', text="Welcome to Light Mode")
        self.toggle_button.configure(bg='lightgray', fg='black')
        self.is_dark = False
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemeApp()
    app.run()
