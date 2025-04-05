import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Employees:
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
        title_label = ttk.Label(container, text="👨‍💼 Employee Management",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left frame for employee list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create right frame for employee details
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_employee_list(left_frame)
        self.init_employee_details(right_frame)
        
        # Load initial data
        self.load_employees()
    
    def init_employee_list(self, parent):
        """Initialize employee list view"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Employee list
        self.employee_tree = ttk.Treeview(parent, columns=("ID", "Name", "Position", "Department", "Status"),
                                       show="headings")
        
        # Configure columns
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Position", text="Position")
        self.employee_tree.heading("Department", text="Department")
        self.employee_tree.heading("Status", text="Status")
        
        # Set column widths
        self.employee_tree.column("ID", width=50)
        self.employee_tree.column("Name", width=150)
        self.employee_tree.column("Position", width=100)
        self.employee_tree.column("Department", width=100)
        self.employee_tree.column("Status", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.employee_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.employee_tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="➕ Add Employee",
                  command=self.show_add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📝 Edit Employee",
                  command=self.show_edit_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Employee",
                  command=self.delete_employee).pack(side=tk.LEFT, padx=5)
    
    def init_employee_details(self, parent):
        """Initialize employee details form"""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Employee Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Employee ID
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
        
        # Position
        position_frame = ttk.Frame(details_frame)
        position_frame.pack(fill=tk.X, pady=5)
        ttk.Label(position_frame, text="Position:").pack(side=tk.LEFT)
        self.position_entry = ttk.Entry(position_frame)
        self.position_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Department
        department_frame = ttk.Frame(details_frame)
        department_frame.pack(fill=tk.X, pady=5)
        ttk.Label(department_frame, text="Department:").pack(side=tk.LEFT)
        self.department_entry = ttk.Entry(department_frame)
        self.department_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Status
        status_frame = ttk.Frame(details_frame)
        status_frame.pack(fill=tk.X, pady=5)
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                  values=["Active", "On Leave", "Terminated"])
        status_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
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
        
        # Address
        address_frame = ttk.Frame(details_frame)
        address_frame.pack(fill=tk.X, pady=5)
        ttk.Label(address_frame, text="Address:").pack(side=tk.LEFT)
        self.address_text = tk.Text(address_frame, height=4)
        self.address_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Hire Date
        hire_date_frame = ttk.Frame(details_frame)
        hire_date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(hire_date_frame, text="Hire Date:").pack(side=tk.LEFT)
        self.hire_date_entry = ttk.Entry(hire_date_frame)
        self.hire_date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Salary
        salary_frame = ttk.Frame(details_frame)
        salary_frame.pack(fill=tk.X, pady=5)
        ttk.Label(salary_frame, text="Salary:").pack(side=tk.LEFT)
        self.salary_entry = ttk.Entry(salary_frame)
        self.salary_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Notes
        notes_frame = ttk.Frame(details_frame)
        notes_frame.pack(fill=tk.X, pady=5)
        ttk.Label(notes_frame, text="Notes:").pack(side=tk.LEFT)
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Save button
        ttk.Button(details_frame, text="💾 Save Changes",
                  command=self.save_employee).pack(fill=tk.X, pady=10)
    
    def load_employees(self):
        """Load employees from database"""
        try:
            # Clear existing items
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            
            # Get employees from database
            self.cursor.execute("""
                SELECT id, name, position, department, status
                FROM employees
                ORDER BY name
            """)
            
            # Add employees to treeview
            for employee in self.cursor.fetchall():
                self.employee_tree.insert("", tk.END, values=employee)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.employee_tree.selection()
        if not selection:
            return
        
        # Get selected employee ID
        employee_id = self.employee_tree.item(selection[0])['values'][0]
        
        # Get employee details from database
        self.cursor.execute("""
            SELECT id, name, position, department, status, email, phone,
                   hire_date, salary, notes
            FROM employees
            WHERE id = ?
        """, (employee_id,))
        
        employee = self.cursor.fetchone()
        if employee:
            # Update form fields
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(employee[0]))
            self.id_entry.configure(state='readonly')
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, employee[1])
            
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(0, employee[2])
            
            self.department_entry.delete(0, tk.END)
            self.department_entry.insert(0, employee[3])
            
            self.status_var.set(employee[4])
            
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, employee[5])
            
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, employee[6])
            
            self.address_text.delete('1.0', tk.END)
            self.address_text.insert('1.0', employee[7] or '')
            
            self.hire_date_entry.delete(0, tk.END)
            self.hire_date_entry.insert(0, employee[8])
            
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, str(employee[9]))
            
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', employee[10] or '')
    
    def show_add_employee(self):
        """Show add employee form"""
        # Clear form
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.configure(state='readonly')
        
        self.name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.status_var.set("Active")
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_text.delete('1.0', tk.END)
        self.hire_date_entry.delete(0, tk.END)
        self.hire_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.salary_entry.delete(0, tk.END)
        self.notes_text.delete('1.0', tk.END)
    
    def show_edit_employee(self):
        """Show edit employee form"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return
    
    def save_employee(self):
        """Save employee changes"""
        try:
            # Get form values
            employee_id = self.id_entry.get()
            name = self.name_entry.get()
            position = self.position_entry.get()
            department = self.department_entry.get()
            status = self.status_var.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            address = self.address_text.get('1.0', tk.END).strip()
            hire_date = self.hire_date_entry.get()
            salary = self.salary_entry.get()
            notes = self.notes_text.get('1.0', tk.END).strip()
            
            # Validate inputs
            if not all([name, position, department, status, email, phone, hire_date, salary]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Validate email format
            if '@' not in email or '.' not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            try:
                salary = float(salary)
            except ValueError:
                messagebox.showerror("Error", "Invalid salary amount")
                return
            
            if employee_id:  # Update existing employee
                self.cursor.execute("""
                    UPDATE employees
                    SET name = ?, position = ?, department = ?, status = ?,
                        email = ?, phone = ?, address = ?, hire_date = ?, salary = ?, notes = ?
                    WHERE id = ?
                """, (name, position, department, status, email, phone, address,
                      hire_date, salary, notes, employee_id))
            else:  # Add new employee
                self.cursor.execute("""
                    INSERT INTO employees (name, position, department, status,
                                         email, phone, address, hire_date, salary, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, position, department, status, email, phone, address,
                      hire_date, salary, notes))
            
            self.conn.commit()
            self.load_employees()
            messagebox.showinfo("Success", "Employee saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee: {str(e)}")
    
    def delete_employee(self):
        """Delete selected employee"""
        selection = self.employee_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            try:
                employee_id = self.employee_tree.item(selection[0])['values'][0]
                
                self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                self.conn.commit()
                
                self.load_employees()
                messagebox.showinfo("Success", "Employee deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete employee: {str(e)}") 