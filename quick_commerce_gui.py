import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
from db_connection import get_connection

# --- UI Configuration Styling ---
BG_COLOR = "#F4F6F9"
SIDEBAR_COLOR = "#2C3E50"
SIDEBAR_TEXT = "#ECF0F1"
BUTTON_DEFAULT = "#34495E"
ACCENT_COLOR = "#3498DB"
CARD_BG = "#FFFFFF"
TEXT_MAIN = "#2C3E50"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_HEADING = ("Helvetica", 14, "bold")
FONT_NORMAL = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")

class QuickCommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Commerce Inventory Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 600)
        
        from db_connection import get_connection

        # Apply custom styles
        self.setup_styles()

        # Initialize Container
        self.main_container = tk.Frame(self.root, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Show Login Screen First
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=FONT_BOLD, background=SIDEBAR_COLOR, foreground="white")
        style.configure("Treeview", font=FONT_NORMAL, rowheight=30, background="white", fieldbackground="white")
        style.map("Treeview", background=[('selected', ACCENT_COLOR)])

    from db_connection import get_connection

    def connect_db(self):
        try:
            return get_connection()
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Cannot connect to database:\n{err}"
            )
            return None

    def clear_container(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    # ==========================
    #       LOGIN SYSTEM
    # ==========================
    def show_login_screen(self):
        self.clear_container(self.main_container)
        
        login_frame = tk.Frame(self.main_container, bg=CARD_BG, padx=40, pady=40, relief=tk.RAISED, borderwidth=2)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(login_frame, text="Quick Commerce Login", font=("Helvetica", 18, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(pady=(0, 20))

        tk.Label(login_frame, text="Username", font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w")
        self.user_entry = tk.Entry(login_frame, font=FONT_NORMAL, width=30)
        self.user_entry.pack(pady=(5, 15), ipady=5)

        tk.Label(login_frame, text="Password", font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w")
        self.pass_entry = tk.Entry(login_frame, show="*", font=FONT_NORMAL, width=30)
        self.pass_entry.pack(pady=(5, 20), ipady=5)

        login_btn = tk.Button(login_frame, text="Login", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white", 
                              width=25, relief=tk.FLAT, command=self.verify_login)
        login_btn.pack(ipady=5)

    def verify_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        if username == "admin" and password == "admin":
            self.show_main_layout()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password.\nHint: admin/admin")

    # ==========================
    #       MAIN LAYOUT
    # ==========================
    def show_main_layout(self):
        self.clear_container(self.main_container)

        # Sidebar
        self.sidebar = tk.Frame(self.main_container, bg=SIDEBAR_COLOR, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        brand_label = tk.Label(self.sidebar, text="Quick\nCommerce", font=("Helvetica", 18, "bold"), 
                               bg=SIDEBAR_COLOR, fg=SIDEBAR_TEXT, pady=30)
        brand_label.pack(fill=tk.X)

        # Main Content Area
        self.content_area = tk.Frame(self.main_container, bg=BG_COLOR)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Navigation Buttons
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Products Management", self.show_products),
            ("Inventory & Alerts", self.show_inventory),
            ("Orders History", self.show_orders),
            ("Place New Order", self.show_place_order),
            ("Logout", self.show_login_screen)         
        ]

        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=text, font=FONT_NORMAL, bg=BUTTON_DEFAULT, fg=SIDEBAR_TEXT,
                            relief=tk.FLAT, anchor="w", padx=20, pady=10, 
                            activebackground=ACCENT_COLOR, activeforeground="white", command=command)
            btn.pack(fill=tk.X, pady=2)

        # Go to default view
        self.show_dashboard()

    # ==========================
    #      HELPER FUNCTIONS
    # ==========================
    def populate_treeview(self, tree, query, params=(), low_stock_highlight=False):
        """
        Executes SELECT queries and displays results in TreeView.

        Parameters:
        - tree: UI table
        - query: SQL query (SELECT)
        - params: tuple for parameterized query
        - low_stock_highlight: highlights rows where stock < 10
        """

        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        conn = self.connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=False)

        try:
            # 🔥 QUERY EXECUTION HAPPENS HERE
            cursor.execute(query, params)
            rows = cursor.fetchall()

            cols = list(cursor.column_names)

            # Setup columns dynamically
            tree["columns"] = cols
            tree["show"] = "headings"

            for col in cols:
                tree.heading(col, text=col.replace("_", " ").title())
                tree.column(col, width=120, anchor=tk.CENTER)

            # Detect stock column index (for highlighting)
            stock_idx = -1
            if low_stock_highlight:
                for i, col_name in enumerate(cols):
                    if "stock" in col_name.lower():
                        stock_idx = i
                        break

            tree.tag_configure("low_stock", background="#FFCDD2")

            # Insert rows
            for row in rows:
                tag = ""
                if low_stock_highlight and stock_idx != -1:
                    try:
                        if float(row[stock_idx]) < 10:
                            tag = "low_stock"
                    except:
                        pass

                tree.insert("", "end", values=row, tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("SQL Error", f"Failed:\n{err}")

        finally:
            conn.close()

    def create_title(self, text):
        title_frame = tk.Frame(self.content_area, bg=BG_COLOR)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        lbl = tk.Label(title_frame, text=text, font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_MAIN)
        lbl.pack(side=tk.LEFT)
        return title_frame

    # ==========================
    #       DASHBOARD VIEW
    # ==========================
    def show_dashboard(self):
        self.clear_container(self.content_area)
        self.create_title("Dashboard Overview")

        cards_frame = tk.Frame(self.content_area, bg=BG_COLOR)
        cards_frame.pack(fill=tk.X, padx=20, pady=10)

        stats = self.get_dashboard_stats()

        self.create_card(cards_frame, "Total Products", stats['products'], 0)
        self.create_card(cards_frame, "Total Orders", stats['orders'], 1)
        self.create_card(cards_frame, "Low Stock Items", stats['low_stock'], 2, bg_color="#E74C3C", fg_color="white")

    def create_card(self, parent, title, value, col, bg_color=CARD_BG, fg_color=TEXT_MAIN):
        card = tk.Frame(parent, bg=bg_color, relief=tk.RIDGE, bd=2, padx=20, pady=20, width=200)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title, font=FONT_NORMAL, bg=bg_color, fg=fg_color).pack()
        tk.Label(card, text=str(value), font=("Helvetica", 24, "bold"), bg=bg_color, fg=fg_color).pack(pady=(10, 0))

    def get_dashboard_stats(self):
        """
        Runs aggregate queries for dashboard cards.
        """
        stats = {'products': 0, 'orders': 0, 'low_stock': 0}

        conn = self.connect_db()
        if not conn:
            return stats

        cursor = conn.cursor()

        try:
            # 🔹 QUERY 1: Total products
            cursor.execute("SELECT COUNT(*) FROM Product")
            stats['products'] = cursor.fetchone()[0]

            # 🔹 QUERY 2: Total orders
            cursor.execute("SELECT COUNT(*) FROM Orders")
            stats['orders'] = cursor.fetchone()[0]

            # 🔹 QUERY 3: Low stock items
            cursor.execute("SELECT COUNT(*) FROM Inventory WHERE stock_quantity < 10")
            stats['low_stock'] = cursor.fetchone()[0]

        except Exception as e:
            print("Dashboard error:", e)

        finally:
            conn.close()

        return stats

    # ==========================
    #       PRODUCTS VIEW
    # ==========================
    def show_products(self):
        self.clear_container(self.content_area)
        top_frame = self.create_title("Manage Products")

        # Top Controls: Search and Add Product
        controls = tk.Frame(self.content_area, bg=BG_COLOR)
        controls.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(controls, text="Search:", font=FONT_NORMAL, bg=BG_COLOR).pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_entry = tk.Entry(controls, textvariable=search_var, font=FONT_NORMAL, width=25)
        search_entry.pack(side=tk.LEFT, padx=5, ipady=4)
        
        btn_search = tk.Button(controls, text="🔍 Search", bg=ACCENT_COLOR, fg="white", font=FONT_BOLD, 
                               relief=tk.FLAT, command=lambda: self.load_products(search_var.get()))
        btn_search.pack(side=tk.LEFT, padx=5, ipady=2)

        btn_add = tk.Button(controls, text="+ Add Product", bg="#2ECC71", fg="white", font=FONT_BOLD,
                            relief=tk.FLAT, command=self.modal_add_product)
        btn_add.pack(side=tk.RIGHT, ipady=2)

        btn_del = tk.Button(controls, text="🗑 Delete Selected", bg="#E74C3C", fg="white", font=FONT_BOLD,
                            relief=tk.FLAT, command=self.delete_product)
        btn_del.pack(side=tk.RIGHT, padx=10, ipady=2)

        # Treeview
        tree_frame = tk.Frame(self.content_area, bg="white", bd=1, relief=tk.SOLID)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.prod_tree = ttk.Treeview(tree_frame, yscrollcommand=scroll_y.set)
        self.prod_tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.prod_tree.yview)

        self.load_products()

    def load_products(self, search_term=""):
        """
        Loads products into table.
        If search term provided → filtered query.
        """

        if search_term:
            # 🔹 QUERY: Search product by name
            query = "SELECT * FROM Product WHERE product_name LIKE %s"
            self.populate_treeview(self.prod_tree, query, (f"%{search_term}%",))
        else:
            # 🔹 QUERY: Fetch all products
            self.populate_treeview(self.prod_tree, "SELECT * FROM Product")

    def modal_add_product(self):
        modal = tk.Toplevel(self.root)
        modal.title("Add New Product")
        modal.geometry("400x450")
        modal.configure(bg=CARD_BG)
        modal.transient(self.root)
        modal.grab_set()

        tk.Label(modal, text="Add Product", font=FONT_HEADING, bg=CARD_BG, fg=TEXT_MAIN).pack(pady=15)
        
        fields = ["Name", "Category ID", "Supplier ID", "Price"]
        entries = {}

        for field in fields:
            frame = tk.Frame(modal, bg=CARD_BG)
            frame.pack(fill=tk.X, padx=30, pady=5)
            tk.Label(frame, text=field, font=FONT_NORMAL, bg=CARD_BG).pack(anchor="w")
            ent = tk.Entry(frame, font=FONT_NORMAL)
            ent.pack(fill=tk.X, ipady=4)
            entries[field] = ent

        def save_product():
            try:
                name = entries["Name"].get().strip()
                cat_id = int(entries["Category ID"].get())
                sup_id = int(entries["Supplier ID"].get())
                price = float(entries["Price"].get())

                if not name: raise ValueError("Name cannot be empty.")

                conn = self.connect_db()
                cursor = conn.cursor()
                # Adapting to typical attributes mentioned: name, category_id, supplier_id, price
                cursor.execute("""
                    INSERT INTO Product
                    (product_name, category_id, supplier_id, price)
                    VALUES (%s,%s,%s,%s)
                """, (name, cat_id, sup_id, price))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Product added successfully!", parent=modal)
                modal.destroy()
                self.load_products()
            except ValueError as ve:
                messagebox.showerror("Input Error", "Please ensure ID and Price are numeric and fields are filled.", parent=modal)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to add \n(Check foreign keys!)\n{err}", parent=modal)

        btn = tk.Button(modal, text="Save Product", bg=ACCENT_COLOR, fg="white", font=FONT_BOLD, 
                        relief=tk.FLAT, command=save_product)
        btn.pack(pady=20, fill=tk.X, padx=30, ipady=5)

    def delete_product(self):
        selected = self.prod_tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a product.")
            return

        item = self.prod_tree.item(selected[0])
        prod_id = item['values'][0]

        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            # 🔥 FIX: removed f-string (was wrong)
            # 🔹 QUERY: Delete product
            cursor.execute("DELETE FROM Product WHERE product_id = %s", (prod_id,))
            conn.commit()

            messagebox.showinfo("Success", "Deleted.")
            self.load_products()

        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Product linked to other tables.")

        finally:
            conn.close()

    # ==========================
    #       INVENTORY VIEW
    # ==========================
    def show_inventory(self):
        self.clear_container(self.content_area)
        self.create_title("Inventory Management (Low Stock Highlighted)")

        controls = tk.Frame(self.content_area, bg=BG_COLOR)
        controls.pack(fill=tk.X, padx=20, pady=(0, 10))

        btn_update = tk.Button(controls, text="Update Stock", bg="#F39C12", fg="white", font=FONT_BOLD,
                            relief=tk.FLAT, command=self.modal_update_inventory)
        btn_update.pack(side=tk.RIGHT, ipady=2)

        tree_frame = tk.Frame(self.content_area, bg="white", bd=1, relief=tk.SOLID)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.inv_tree = ttk.Treeview(tree_frame, yscrollcommand=scroll_y.set)
        self.inv_tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.inv_tree.yview)

        self.load_inventory()

    def load_inventory(self):
        # Highlighting items with <10 stock
        self.populate_treeview(self.inv_tree, "SELECT * FROM Inventory", low_stock_highlight=True)

    def modal_update_inventory(self):
        selected = self.inv_tree.selection()
        
        modal = tk.Toplevel(self.root)
        modal.title("Update Stock")
        modal.geometry("350x250")
        modal.configure(bg=CARD_BG)
        modal.transient(self.root)
        modal.grab_set()

        tk.Label(modal, text="Update Inventory Stock", font=FONT_HEADING, bg=CARD_BG).pack(pady=15)

        tk.Label(modal, text="Inventory ID:", font=FONT_NORMAL, bg=CARD_BG).pack()
        inv_id_var = tk.StringVar()
        ent_id = tk.Entry(modal, textvariable=inv_id_var, font=FONT_NORMAL)
        ent_id.pack(pady=5)

        tk.Label(modal, text="New Stock Quantity:", font=FONT_NORMAL, bg=CARD_BG).pack()
        stock_var = tk.StringVar()
        ent_stock = tk.Entry(modal, textvariable=stock_var, font=FONT_NORMAL)
        ent_stock.pack(pady=5)

        # Pre-fill if item selected
        if selected:
            item = self.inv_tree.item(selected[0])['values']
            inv_id_var.set(str(item[0])) # assuming inv_id is col 0

        def save_stock():
            try:
                iid = int(inv_id_var.get())
                qty = int(stock_var.get())
                
                if qty < 0: raise ValueError("Quantity cannot be negative.")

                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE Inventory SET stock_quantity = %s WHERE inventory_id = %s", (qty, iid))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Stock updated successfully!", parent=modal)
                modal.destroy()
                self.load_inventory()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric IDs and quantities.", parent=modal)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=modal)

        tk.Button(modal, text="Update", bg=ACCENT_COLOR, fg="white", font=FONT_BOLD, 
                  relief=tk.FLAT, command=save_stock).pack(pady=10, fill=tk.X, padx=50)

    # ==========================
    #       ORDERS VIEW
    # ==========================
    def show_orders(self):
        self.clear_container(self.content_area)
        self.create_title("Orders Master List")

        tree_frame = tk.Frame(self.content_area, bg="white", bd=1, relief=tk.SOLID)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.ord_tree = ttk.Treeview(tree_frame, yscrollcommand=scroll_y.set)
        self.ord_tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.ord_tree.yview)

        self.populate_treeview(self.ord_tree, "SELECT * FROM Orders ORDER BY order_id DESC")

    # ==========================
    #      PLACE ORDER TOOL
    # ==========================
    def show_place_order(self):
        self.clear_container(self.content_area)
        self.create_title("Simulate / Place New Order")

        form_frame = tk.Frame(self.content_area, bg=CARD_BG, padx=40, pady=40, bd=1, relief=tk.SOLID)
        form_frame.pack(padx=20, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Select Product ID:", font=FONT_NORMAL, bg=CARD_BG).grid(row=0, column=0, sticky="w", pady=10)
        self.po_prod_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.po_prod_var, font=FONT_NORMAL, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Customer ID:", font=FONT_NORMAL, bg=CARD_BG).grid(row=1, column=0, sticky="w", pady=10)
        self.po_cust_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.po_cust_var, font=FONT_NORMAL, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Quantity:", font=FONT_NORMAL, bg=CARD_BG).grid(row=2, column=0, sticky="w", pady=10)
        self.po_qty_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.po_qty_var, font=FONT_NORMAL, width=30).grid(row=2, column=1, padx=10, pady=10)

        btn_place = tk.Button(form_frame, text="Confirm & Place Order", bg="#27AE60", fg="white", font=FONT_BOLD,
                              relief=tk.FLAT, command=self.process_order)
        btn_place.grid(row=3, column=0, columnspan=2, pady=20, ipadx=20, ipady=5)

        tk.Label(form_frame, text="Note: Stock will be automatically checked and deducted from Inventory.",
                 font=("Helvetica", 10, "italic"), bg=CARD_BG, fg="#7f8c8d").grid(row=4, column=0, columnspan=2)

    def process_order(self):
        """
        Handles full transaction:
        1. Check stock
        2. Insert order
        3. Insert order items
        4. Deduct inventory
        """

        try:
            pid = int(self.po_prod_var.get())
            cid = int(self.po_cust_var.get())
            qty = int(self.po_qty_var.get())

            if qty <= 0:
                raise ValueError

        except:
            messagebox.showerror("Input Error", "Invalid input.")
            return

        conn = self.connect_db()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)

        try:
            # 🔹 QUERY 1: Get inventory rows
            cursor.execute(
                "SELECT inventory_id, stock_quantity FROM Inventory WHERE product_id = %s",
                (pid,)
            )
            inv_records = cursor.fetchall()

            if not inv_records:
                messagebox.showerror("Error", "No inventory found.")
                return

            total_stock = sum(row['stock_quantity'] for row in inv_records)

            if total_stock < qty:
                messagebox.showerror("Stock Error", f"Available: {total_stock}")
                return

            # 🔹 QUERY 2: Get product price
            cursor.execute(
                "SELECT price FROM Product WHERE product_id = %s",
                (pid,)
            )
            prod = cursor.fetchone()

            if not prod:
                messagebox.showerror("Error", "Invalid product.")
                return

            price = prod['price']
            total_amount = price * qty

            # 🔹 QUERY 3: Insert order
            cursor.execute("""
                INSERT INTO Orders (customer_id, order_date, total_amount, order_status)
                VALUES (%s, %s, %s, %s)
            """, (cid, datetime.now(), total_amount, "Shipped"))

            order_id = cursor.lastrowid

            # 🔹 QUERY 4: Insert order items
            cursor.execute("""
                INSERT INTO Order_Items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, pid, qty, price))

            # 🔹 QUERY 5: Update inventory (loop)
            remaining = qty

            for record in inv_records:
                if remaining <= 0:
                    break

                inv_id = record['inventory_id']
                stock = record['stock_quantity']

                deduct = min(stock, remaining)

                cursor.execute(
                    "UPDATE Inventory SET stock_quantity = stock_quantity - %s WHERE inventory_id = %s",
                    (deduct, inv_id)
                )

                remaining -= deduct

            conn.commit()

            messagebox.showinfo("Success", f"Order #{order_id} placed")

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("DB Error", str(err))

        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickCommerceApp(root)
    root.mainloop()
