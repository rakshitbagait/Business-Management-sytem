import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Customers:
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
        title_label = ttk.Label(container, text="👥 Customer Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for customer list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for customer details
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_customer_list(left_frame)
        self.init_customer_details(right_frame)
        
        # Load initial data
        self.load_customers()
    
    def init_customer_list(self, parent):
        """Initialize customer list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Add search button
        ttk.Button(search_frame, text="Search",
                  command=self.search_customers).pack(side=tk.LEFT, padx=5)
        
        # Customer list
        self.customer_tree = ttk.Treeview(parent, columns=("ID", "Name", "Email", "Phone", "Total Purchases"),
                                       show="headings")
        
        # Configure columns
        self.customer_tree.heading("ID", text="ID")
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.heading("Phone", text="Phone")
        self.customer_tree.heading("Total Purchases", text="Total Purchases")
        
        # Set column widths
        self.customer_tree.column("ID", width=50)
        self.customer_tree.column("Name", width=150)
        self.customer_tree.column("Email", width=200)
        self.customer_tree.column("Phone", width=100)
        self.customer_tree.column("Total Purchases", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ Add Customer",
                  command=self.show_add_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Customer",
                  command=self.show_edit_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Customer",
                  command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 Generate Invoice",
                  command=self.generate_invoice).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_customers())
    
    def init_customer_details(self, parent):
        """Initialize customer details form"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Customer Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer ID
        id_frame = ttk.Frame(details_frame)
        id_frame.pack(fill=tk.X, pady=5)
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, state='readonly')
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Name
        name_frame = ttk.Frame(details_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Email
        email_frame = ttk.Frame(details_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="Email:").pack(side=tk.LEFT)
        self.email_entry = ttk.Entry(email_frame)
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Phone
        phone_frame = ttk.Frame(details_frame)
        phone_frame.pack(fill=tk.X, pady=5)
        ttk.Label(phone_frame, text="Phone:").pack(side=tk.LEFT)
        self.phone_entry = ttk.Entry(phone_frame)
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Total Purchases
        total_purchases_frame = ttk.Frame(details_frame)
        total_purchases_frame.pack(fill=tk.X, pady=5)
        ttk.Label(total_purchases_frame, text="Total Purchases:").pack(side=tk.LEFT)
        self.total_purchases_entry = ttk.Entry(total_purchases_frame, state='readonly')
        self.total_purchases_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Address
        address_frame = ttk.Frame(details_frame)
        address_frame.pack(fill=tk.X, pady=5)
        ttk.Label(address_frame, text="Address:").pack(side=tk.LEFT)
        self.address_text = tk.Text(address_frame, height=4)
        self.address_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Notes
        notes_frame = ttk.Frame(details_frame)
        notes_frame.pack(fill=tk.X, pady=5)
        ttk.Label(notes_frame, text="Notes:").pack(side=tk.LEFT)
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_customer).pack(fill=tk.X, pady=10)
    
    def load_customers(self):
        """Load customers from database"""
        try:
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Get customers from database
            self.cursor.execute("""
                SELECT id, name, email, phone, total_purchases
                FROM customers
                ORDER BY name
            """)
            
            # Add customers to treeview
            for customer in self.cursor.fetchall():
                self.customer_tree.insert("", tk.END, values=customer)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def on_customer_select(self, event):
        """Handle customer selection"""
        selection = self.customer_tree.selection()
        if not selection:
            return
        
        # Get selected customer ID
        customer_id = self.customer_tree.item(selection[0])['values'][0]
        
        # Get customer details from database
        self.cursor.execute("""
            SELECT id, name, email, phone, address, notes
            FROM customers
            WHERE id = ?
        """, (customer_id,))
        
        customer = self.cursor.fetchone()
        if customer:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(customer[0]))
            self.id_entry.configure(state='readonly')
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, customer[1])
            
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, customer[2])
            
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, customer[3])
            
            self.total_purchases_entry.delete(0, tk.END)
            self.total_purchases_entry.insert(0, str(customer[4]))
            
            self.address_text.delete('1.0', tk.END)
            self.address_text.insert('1.0', customer[5] or '')
            
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', customer[6] or '')
    
    def show_add_customer(self):
        """Show add customer form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.total_purchases_entry.delete(0, tk.END)
        self.address_text.delete('1.0', tk.END)
        self.notes_text.delete('1.0', tk.END)
    
    def show_edit_customer(self):
        """Show edit customer form"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return
    
    def save_customer(self):
        """Save customer changes"""
        try:
            # Get form values
            customer_id = self.id_entry.get()
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            total_purchases = self.total_purchases_entry.get()
            address = self.address_text.get('1.0', tk.END).strip()
            notes = self.notes_text.get('1.0', tk.END).strip()
            
            # Validate inputs
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Validate email format
            if '@' not in email or '.' not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            if customer_id:  # Update existing customer
                self.cursor.execute("""
                    UPDATE customers
                    SET name = ?, email = ?, phone = ?, total_purchases = ?, address = ?, notes = ?
                    WHERE id = ?
                """, (name, email, phone, total_purchases, address, notes, customer_id))
            else:  # Add new customer
                self.cursor.execute("""
                    INSERT INTO customers (name, email, phone, total_purchases, address, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, email, phone, total_purchases, address, notes))
            
            self.conn.commit()
            self.load_customers()
            messagebox.showinfo("Success", "Customer saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {str(e)}")
    
    def delete_customer(self):
        """Delete selected customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            try:
                customer_id = self.customer_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
                self.conn.commit()
                
                self.load_customers()
                messagebox.showinfo("Success", "Customer deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")
    
    def generate_invoice(self):
        """Generate and send invoice to customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to generate invoice")
            return
        
        try:
            # Get selected customer ID
            customer_id = self.customer_tree.item(selection[0])['values'][0]
            
            # Get customer details
            self.cursor.execute("""
                SELECT name, email, phone, total_purchases
                FROM customers
                WHERE id = ?
            """, (customer_id,))
            
            customer = self.cursor.fetchone()
            if not customer:
                messagebox.showerror("Error", "Customer not found")
                return
            
            name, email, phone, total_purchases = customer
            
            # Get recent sales for this customer
            self.cursor.execute("""
                SELECT date, total_amount
                FROM sales
                WHERE customer_name = ?
                ORDER BY date DESC
                LIMIT 5
            """, (name,))
            
            recent_sales = self.cursor.fetchall()
            
            # Generate invoice content
            invoice_content = f"""
INVOICE
=======
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Invoice #: INV-{datetime.now().strftime('%Y%m%d%H%M%S')}

Customer Details:
---------------
Name: {name}
Email: {email}
Phone: {phone}

Recent Purchases:
---------------
"""
            
            for sale_date, amount in recent_sales:
                invoice_content += f"{sale_date}: ${amount:.2f}\n"
            
            invoice_content += f"""
Total Amount: ${total_purchases:.2f}

Thank you for your business!
===========================
"""
            
            # Save invoice to file
            filename = f"invoice_{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(invoice_content)
            
            # Here you would integrate with an SMS service to send the invoice
            # For now, we'll just show a success message
            messagebox.showinfo("Success", 
                              f"Invoice generated successfully!\nSaved as: {filename}\n\n"
                              f"Note: SMS sending functionality requires integration with an SMS service.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")
    
    def search_customers(self):
        """Search customers and highlight matches"""
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        try:
            # Get all customers
            self.cursor.execute("""
                SELECT id, name, email, phone, total_purchases
                FROM customers
                ORDER BY name
            """)
            
            # Add customers to treeview with highlighting
            for customer in self.cursor.fetchall():
                # Convert all values to strings for case-insensitive search
                values = [str(val) for val in customer]
                
                # Check if any field contains the search term
                if search_term in ' '.join(values).lower():
                    # Insert with tag for highlighting
                    item = self.customer_tree.insert("", tk.END, values=values, tags=('highlight',))
                else:
                    # Insert without highlighting
                    self.customer_tree.insert("", tk.END, values=values)
            
            # Configure tag for highlighting
            self.customer_tree.tag_configure('highlight', background='#FFE5B4')  # Light orange background
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search customers: {str(e)}") 