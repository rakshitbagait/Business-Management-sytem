import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class Financial:
    def __init__(self, parent, db_connection):
        self.frame = ttk.Frame(parent)
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
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(container, text="💵 Financial Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for transaction list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for transaction details and charts
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_transaction_list(left_frame)
        self.init_transaction_details(right_frame)
        
        # Load initial data
        self.load_transactions()
    
    def init_transaction_list(self, parent):
        """Initialize transaction list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Add search button
        ttk.Button(search_frame, text="Search",
                  command=self.search_transactions).pack(side=tk.LEFT, padx=5)
        
        # Transaction list
        self.transaction_tree = ttk.Treeview(parent, columns=("ID", "Date", "Type", "Category", "Amount"),
                                          show="headings")
        
        # Configure columns
        self.transaction_tree.heading("ID", text="ID")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Amount", text="Amount")
        
        # Set column widths
        self.transaction_tree.column("ID", width=50)
        self.transaction_tree.column("Date", width=100)
        self.transaction_tree.column("Type", width=100)
        self.transaction_tree.column("Category", width=150)
        self.transaction_tree.column("Amount", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.transaction_tree.bind('<<TreeviewSelect>>', self.on_transaction_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ New Transaction",
                  command=self.show_new_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Transaction",
                  command=self.show_edit_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Transaction",
                  command=self.delete_transaction).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_transactions())
    
    def init_transaction_details(self, parent):
        """Initialize transaction details and charts"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Transaction Details", padding=10)
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Transaction ID
        id_frame = ttk.Frame(details_frame)
        id_frame.pack(fill=tk.X, pady=5)
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, state='readonly')
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Date
        date_frame = ttk.Frame(details_frame)
        date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT)
        self.date_entry = ttk.Entry(date_frame)
        self.date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Type
        type_frame = ttk.Frame(details_frame)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var,
                                values=["Income", "Expense"])
        type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Category
        category_frame = ttk.Frame(details_frame)
        category_frame.pack(fill=tk.X, pady=5)
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(category_frame)
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Amount
        amount_frame = ttk.Frame(details_frame)
        amount_frame.pack(fill=tk.X, pady=5)
        ttk.Label(amount_frame, text="Amount:").pack(side=tk.LEFT)
        self.amount_entry = ttk.Entry(amount_frame)
        self.amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Description
        desc_frame = ttk.Frame(details_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(desc_frame, text="Description:").pack(side=tk.LEFT)
        self.desc_text = tk.Text(desc_frame, height=4)
        self.desc_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_transaction).pack(fill=tk.X, pady=10)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Financial Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Total Income
        income_frame = ttk.Frame(summary_frame)
        income_frame.pack(fill=tk.X, pady=5)
        ttk.Label(income_frame, text="💰 Total Income:").pack(side=tk.LEFT)
        self.total_income_label = ttk.Label(income_frame, text="$0.00")
        self.total_income_label.pack(side=tk.RIGHT)
        
        # Total Expense
        expense_frame = ttk.Frame(summary_frame)
        expense_frame.pack(fill=tk.X, pady=5)
        ttk.Label(expense_frame, text="💸 Total Expense:").pack(side=tk.LEFT)
        self.total_expense_label = ttk.Label(expense_frame, text="$0.00")
        self.total_expense_label.pack(side=tk.RIGHT)
        
        # Net Profit
        profit_frame = ttk.Frame(summary_frame)
        profit_frame.pack(fill=tk.X, pady=5)
        ttk.Label(profit_frame, text="📈 Net Profit:").pack(side=tk.LEFT)
        self.net_profit_label = ttk.Label(profit_frame, text="$0.00")
        self.net_profit_label.pack(side=tk.RIGHT)
        
        # Charts frame
        charts_frame = ttk.LabelFrame(parent, text="Financial Analytics", padding=10)
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create figure for charts
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def load_transactions(self):
        """Load transactions from database"""
        try:
            # Clear existing items
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Get transactions from database
            self.cursor.execute("""
                SELECT id, date, type, category, amount
                FROM financial_transactions
                ORDER BY date DESC
            """)
            
            # Add transactions to treeview
            for transaction in self.cursor.fetchall():
                self.transaction_tree.insert("", tk.END, values=transaction)
            
            # Update summary and charts
            self.update_summary()
            self.update_charts()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
    
    def on_transaction_select(self, event):
        """Handle transaction selection"""
        selection = self.transaction_tree.selection()
        if not selection:
            return
        
        # Get selected transaction ID
        transaction_id = self.transaction_tree.item(selection[0])['values'][0]
        
        # Get transaction details from database
        self.cursor.execute("""
            SELECT id, date, type, category, amount, description
            FROM financial_transactions
            WHERE id = ?
        """, (transaction_id,))
        
        transaction = self.cursor.fetchone()
        if transaction:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(transaction[0]))
            self.id_entry.configure(state='readonly')
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, transaction[1])
            
            self.type_var.set(transaction[2])
            
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, transaction[3])
            
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, str(transaction[4]))
            
            self.desc_text.delete('1.0', tk.END)
            self.desc_text.insert('1.0', transaction[5] or '')
    
    def show_new_transaction(self):
        """Show add transaction form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        self.type_var.set("Income")
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.desc_text.delete('1.0', tk.END)
    
    def show_edit_transaction(self):
        """Show edit transaction form"""
        selection = self.transaction_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a transaction to edit")
            return
    
    def save_transaction(self):
        """Save transaction changes"""
        try:
            # Get form values
            transaction_id = self.id_entry.get()
            date = self.date_entry.get()
            type_ = self.type_var.get()
            category = self.category_entry.get()
            amount = self.amount_entry.get()
            description = self.desc_text.get('1.0', tk.END).strip()
            
            # Validate inputs
            if not all([date, type_, category, amount]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
                return
            
            if transaction_id:  # Update existing transaction
                self.cursor.execute("""
                    UPDATE financial_transactions
                    SET date = ?, type = ?, category = ?, amount = ?, description = ?
                    WHERE id = ?
                """, (date, type_, category, amount, description, transaction_id))
            else:  # Add new transaction
                self.cursor.execute("""
                    INSERT INTO financial_transactions (date, type, category, amount, description)
                    VALUES (?, ?, ?, ?, ?)
                """, (date, type_, category, amount, description))
            
            self.conn.commit()
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")
    
    def delete_transaction(self):
        """Delete selected transaction"""
        selection = self.transaction_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
            try:
                transaction_id = self.transaction_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM financial_transactions WHERE id = ?", (transaction_id,))
                self.conn.commit()
                
                self.load_transactions()
                messagebox.showinfo("Success", "Transaction deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")
    
    def update_summary(self):
        """Update financial summary"""
        try:
            # Get total income
            self.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM financial_transactions
                WHERE type = 'Income'
            """)
            total_income = self.cursor.fetchone()[0]
            
            # Get total expense
            self.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM financial_transactions
                WHERE type = 'Expense'
            """)
            total_expense = self.cursor.fetchone()[0]
            
            # Calculate net profit
            net_profit = total_income - total_expense
            
            # Update labels
            self.total_income_label.config(text=f"${total_income:,.2f}")
            self.total_expense_label.config(text=f"${total_expense:,.2f}")
            self.net_profit_label.config(text=f"${net_profit:,.2f}")
            
        except Exception as e:
            print(f"Error updating summary: {str(e)}")
    
    def update_charts(self):
        """Update financial charts"""
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Get transaction data for charts
            self.cursor.execute("""
                SELECT date, type, amount
                FROM financial_transactions
                ORDER BY date
                LIMIT 7
            """)
            
            transactions = self.cursor.fetchall()
            if transactions:
                dates = [t[0] for t in transactions]
                income = [t[2] if t[1] == 'Income' else 0 for t in transactions]
                expense = [t[2] if t[1] == 'Expense' else 0 for t in transactions]
                
                # Plot income vs expense
                self.ax1.bar(dates, income, color=self.colors['success'],
                           label='Income', alpha=0.6)
                self.ax1.bar(dates, [-e for e in expense], color=self.colors['error'],
                           label='Expense', alpha=0.6)
                self.ax1.set_title('💰 Income vs Expense')
                self.ax1.set_xlabel('Date')
                self.ax1.set_ylabel('Amount ($)')
                self.ax1.legend()
                self.ax1.tick_params(axis='x', rotation=45)
                
                # Get category distribution
                self.cursor.execute("""
                    SELECT category, SUM(amount)
                    FROM financial_transactions
                    WHERE type = 'Expense'
                    GROUP BY category
                """)
                
                categories = self.cursor.fetchall()
                if categories:
                    cat_names = [c[0] for c in categories]
                    cat_amounts = [c[1] for c in categories]
                    
                    # Plot expense distribution
                    self.ax2.pie(cat_amounts, labels=cat_names, autopct='%1.1f%%',
                               colors=[self.colors['primary'], self.colors['accent'],
                                     self.colors['success']])
                    self.ax2.set_title('💸 Expense Distribution')
            
            # Adjust layout and display
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating charts: {str(e)}")
    
    def search_transactions(self):
        """Search transactions and highlight matches"""
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        try:
            # Get all transactions
            self.cursor.execute("""
                SELECT id, date, type, category, amount
                FROM financial_transactions
                ORDER BY date DESC
            """)
            
            # Add transactions to treeview with highlighting
            for transaction in self.cursor.fetchall():
                # Convert all values to strings for case-insensitive search
                values = [str(val) for val in transaction]
                
                # Check if any field contains the search term
                if search_term in ' '.join(values).lower():
                    # Insert with tag for highlighting
                    item = self.transaction_tree.insert("", tk.END, values=values, tags=('highlight',))
                else:
                    # Insert without highlighting
                    self.transaction_tree.insert("", tk.END, values=values)
            
            # Configure tag for highlighting
            self.transaction_tree.tag_configure('highlight', background='#FFE5B4')  # Light orange background
            
            # Update summary and charts
            self.update_summary()
            self.update_charts()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search transactions: {str(e)}") 