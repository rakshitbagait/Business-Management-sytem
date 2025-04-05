import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Inventory:
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
        title_label = ttk.Label(container, text="📦 Inventory Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for product list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for product details
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_product_list(left_frame)
        self.init_product_details(right_frame)
        
        # Load initial data
        self.load_products()
    
    def init_product_list(self, parent):
        """Initialize product list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Add search button
        ttk.Button(search_frame, text="Search",
                  command=self.search_products).pack(side=tk.LEFT, padx=5)
        
        # Product list
        self.product_tree = ttk.Treeview(parent, columns=("ID", "Name", "Category", "Stock", "Price"),
                                       show="headings")
        
        # Configure columns
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Stock", text="Stock")
        self.product_tree.heading("Price", text="Price")
        
        # Set column widths
        self.product_tree.column("ID", width=50)
        self.product_tree.column("Name", width=200)
        self.product_tree.column("Category", width=100)
        self.product_tree.column("Stock", width=80)
        self.product_tree.column("Price", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ Add Product",
                  command=self.show_add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Product",
                  command=self.show_edit_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Product",
                  command=self.delete_product).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.search_products())
    
    def init_product_details(self, parent):
        """Initialize product details form"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Product Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product ID
        id_frame = ttk.Frame(details_frame)
        id_frame.pack(fill=tk.X, pady=5)
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        self.id_entry = ttk.Entry(id_frame, state='readonly')
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Product Name
        name_frame = ttk.Frame(details_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Category
        category_frame = ttk.Frame(details_frame)
        category_frame.pack(fill=tk.X, pady=5)
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(category_frame)
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Stock
        stock_frame = ttk.Frame(details_frame)
        stock_frame.pack(fill=tk.X, pady=5)
        ttk.Label(stock_frame, text="Stock:").pack(side=tk.LEFT)
        self.stock_entry = ttk.Entry(stock_frame)
        self.stock_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Price
        price_frame = ttk.Frame(details_frame)
        price_frame.pack(fill=tk.X, pady=5)
        ttk.Label(price_frame, text="Price:").pack(side=tk.LEFT)
        self.price_entry = ttk.Entry(price_frame)
        self.price_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Description
        desc_frame = ttk.Frame(details_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(desc_frame, text="Description:").pack(side=tk.LEFT)
        self.desc_text = tk.Text(desc_frame, height=4)
        self.desc_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_product).pack(fill=tk.X, pady=10)
    
    def load_products(self):
        """Load products from database"""
        try:
            # Clear existing items
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
            
            # Get products from database
            self.cursor.execute("""
                SELECT id, name, category, stock, price
                FROM products
                ORDER BY name
            """)
            
            # Add products to treeview
            for product in self.cursor.fetchall():
                self.product_tree.insert("", tk.END, values=product)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.product_tree.selection()
        if not selection:
            return
        
        # Get selected product ID
        product_id = self.product_tree.item(selection[0])['values'][0]
        
        # Get product details from database
        self.cursor.execute("""
            SELECT id, name, category, stock, price, description
            FROM products
            WHERE id = ?
        """, (product_id,))
        
        product = self.cursor.fetchone()
        if product:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(product[0]))
            self.id_entry.configure(state='readonly')
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, product[1])
            
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, product[2])
            
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, str(product[3]))
            
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(product[4]))
            
            self.desc_text.delete('1.0', tk.END)
            self.desc_text.insert('1.0', product[5] or '')
    
    def show_add_product(self):
        """Show add product form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.desc_text.delete('1.0', tk.END)
    
    def show_edit_product(self):
        """Show edit product form"""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
    
    def save_product(self):
        """Save product changes"""
        try:
            # Get form values
            product_id = self.id_entry.get()
            name = self.name_entry.get()
            category = self.category_entry.get()
            stock = self.stock_entry.get()
            price = self.price_entry.get()
            description = self.desc_text.get('1.0', tk.END).strip()
            
            # Validate inputs
            if not all([name, category, stock, price]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            try:
                stock = int(stock)
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Invalid stock or price value")
                return
            
            if product_id:  # Update existing product
                self.cursor.execute("""
                    UPDATE products
                    SET name = ?, category = ?, stock = ?, price = ?, description = ?
                    WHERE id = ?
                """, (name, category, stock, price, description, product_id))
            else:  # Add new product
                self.cursor.execute("""
                    INSERT INTO products (name, category, stock, price, description)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, category, stock, price, description))
            
            self.conn.commit()
            self.load_products()
            messagebox.showinfo("Success", "Product saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {str(e)}")
    
    def delete_product(self):
        """Delete selected product"""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            try:
                product_id = self.product_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                self.conn.commit()
                
                self.load_products()
                messagebox.showinfo("Success", "Product deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
    
    def search_products(self):
        """Search products and highlight matches"""
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        try:
            # Get all products
            self.cursor.execute("""
                SELECT id, name, category, stock, price
                FROM products
                ORDER BY name
            """)
            
            # Add products to treeview with highlighting
            for product in self.cursor.fetchall():
                # Convert all values to strings for case-insensitive search
                values = [str(val) for val in product]
                
                # Check if any field contains the search term
                if search_term in ' '.join(values).lower():
                    # Insert with tag for highlighting
                    item = self.product_tree.insert("", tk.END, values=values, tags=('highlight',))
                else:
                    # Insert without highlighting
                    self.product_tree.insert("", tk.END, values=values)
            
            # Configure tag for highlighting
            self.product_tree.tag_configure('highlight', background='#FFE5B4')  # Light orange background
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search products: {str(e)}") 