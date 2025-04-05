import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sv_ttk  # Modern theme for tkinter
from PIL import Image, ImageTk
import os
import sqlite3
from datetime import datetime
import hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random

from dashboard import Dashboard
from inventory import Inventory
from sales import Sales
from customers import Customers
from employees import Employees
from suppliers import Suppliers
from financial import Financial

class RegistrationWindow:
    def __init__(self, parent, db_connection):
        self.window = tk.Toplevel(parent)
        self.window.title("User Registration")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        # Store database connection
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
        # Configure colors
        self.colors = {
            'primary': '#1E88E5',  # Blue
            'secondary': '#FFFFFF',  # White
            'accent': '#64B5F6',  # Light Blue
            'text': '#333333',  # Dark Gray
            'error': '#FF5252',  # Red
            'success': '#4CAF50',  # Green
            'background': '#F5F5F5'  # Light Gray
        }
        
        # Create main container
        container = ttk.Frame(self.window)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(container, text="✨ Create New Account",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(container, text="Please fill in your details to register.",
                                 font=('Helvetica', 12))
        subtitle_label.pack(pady=(0, 30))
        
        # Registration form
        self.create_registration_form(container)
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the registration window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_registration_form(self, parent):
        """Create the registration form"""
        # Form frame
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Username
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill=tk.X, pady=5)
        ttk.Label(username_frame, text="👤 Username").pack(anchor=tk.W)
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Email
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="📧 Email").pack(anchor=tk.W)
        self.email_entry = ttk.Entry(email_frame)
        self.email_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="🔒 Password").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(password_frame, show="•")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm Password
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill=tk.X, pady=5)
        ttk.Label(confirm_frame, text="🔒 Confirm Password").pack(anchor=tk.W)
        self.confirm_entry = ttk.Entry(confirm_frame, show="•")
        self.confirm_entry.pack(fill=tk.X, pady=5)
        
        # Terms and Conditions
        self.terms_var = tk.BooleanVar()
        terms_frame = ttk.Frame(form_frame)
        terms_frame.pack(fill=tk.X, pady=10)
        ttk.Checkbutton(terms_frame, text="I agree to the Terms and Conditions",
                       variable=self.terms_var).pack(anchor=tk.W)
        
        # Register button
        register_btn = ttk.Button(form_frame, text="✨ Register",
                                command=self.register, style='Accent.TButton')
        register_btn.pack(fill=tk.X, pady=20)
        
        # Back to login link
        ttk.Label(form_frame, text="Already have an account? Login",
                 foreground=self.colors['primary'],
                 cursor="hand2").pack(pady=10)
    
    def register(self):
        """Handle user registration"""
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Validate inputs
        if not all([username, email, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not self.terms_var.get():
            messagebox.showerror("Error", "Please agree to the Terms and Conditions")
            return
        
        # Validate email format
        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Validate password strength
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        try:
            # Check if username exists
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Check if email exists
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already exists")
                return
            
            # Hash password using SHA-256
            hashed = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert new user
            self.cursor.execute("""
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            """, (username, hashed, email, 'user'))
            
            self.conn.commit()
            
            # Generate welcome message
            self.generate_welcome_message(username, email)
            
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")
    
    def generate_welcome_message(self, username, email):
        """Generate welcome message for new users"""
        try:
            filename = f"welcome_{username}.txt"
            with open(filename, 'w') as f:
                f.write(f"Welcome to Business Management System, {username}!\n\n")
                f.write("Thank you for joining our platform. Here are your account details:\n")
                f.write(f"Username: {username}\n")
                f.write(f"Email: {email}\n\n")
                f.write("Getting Started:\n")
                f.write("1. Log in to your account\n")
                f.write("2. Explore the dashboard\n")
                f.write("3. Start managing your business\n")
            
        except Exception as e:
            print(f"Failed to generate welcome message: {str(e)}")

class BusinessManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Business Management System")
        self.root.geometry("1200x800")
        
        # Apply modern theme
        sv_ttk.set_theme("light")
        
        # Configure colors
        self.colors = {
            'primary': '#1E88E5',  # Blue
            'secondary': '#FFFFFF',  # White
            'accent': '#64B5F6',  # Light Blue
            'text': '#333333',  # Dark Gray
            'error': '#FF5252',  # Red
            'success': '#4CAF50',  # Green
            'background': '#F5F5F5'  # Light Gray
        }
        
        # Set window background
        self.root.configure(bg=self.colors['background'])
        
        # Initialize database
        self.init_database()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.main_container)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create main menu frame (initially hidden)
        self.menu_frame = ttk.Frame(self.main_container)
        
        # Create content frame (initially hidden)
        self.content_frame = ttk.Frame(self.main_container)
        
        # Initialize UI components
        self.init_login_ui()
        
        # Initialize module instances
        self.current_module = None
        
    def init_database(self):
        """Initialize SQLite database and create necessary tables"""
        self.conn = sqlite3.connect('bms.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                stock INTEGER DEFAULT 0,
                price REAL NOT NULL,
                description TEXT
            );
            
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                items TEXT,
                items_count INTEGER DEFAULT 0,
                total_amount REAL NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                notes TEXT,
                total_purchases INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                department TEXT,
                status TEXT DEFAULT 'Active',
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                hire_date TEXT,
                salary REAL,
                notes TEXT
            );
            
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_person TEXT,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                status TEXT DEFAULT 'Active',
                address TEXT,
                payment_terms TEXT,
                notes TEXT
            );
            
            CREATE TABLE IF NOT EXISTS financial_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            );
        ''')
        
        # Create default admin user if not exists
        self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not self.cursor.fetchone():
            # Simple password hashing using SHA-256
            hashed = hashlib.sha256('admin123'.encode()).hexdigest()
            self.cursor.execute("""
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            """, ('admin', hashed, 'admin@example.com', 'admin'))
        
        self.conn.commit()
    
    def init_login_ui(self):
        """Initialize login interface"""
        # Create main container with shadow effect
        container = ttk.Frame(self.login_frame)
        container.pack(expand=True)
        
        # Create card-like frame
        card = ttk.Frame(container, padding=20)
        card.pack(padx=20, pady=20)
        
        # Title with emoji
        title_label = ttk.Label(card, text="🏢 Business Management System",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(card, text="Welcome back! Please login to your account.",
                                 font=('Helvetica', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Login form frame
        form_frame = ttk.Frame(card)
        form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Username
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill=tk.X, pady=5)
        ttk.Label(username_frame, text="👤 Username").pack(anchor=tk.W)
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Password
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="🔒 Password").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(password_frame, show="•")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Remember me checkbox
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Remember me",
                       variable=self.remember_var).pack(anchor=tk.W, pady=5)
        
        # Forgot password link
        ttk.Label(form_frame, text="Forgot password?",
                 foreground=self.colors['primary'],
                 cursor="hand2").pack(anchor=tk.E, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Login button
        login_btn = ttk.Button(button_frame, text="🚪 Login",
                             command=self.login, style='Accent.TButton')
        login_btn.pack(side=tk.LEFT, expand=True, padx=5)
        
        # Sign up button
        signup_btn = ttk.Button(button_frame, text="✨ Sign Up",
                              command=self.show_registration, style='Accent.TButton')
        signup_btn.pack(side=tk.LEFT, expand=True, padx=5)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Load saved credentials if remember me was checked
        self.load_saved_credentials()
    
    def show_registration(self):
        """Show registration window"""
        RegistrationWindow(self.root, self.conn)
    
    def load_saved_credentials(self):
        """Load saved credentials if they exist"""
        try:
            if os.path.exists('credentials.txt'):
                with open('credentials.txt', 'r') as f:
                    username = f.readline().strip()
                    self.username_entry.insert(0, username)
                    self.remember_var.set(True)
        except Exception:
            pass
    
    def save_credentials(self):
        """Save credentials if remember me is checked"""
        try:
            if self.remember_var.get():
                with open('credentials.txt', 'w') as f:
                    f.write(self.username_entry.get())
            elif os.path.exists('credentials.txt'):
                os.remove('credentials.txt')
        except Exception:
            pass
    
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([username, password]):
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = self.cursor.fetchone()
            
            # Hash password using SHA-256 for comparison
            hashed = hashlib.sha256(password.encode()).hexdigest()
            
            if user and hashed == user[2]:
                # Save credentials if remember me is checked
                self.save_credentials()
                
                self.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'role': user[4]
                }
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def show_main_menu(self):
        """Show main menu after successful login"""
        self.login_frame.pack_forget()
        self.menu_frame.pack(fill=tk.X, padx=5, pady=5)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create menu buttons with emojis
        menu_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📦 Inventory", self.show_inventory),
            ("💰 Sales", self.show_sales),
            ("👥 Customers", self.show_customers),
            ("👨‍💼 Employees", self.show_employees),
            ("🏭 Suppliers", self.show_suppliers),
            ("💵 Financial", self.show_financial),
            ("🚪 Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            ttk.Button(self.menu_frame, text=text,
                      command=command).pack(side=tk.LEFT, padx=5)
    
    def logout(self):
        """Handle logout"""
        self.menu_frame.pack_forget()
        self.content_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        # Clear current module
        if self.current_module:
            self.current_module.frame.pack_forget()
            self.current_module = None
    
    def show_module(self, module_class):
        """Show a module in the content frame"""
        # Clear current module
        if self.current_module:
            self.current_module.frame.pack_forget()
        
        # Create and show new module
        self.current_module = module_class(self.content_frame, self.conn)
        self.current_module.frame.pack(fill=tk.BOTH, expand=True)
    
    def show_dashboard(self):
        """Show dashboard module"""
        self.show_module(Dashboard)
    
    def show_inventory(self):
        """Show inventory module"""
        self.show_module(Inventory)
    
    def show_sales(self):
        """Show sales module"""
        self.show_module(Sales)
    
    def show_customers(self):
        """Show customers module"""
        self.show_module(Customers)
    
    def show_employees(self):
        """Show employees module"""
        self.show_module(Employees)
    
    def show_suppliers(self):
        """Show suppliers module"""
        self.show_module(Suppliers)
    
    def show_financial(self):
        """Show financial module"""
        self.show_module(Financial)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BusinessManagementSystem()
    app.run() 