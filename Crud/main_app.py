# main_app.py
import customtkinter as ctk
from database_manager import DatabaseManager
from sales_ui import SalesApp

# --- Database Configuration ---
DB_CONFIG = {
    "host": "localhost",
    "database": "qsdbt",
    "user": "python_user",
    "password": "1234",
    "port": "5432" 
}

if __name__ == "__main__":
    #Themes
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("green")  # Themes: "blue" (default), "dark-blue", "green"

    # Initialize the Database Manager
    db_manager = DatabaseManager(DB_CONFIG)

    # Initialize and run the Sales Application
    app = SalesApp(db_manager)
    app.mainloop()