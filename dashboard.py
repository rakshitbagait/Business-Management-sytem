import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
from datetime import datetime, timedelta

class Dashboard:
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
        title_label = ttk.Label(container, text="📊 Dashboard",
                              font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create metrics frame
        self.metrics_frame = ttk.Frame(container)
        self.metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create charts frame
        self.charts_frame = ttk.Frame(container)
        self.charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize components
        self.init_metrics()
        self.init_charts()
        
        # Load data
        self.load_data()
    
    def init_metrics(self):
        """Initialize metrics display"""
        # Create metrics grid
        metrics = [
            ("💰 Total Sales", "0"),
            ("📦 Total Products", "0"),
            ("👥 Total Customers", "0"),
            ("👨‍💼 Total Employees", "0"),
            ("🏭 Total Suppliers", "0"),
            ("💵 Total Revenue", "0"),
            ("📈 Growth Rate", "0%"),
            ("📊 Profit Margin", "0%")
        ]
        
        for i, (label, value) in enumerate(metrics):
            metric_frame = ttk.Frame(self.metrics_frame)
            metric_frame.pack(side=tk.LEFT, expand=True, padx=5)
            
            ttk.Label(metric_frame, text=label,
                     font=('Helvetica', 12)).pack()
            ttk.Label(metric_frame, text=value,
                     font=('Helvetica', 20, 'bold')).pack()
    
    def init_charts(self):
        """Initialize charts"""
        # Create figure for charts
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def load_data(self):
        """Load and display dashboard data"""
        try:
            # Get total sales
            self.cursor.execute("SELECT COUNT(*) FROM sales")
            total_sales = self.cursor.fetchone()[0]
            
            # Get total products
            self.cursor.execute("SELECT COUNT(*) FROM products")
            total_products = self.cursor.fetchone()[0]
            
            # Get total customers
            self.cursor.execute("SELECT COUNT(*) FROM customers")
            total_customers = self.cursor.fetchone()[0]
            
            # Get total employees
            self.cursor.execute("SELECT COUNT(*) FROM employees")
            total_employees = self.cursor.fetchone()[0]
            
            # Get total suppliers
            self.cursor.execute("SELECT COUNT(*) FROM suppliers")
            total_suppliers = self.cursor.fetchone()[0]
            
            # Get total revenue
            self.cursor.execute("SELECT SUM(total_amount) FROM sales")
            total_revenue = self.cursor.fetchone()[0] or 0
            
            # Calculate growth rate (example)
            growth_rate = random.uniform(5, 15)
            
            # Calculate profit margin (example)
            profit_margin = random.uniform(20, 30)
            
            # Update metrics
            metrics = [
                (f"💰 Total Sales", f"{total_sales:,}"),
                (f"📦 Total Products", f"{total_products:,}"),
                (f"👥 Total Customers", f"{total_customers:,}"),
                (f"👨‍💼 Total Employees", f"{total_employees:,}"),
                (f"🏭 Total Suppliers", f"{total_suppliers:,}"),
                (f"💵 Total Revenue", f"${total_revenue:,.2f}"),
                (f"📈 Growth Rate", f"{growth_rate:.1f}%"),
                (f"📊 Profit Margin", f"{profit_margin:.1f}%")
            ]
            
            for widget in self.metrics_frame.winfo_children():
                widget.destroy()
            
            for label, value in metrics:
                metric_frame = ttk.Frame(self.metrics_frame)
                metric_frame.pack(side=tk.LEFT, expand=True, padx=5)
                
                ttk.Label(metric_frame, text=label,
                         font=('Helvetica', 12)).pack()
                ttk.Label(metric_frame, text=value,
                         font=('Helvetica', 20, 'bold')).pack()
            
            # Update charts
            self.update_charts()
            
        except Exception as e:
            print(f"Error loading dashboard data: {str(e)}")
    
    def update_charts(self):
        """Update dashboard charts"""
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Generate sample data for charts
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                    for i in range(7)]
            sales_data = [random.randint(1000, 5000) for _ in range(7)]
            revenue_data = [random.randint(5000, 15000) for _ in range(7)]
            
            # Plot sales trend
            self.ax1.plot(dates, sales_data, marker='o',
                         color=self.colors['primary'])
            self.ax1.set_title('📈 Sales Trend')
            self.ax1.set_xlabel('Date')
            self.ax1.set_ylabel('Number of Sales')
            self.ax1.tick_params(axis='x', rotation=45)
            
            # Plot revenue trend
            self.ax2.plot(dates, revenue_data, marker='o',
                         color=self.colors['success'])
            self.ax2.set_title('💰 Revenue Trend')
            self.ax2.set_xlabel('Date')
            self.ax2.set_ylabel('Revenue ($)')
            self.ax2.tick_params(axis='x', rotation=45)
            
            # Adjust layout and display
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating charts: {str(e)}") 