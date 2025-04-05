import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Sales:
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
        title_label = ttk.Label(container, text="💰 Sales Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for sales list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for sales details and charts
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_sales_list(left_frame)
        self.init_sales_details(right_frame)
        
        # Load initial data
        self.load_sales()
    
    def init_sales_list(self, parent):
        """Initialize sales list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Add search button
        ttk.Button(search_frame, text="Search",
                  command=self.search_sales).pack(side=tk.LEFT, padx=5)
        
        # Sales list
        self.sales_tree = ttk.Treeview(parent, columns=("ID", "Date", "Customer", "Items", "Total"),
                                     show="headings")
        
        # Configure columns
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Customer", text="Customer")
        self.sales_tree.heading("Items", text="Items")
        self.sales_tree.heading("Total", text="Total")
        
        # Set column widths
        self.sales_tree.column("ID", width=50)
        self.sales_tree.column("Date", width=100)
        self.sales_tree.column("Customer", width=150)
        self.sales_tree.column("Items", width=100)
        self.sales_tree.column("Total", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.sales_tree.bind('<<TreeviewSelect>>', self.on_sale_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ New Sale",
                  command=self.show_new_sale).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Sale",
                  command=self.show_edit_sale).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Sale",
                  command=self.delete_sale).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_sales())
    
    def init_sales_details(self, parent):
        """Initialize sales details and charts"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Sale Details", padding=10)
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sale ID
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
        
        # Customer
        customer_frame = ttk.Frame(details_frame)
        customer_frame.pack(fill=tk.X, pady=5)
        ttk.Label(customer_frame, text="Customer:").pack(side=tk.LEFT)
        self.customer_entry = ttk.Entry(customer_frame)
        self.customer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Items
        items_frame = ttk.Frame(details_frame)
        items_frame.pack(fill=tk.X, pady=5)
        ttk.Label(items_frame, text="Items:").pack(side=tk.LEFT)
        self.items_text = tk.Text(items_frame, height=4)
        self.items_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Total
        total_frame = ttk.Frame(details_frame)
        total_frame.pack(fill=tk.X, pady=5)
        ttk.Label(total_frame, text="Total:").pack(side=tk.LEFT)
        self.total_entry = ttk.Entry(total_frame)
        self.total_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_sale).pack(fill=tk.X, pady=10)
        
        # Charts frame
        charts_frame = ttk.LabelFrame(parent, text="Sales Analytics", padding=10)
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create figure for charts
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def load_sales(self):
        """Load sales from database"""
        try:
            # Clear existing items
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
            
            # Get sales from database
            self.cursor.execute("""
                SELECT id, date, customer_name, items_count, total_amount
                FROM sales
                ORDER BY date DESC
            """)
            
            # Add sales to treeview
            for sale in self.cursor.fetchall():
                self.sales_tree.insert("", tk.END, values=sale)
            
            # Update charts
            self.update_charts()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sales: {str(e)}")
    
    def on_sale_select(self, event):
        """Handle sale selection"""
        selection = self.sales_tree.selection()
        if not selection:
            return
        
        # Get selected sale ID
        sale_id = self.sales_tree.item(selection[0])['values'][0]
        
        # Get sale details from database
        self.cursor.execute("""
            SELECT id, date, customer_name, items, total_amount
            FROM sales
            WHERE id = ?
        """, (sale_id,))
        
        sale = self.cursor.fetchone()
        if sale:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(sale[0]))
            self.id_entry.configure(state='readonly')
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, sale[1])
            
            self.customer_entry.delete(0, tk.END)
            self.customer_entry.insert(0, sale[2])
            
            self.items_text.delete('1.0', tk.END)
            self.items_text.insert('1.0', sale[3] or '')
            
            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, str(sale[4]))
    
    def show_new_sale(self):
        """Show new sale form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        self.customer_entry.delete(0, tk.END)
        self.items_text.delete('1.0', tk.END)
        self.total_entry.delete(0, tk.END)
    
    def show_edit_sale(self):
        """Show edit sale form"""
        selection = self.sales_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a sale to edit")
            return
    
    def save_sale(self):
        """Save sale changes"""
        try:
            # Get form values
            sale_id = self.id_entry.get()
            date = self.date_entry.get()
            customer = self.customer_entry.get()
            items = self.items_text.get('1.0', tk.END).strip()
            total = self.total_entry.get()
            
            # Validate inputs
            if not all([date, customer, items, total]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            try:
                total = float(total)
            except ValueError:
                messagebox.showerror("Error", "Invalid total amount")
                return
            
            if sale_id:  # Update existing sale
                self.cursor.execute("""
                    UPDATE sales
                    SET date = ?, customer_name = ?, items = ?, total_amount = ?
                    WHERE id = ?
                """, (date, customer, items, total, sale_id))
            else:  # Add new sale
                self.cursor.execute("""
                    INSERT INTO sales (date, customer_name, items, total_amount)
                    VALUES (?, ?, ?, ?)
                """, (date, customer, items, total))
            
            self.conn.commit()
            self.load_sales()
            messagebox.showinfo("Success", "Sale saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sale: {str(e)}")
    
    def delete_sale(self):
        """Delete selected sale"""
        selection = self.sales_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a sale to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this sale?"):
            try:
                sale_id = self.sales_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
                self.conn.commit()
                
                self.load_sales()
                messagebox.showinfo("Success", "Sale deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete sale: {str(e)}")
    
    def update_charts(self):
        """Update sales charts"""
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Get sales data for charts
            self.cursor.execute("""
                SELECT date, total_amount
                FROM sales
                ORDER BY date
                LIMIT 7
            """)
            
            sales_data = self.cursor.fetchall()
            if sales_data:
                dates = [sale[0] for sale in sales_data]
                amounts = [sale[1] for sale in sales_data]
                
                # Plot daily sales
                self.ax1.plot(dates, amounts, marker='o',
                            color=self.colors['primary'])
                self.ax1.set_title('📈 Daily Sales')
                self.ax1.set_xlabel('Date')
                self.ax1.set_ylabel('Amount ($)')
                self.ax1.tick_params(axis='x', rotation=45)
                
                # Plot sales distribution
                self.ax2.pie(amounts, labels=dates, autopct='%1.1f%%',
                           colors=[self.colors['primary'], self.colors['accent'],
                                 self.colors['success']])
                self.ax2.set_title('💰 Sales Distribution')
            
            # Adjust layout and display
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating charts: {str(e)}")
    
    def search_sales(self):
        """Search sales and highlight matches"""
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        try:
            # Get all sales
            self.cursor.execute("""
                SELECT id, date, customer_name, items_count, total_amount
                FROM sales
                ORDER BY date DESC
            """)
            
            # Add sales to treeview with highlighting
            for sale in self.cursor.fetchall():
                # Convert all values to strings for case-insensitive search
                values = [str(val) for val in sale]
                
                # Check if any field contains the search term
                if search_term in ' '.join(values).lower():
                    # Insert with tag for highlighting
                    item = self.sales_tree.insert("", tk.END, values=values, tags=('highlight',))
                else:
                    # Insert without highlighting
                    self.sales_tree.insert("", tk.END, values=values)
            
            # Configure tag for highlighting
            self.sales_tree.tag_configure('highlight', background='#FFE5B4')  # Light orange background
            
            # Update charts
            self.update_charts()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search sales: {str(e)}") 