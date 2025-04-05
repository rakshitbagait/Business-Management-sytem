import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Suppliers:
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
        title_label = ttk.Label(container, text="🏭 Supplier Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for supplier list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for supplier details
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_supplier_list(left_frame)
        self.init_supplier_details(right_frame)
        
        # Load initial data
        self.load_suppliers()
    
    def init_supplier_list(self, parent):
        """Initialize supplier list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Add search button
        ttk.Button(search_frame, text="Search",
                  command=self.search_suppliers).pack(side=tk.LEFT, padx=5)
        
        # Supplier list
        self.supplier_tree = ttk.Treeview(parent, columns=("ID", "Name", "Contact", "Email", "Status"),
                                       show="headings")
        
        # Configure columns
        self.supplier_tree.heading("ID", text="ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Contact", text="Contact")
        self.supplier_tree.heading("Email", text="Email")
        self.supplier_tree.heading("Status", text="Status")
        
        # Set column widths
        self.supplier_tree.column("ID", width=50)
        self.supplier_tree.column("Name", width=150)
        self.supplier_tree.column("Contact", width=100)
        self.supplier_tree.column("Email", width=200)
        self.supplier_tree.column("Status", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.supplier_tree.yview)
        self.supplier_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.supplier_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.supplier_tree.bind('<<TreeviewSelect>>', self.on_supplier_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ Add Supplier",
                  command=self.show_add_supplier).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Supplier",
                  command=self.show_edit_supplier).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Supplier",
                  command=self.delete_supplier).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_suppliers())
    
    def init_supplier_details(self, parent):
        """Initialize supplier details form"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Supplier Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Supplier ID
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
        
        # Contact Person
        contact_frame = ttk.Frame(details_frame)
        contact_frame.pack(fill=tk.X, pady=5)
        ttk.Label(contact_frame, text="Contact Person:").pack(side=tk.LEFT)
        self.contact_entry = ttk.Entry(contact_frame)
        self.contact_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
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
        
        # Status
        status_frame = ttk.Frame(details_frame)
        status_frame.pack(fill=tk.X, pady=5)
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                  values=["Active", "Inactive", "Pending"])
        status_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Address
        address_frame = ttk.Frame(details_frame)
        address_frame.pack(fill=tk.X, pady=5)
        ttk.Label(address_frame, text="Address:").pack(side=tk.LEFT)
        self.address_text = tk.Text(address_frame, height=4)
        self.address_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Payment Terms
        payment_frame = ttk.Frame(details_frame)
        payment_frame.pack(fill=tk.X, pady=5)
        ttk.Label(payment_frame, text="Payment Terms:").pack(side=tk.LEFT)
        self.payment_entry = ttk.Entry(payment_frame)
        self.payment_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Notes
        notes_frame = ttk.Frame(details_frame)
        notes_frame.pack(fill=tk.X, pady=5)
        ttk.Label(notes_frame, text="Notes:").pack(side=tk.LEFT)
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_supplier).pack(fill=tk.X, pady=10)
    
    def load_suppliers(self):
        """Load suppliers from database"""
        try:
            # Clear existing items
            for item in self.supplier_tree.get_children():
                self.supplier_tree.delete(item)
            
            # Get suppliers from database
            self.cursor.execute("""
                SELECT id, name, contact_person, email, status
                FROM suppliers
                ORDER BY name
            """)
            
            # Add suppliers to treeview
            for supplier in self.cursor.fetchall():
                self.supplier_tree.insert("", tk.END, values=supplier)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load suppliers: {str(e)}")
    
    def on_supplier_select(self, event):
        """Handle supplier selection"""
        selection = self.supplier_tree.selection()
        if not selection:
            return
        
        # Get selected supplier ID
        supplier_id = self.supplier_tree.item(selection[0])['values'][0]
        
        # Get supplier details from database
        self.cursor.execute("""
            SELECT id, name, contact_person, email, phone, status,
                   address, payment_terms, notes
            FROM suppliers
            WHERE id = ?
        """, (supplier_id,))
        
        supplier = self.cursor.fetchone()
        if supplier:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(supplier[0]))
            self.id_entry.configure(state='readonly')
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, supplier[1])
            
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, supplier[2])
            
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, supplier[3])
            
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, supplier[4])
            
            self.status_var.set(supplier[5])
            
            self.address_text.delete('1.0', tk.END)
            self.address_text.insert('1.0', supplier[6] or '')
            
            self.payment_entry.delete(0, tk.END)
            self.payment_entry.insert(0, supplier[7] or '')
            
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', supplier[8] or '')
    
    def show_add_supplier(self):
        """Show add supplier form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.status_var.set("Active")
        self.address_text.delete('1.0', tk.END)
        self.payment_entry.delete(0, tk.END)
        self.notes_text.delete('1.0', tk.END)
    
    def show_edit_supplier(self):
        """Show edit supplier form"""
        selection = self.supplier_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to edit")
            return
    
    def save_supplier(self):
        """Save supplier changes"""
        try:
            # Get form values
            supplier_id = self.id_entry.get()
            name = self.name_entry.get()
            contact = self.contact_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            status = self.status_var.get()
            address = self.address_text.get('1.0', tk.END).strip()
            payment = self.payment_entry.get()
            notes = self.notes_text.get('1.0', tk.END).strip()
            
            # Validate inputs
            if not all([name, contact, email, phone, status]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Validate email format
            if '@' not in email or '.' not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            if supplier_id:  # Update existing supplier
                self.cursor.execute("""
                    UPDATE suppliers
                    SET name = ?, contact_person = ?, email = ?, phone = ?,
                        status = ?, address = ?, payment_terms = ?, notes = ?
                    WHERE id = ?
                """, (name, contact, email, phone, status, address,
                      payment, notes, supplier_id))
            else:  # Add new supplier
                self.cursor.execute("""
                    INSERT INTO suppliers (name, contact_person, email, phone,
                                         status, address, payment_terms, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, contact, email, phone, status, address,
                      payment, notes))
            
            self.conn.commit()
            self.load_suppliers()
            messagebox.showinfo("Success", "Supplier saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save supplier: {str(e)}")
    
    def delete_supplier(self):
        """Delete selected supplier"""
        selection = self.supplier_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this supplier?"):
            try:
                supplier_id = self.supplier_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
                self.conn.commit()
                
                self.load_suppliers()
                messagebox.showinfo("Success", "Supplier deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete supplier: {str(e)}")
    
    def search_suppliers(self):
        """Search suppliers and highlight matches"""
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.supplier_tree.get_children():
            self.supplier_tree.delete(item)
        
        try:
            # Get all suppliers
            self.cursor.execute("""
                SELECT id, name, contact_person, email, status
                FROM suppliers
                ORDER BY name
            """)
            
            # Add suppliers to treeview with highlighting
            for supplier in self.cursor.fetchall():
                # Convert all values to strings for case-insensitive search
                values = [str(val) for val in supplier]
                
                # Check if any field contains the search term
                if search_term in ' '.join(values).lower():
                    # Insert with tag for highlighting
                    item = self.supplier_tree.insert("", tk.END, values=values, tags=('highlight',))
                else:
                    # Insert without highlighting
                    self.supplier_tree.insert("", tk.END, values=values)
            
            # Configure tag for highlighting
            self.supplier_tree.tag_configure('highlight', background='#FFE5B4')  # Light orange background
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search suppliers: {str(e)}") 