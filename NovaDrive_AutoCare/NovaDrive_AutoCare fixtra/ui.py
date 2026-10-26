import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import Database
from config import SHOP_NAME, SHOP_TAGLINE

BG = "#0F172A"
PANEL = "#111827"
CARD = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
ACCENT = "#22C55E"
BLUE = "#3B82F6"
ORANGE = "#F59E0B"
RED = "#EF4444"
PURPLE = "#A855F7"
CYAN = "#06B6D4"


class NovaDriveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{SHOP_NAME} | Management System")
        self.geometry("1400x850")
        self.minsize(1100, 700)
        self.configure(bg=BG)
        self.db = Database()
        try:
            self.db.connect()
        except Exception as e:
            messagebox.showerror("MySQL Connection Error",
                                 f"Could not connect to MySQL.\n\n{e}\n\n"
                                 "Check config.py and make sure MySQL Server is running.")
            self.destroy()
            return
        self._styles()
        self._build()
        self.show_dashboard()

    def _styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview", background=CARD, fieldbackground=CARD,
                    foreground=TEXT, rowheight=32, borderwidth=0)
        s.configure("Treeview.Heading", background="#1e2d48",
                    foreground=TEXT, font=("Segoe UI", 10, "bold"), padding=8)
        s.map("Treeview", background=[("selected", "#21466d")])
        s.configure("TButton", font=("Segoe UI", 10, "bold"), padding=9)
        s.configure("Accent.TButton", background=ACCENT, foreground="#07130d")
        s.map("Accent.TButton", background=[("active", "#6bf0ae")])

    def _build(self):
        self.sidebar = tk.Frame(self, bg="#09101d", width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg="#09101d")
        logo.pack(fill="x", padx=22, pady=(28, 24))
        tk.Label(logo, text="F", bg=ACCENT, fg="#07130d",
                 font=("Segoe UI", 22, "bold"), width=2, height=1).pack(side="left")
        tx = tk.Frame(logo, bg="#09101d")
        tx.pack(side="left", padx=10)
        tk.Label(tx, text="FIXTRA", bg="#09101d", fg=TEXT,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(tx, text="AUTOCARE", bg="#09101d", fg=ACCENT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        self.nav = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("◉", "Customers", self.show_customers),
            ("▣", "Vehicles", self.show_vehicles),
            ("⚙", "Service Jobs", self.show_jobs),
            ("◫", "Service Catalog", self.show_catalog),
            ("□", "Inventory", self.show_inventory),
            ("₹", "Billing", self.show_billing),
            ("◷", "Reminders", self.show_reminders),
        ]
        for icon, text, cmd in self.nav:
            b = tk.Button(self.sidebar, text=f"  {icon}   {text}", command=cmd,
                          anchor="w", bd=0, relief="flat", bg="#09101d", fg=MUTED,
                          activebackground="#16253d", activeforeground=TEXT,
                          font=("Segoe UI", 11), padx=20, pady=11)
            b.pack(fill="x", padx=10, pady=2)

        tk.Label(self.sidebar, text="REAL-WORLD SERVICE CONTROL", bg="#09101d",
                 fg="#50627b", font=("Segoe UI", 8, "bold")).pack(side="bottom", pady=25)

        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def header(self, title, subtitle=""):
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", padx=32, pady=(26, 16))
        tk.Label(top, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 24, "bold")).pack(side="left")
        if subtitle:
            tk.Label(top, text=subtitle, bg=BG, fg=MUTED,
                     font=("Segoe UI", 10)).pack(side="left", padx=15, pady=(8,0))
        return top

    def card(self, parent, title, value, color=ACCENT):
        f = tk.Frame(parent, bg=CARD, height=112)
        f.pack_propagate(False)
        tk.Frame(f, bg=color, width=5).pack(side="left", fill="y")
        body = tk.Frame(f, bg=CARD)
        body.pack(fill="both", expand=True, padx=18, pady=14)
        tk.Label(body, text=title.upper(), bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(body, text=str(value), bg=CARD, fg=TEXT,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(6,0))
        return f

    def table(self, parent, columns, widths=None):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, padx=32, pady=8)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for i, c in enumerate(columns):
            tree.heading(c, text=c)
            tree.column(c, width=(widths[i] if widths else 130), anchor="w")
        ys = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=ys.set)
        tree.pack(side="left", fill="both", expand=True)
        ys.pack(side="right", fill="y")
        return tree
        # ==========================================================
        # REVENUE BAR CHART
        # ==========================================================

    def revenue_bar_chart(self, parent):
        box = tk.Frame(
            parent,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground="#26334D"
        )

        box.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            box,
            text="Revenue Overview",
            font=("Segoe UI", 15, "bold"),
            fg=TEXT,
            bg=PANEL
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 2)
        )

        subtitle = tk.Label(
            box,
            text="Last 7 days",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=PANEL
        )

        subtitle.pack(
            anchor="w",
            padx=20
        )

        chart = tk.Canvas(
            box,
            height=280,
            bg=PANEL,
            highlightthickness=0
        )

        chart.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        rows = self.db.query(
            """
            SELECT DATE(paid_at) AS pay_date,
                   COALESCE(SUM(amount), 0) AS revenue
            FROM payments
            WHERE paid_at >= CURDATE() - INTERVAL 6 DAY
            GROUP BY DATE(paid_at)
            ORDER BY pay_date
            """,
            fetch=True
        )

        values = {}

        for r in rows:
            values[str(r["pay_date"])] = float(
                r["revenue"] or 0
            )

        days = []

        for i in range(6, -1, -1):
            d = date.today() - timedelta(days=i)
            days.append(d)

        amounts = [
            values.get(str(d), 0)
            for d in days
        ]

        def draw_chart(event=None):
            chart.delete("all")

            width = chart.winfo_width()
            height = chart.winfo_height()

            if width < 100:
                return

            left = 50
            right = 20
            top = 25
            bottom = 45

            chart_width = width - left - right
            chart_height = height - top - bottom

            max_value = max(amounts) if amounts else 0

            if max_value <= 0:
                max_value = 100

            bar_gap = 15

            bar_width = (
                                chart_width - bar_gap * 8
                        ) / 7

            for i, amount in enumerate(amounts):
                x1 = (
                        left +
                        i * (bar_width + bar_gap)
                )

                x2 = x1 + bar_width

                bar_height = (
                                     amount / max_value
                             ) * chart_height

                y1 = (
                        top +
                        chart_height -
                        bar_height
                )

                y2 = top + chart_height

                chart.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=ACCENT,
                    outline=""
                )

                chart.create_text(
                    (x1 + x2) / 2,
                    y1 - 10,
                    text=f"₹{amount:,.0f}",
                    fill=TEXT,
                    font=("Segoe UI", 8, "bold")
                )

                chart.create_text(
                    (x1 + x2) / 2,
                    y2 + 18,
                    text=days[i].strftime("%a"),
                    fill=MUTED,
                    font=("Segoe UI", 9)
                )

            chart.create_line(
                left,
                top + chart_height,
                width - right,
                top + chart_height,
                fill="#334155"
            )

        chart.bind(
            "<Configure>",
            draw_chart
        )

        return box

    def show_dashboard(self):
        self.clear()

        self.header(
            "Good day 👋",
            "Fixtra AutoCare — Business & Service Dashboard"
        )
        # ==========================================================
        # DASHBOARD SCROLL CONTAINER
        # ==========================================================

        dashboard_area = tk.Frame(
            self.content,
            bg=BG
        )
        dashboard_area.pack(
            fill="both",
            expand=True
        )

        dashboard_canvas = tk.Canvas(
            dashboard_area,
            bg=BG,
            highlightthickness=0
        )

        dashboard_scrollbar = ttk.Scrollbar(
            dashboard_area,
            orient="vertical",
            command=dashboard_canvas.yview
        )

        dashboard_frame = tk.Frame(
            dashboard_canvas,
            bg=BG
        )

        dashboard_frame.bind(
            "<Configure>",
            lambda e: dashboard_canvas.configure(
                scrollregion=dashboard_canvas.bbox("all")
            )
        )

        dashboard_canvas.create_window(
            (0, 0),
            window=dashboard_frame,
            anchor="nw"
        )

        dashboard_canvas.configure(
            yscrollcommand=dashboard_scrollbar.set
        )

        dashboard_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        dashboard_scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================================================
        # TOP STAT CARDS
        # ==========================================================

        stats = tk.Frame(dashboard_frame, bg=BG)
        stats.pack(fill="x", padx=32, pady=(0, 15))

        active_jobs = self.db.scalar("""
            SELECT COUNT(*)
            FROM service_jobs
            WHERE status IN ('Booked','In Progress','Waiting Parts')
        """) or 0

        ready_jobs = self.db.scalar("""
            SELECT COUNT(*)
            FROM service_jobs
            WHERE status='Ready'
        """) or 0

        customers = self.db.scalar("""
            SELECT COUNT(*)
            FROM customers
        """) or 0

        vehicles = self.db.scalar("""
            SELECT COUNT(*)
            FROM vehicles
        """) or 0

        revenue_today = self.db.scalar("""
            SELECT COALESCE(SUM(amount),0)
            FROM payments
            WHERE DATE(paid_at)=CURDATE()
        """) or 0

        outstanding = self.db.scalar("""
            SELECT COALESCE(SUM(total_amount),0)
            FROM service_jobs
            WHERE payment_status <> 'Paid'
        """) or 0

        values = [
            ("Active Jobs", active_jobs, BLUE),
            ("Ready for Delivery", ready_jobs, ACCENT),
            ("Customers", customers, ORANGE),
            ("Vehicles", vehicles, PURPLE),
            ("Revenue Today", f"₹{float(revenue_today):,.0f}", CYAN),
            ("Outstanding", f"₹{float(outstanding):,.0f}", RED),
        ]

        for i, (title, value, color) in enumerate(values):
            x = self.card(
                stats,
                title,
                value,
                color
            )

            x.grid(
                row=0,
                column=i,
                padx=(0 if i == 0 else 8, 0),
                sticky="nsew"
            )

            stats.grid_columnconfigure(
                i,
                weight=1
            )

        # ==========================================================
        # GRAPH AREA
        # ==========================================================

        charts = tk.Frame(
            dashboard_frame,
            bg=BG
        )

        charts.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=10
        )
        # ==========================================================
        # REVENUE BAR CHART
        # ==========================================================

        revenue_panel = self.revenue_bar_chart(dashboard_frame)

        revenue_panel.pack(
            fill="x",
            padx=32,
            pady=10
        )



        # ==========================================================
        # SERVICE STATUS DONUT
        # ==========================================================

        status_panel = tk.Frame(
            charts,
            bg=PANEL,
            width=380
        )

        status_panel.pack(
            side="right",
            fill="both",
            padx=(8, 0)
        )

        status_panel.pack_propagate(False)

        tk.Label(
            status_panel,
            text="🍩 Service Status",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        statuses = [
            "Booked",
            "In Progress",
            "Waiting Parts",
            "Ready",
            "Completed"
        ]

        status_values = []

        for status in statuses:
            count = self.db.scalar(
                """
                SELECT COUNT(*)
                FROM service_jobs
                WHERE status=%s
                """,
                (status,)
            ) or 0

            status_values.append(
                int(count)
            )

        status_fig = Figure(
            figsize=(4, 3),
            dpi=100,
            facecolor=PANEL
        )

        status_ax = status_fig.add_subplot(111)

        status_colors = [
            BLUE,
            ORANGE,
            RED,
            ACCENT,
            PURPLE
        ]

        if sum(status_values) > 0:

            status_ax.pie(
                status_values,
                labels=statuses,
                autopct="%1.0f%%",
                startangle=90,
                colors=status_colors,
                wedgeprops={
                    "width": 0.42,
                    "edgecolor": PANEL
                },
                textprops={
                    "color": TEXT,
                    "fontsize": 8
                }
            )

        else:

            status_ax.text(
                0.5,
                0.5,
                "No service data",
                ha="center",
                va="center",
                color=MUTED
            )

        status_ax.set_facecolor(PANEL)

        status_fig.tight_layout()

        status_canvas = FigureCanvasTkAgg(
            status_fig,
            master=status_panel
        )

        status_canvas.draw()

        status_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ==========================================================
        # LOWER DATA SECTION
        # ==========================================================

        lower = tk.Frame(
            dashboard_frame,
            bg=BG
        )

        lower.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=(5, 20)
        )

        # ==========================================================
        # RECENT SERVICE JOBS
        # ==========================================================

        jobs_panel = tk.Frame(
            lower,
            bg=PANEL
        )

        jobs_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            jobs_panel,
            text="🚗 Today's Service Pipeline",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=15
        )

        tree = ttk.Treeview(
            jobs_panel,
            columns=(
                "Job",
                "Vehicle",
                "Customer",
                "Status",
                "Total"
            ),
            show="headings"
        )

        for c, w in zip(
                (
                        "Job",
                        "Vehicle",
                        "Customer",
                        "Status",
                        "Total"
                ),
                (
                        60,
                        120,
                        180,
                        120,
                        110
                )
        ):
            tree.heading(
                c,
                text=c
            )

            tree.column(
                c,
                width=w
            )

        rows = self.db.query(
            """
            SELECT
                j.job_id,
                v.registration_no,
                c.full_name,
                j.status,
                j.total_amount

            FROM service_jobs j

            JOIN vehicles v
                ON j.vehicle_id=v.vehicle_id

            JOIN customers c
                ON v.customer_id=c.customer_id

            ORDER BY j.job_id DESC

            LIMIT 8
            """,
            fetch=True
        )

        for r in rows:
            tree.insert(
                "",
                "end",
                values=(
                    r["job_id"],
                    r["registration_no"],
                    r["full_name"],
                    r["status"],
                    f"₹{float(r['total_amount']):,.2f}"
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ==========================================================
        # BUSINESS SUMMARY
        # ==========================================================

        summary = tk.Frame(
            lower,
            bg=PANEL,
            width=330
        )

        summary.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        summary.pack_propagate(False)

        tk.Label(
            summary,
            text="📊 Business Summary",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=15
        )

        low_stock = self.db.scalar("""
            SELECT COUNT(*)
            FROM parts
            WHERE stock_qty <= reorder_level
        """) or 0

        completed = self.db.scalar("""
            SELECT COUNT(*)
            FROM service_jobs
            WHERE status='Completed'
        """) or 0

        urgent = self.db.scalar("""
            SELECT COUNT(*)
            FROM service_jobs
            WHERE priority='Urgent'
        """) or 0

        summary_data = [
            ("💰 Revenue Today", f"₹{float(revenue_today):,.0f}", CYAN),
            ("📦 Low Stock Items", low_stock, ORANGE),
            ("✅ Completed Jobs", completed, ACCENT),
            ("🚨 Urgent Jobs", urgent, RED),
        ]

        for label, value, color in summary_data:
            box = tk.Frame(
                summary,
                bg="#16233A"
            )

            box.pack(
                fill="x",
                padx=15,
                pady=5
            )

            tk.Label(
                box,
                text=label,
                bg="#16233A",
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=12,
                pady=(8, 0)
            )

            tk.Label(
                box,
                text=str(value),
                bg="#16233A",
                fg=color,
                font=("Segoe UI", 18, "bold")
            ).pack(
                anchor="w",
                padx=12,
                pady=(2, 8)
            )

    def show_customers(self):
        self.clear(); self.header("Customers","Customer relationship and contact records")
        bar=tk.Frame(self.content,bg=BG); bar.pack(fill="x",padx=32)
        tk.Button(bar,text="+ Add Customer",command=self.add_customer,bg=ACCENT,fg="#07130d",
                  bd=0,font=("Segoe UI",10,"bold"),padx=15,pady=9).pack(side="left")
        tree = self.table(
            self.content,
            ("Job", "Customer", "Vehicle", "Invoice Total", "Payment Status"),
            [70, 220, 130, 150, 150]
        )
        rows=self.db.query("SELECT customer_id,full_name,phone,email,address,created_at FROM customers ORDER BY customer_id DESC",fetch=True)
        for r in rows: tree.insert("", "end", values=(r["customer_id"],r["full_name"],r["phone"],r["email"] or "",r["address"] or "",str(r["created_at"])[:16]))

    def add_customer(self):
        self.form_window("Add Customer",[
            ("Full name",""),("Phone",""),("Email",""),("Address","")
        ], self.save_customer)

    def save_customer(self, vals, win):
        if not vals[0] or not vals[1]: return messagebox.showwarning("Required","Name and phone are required.")
        self.db.query("INSERT INTO customers(full_name,phone,email,address) VALUES(%s,%s,%s,%s)",tuple(vals))
        win.destroy(); self.show_customers()

    def show_vehicles(self):
        self.clear(); self.header("Vehicles","Any make, model, fuel type or powertrain")
        bar=tk.Frame(self.content,bg=BG); bar.pack(fill="x",padx=32)
        tk.Button(bar,text="+ Add Vehicle",command=self.add_vehicle,bg=ACCENT,fg="#07130d",
                  bd=0,font=("Segoe UI",10,"bold"),padx=15,pady=9).pack(side="left")
        tree=self.table(self.content,("ID","Registration","Make","Model","Year","Fuel","Odometer","Owner"),[55,120,130,140,70,100,100,190])
        rows=self.db.query("""SELECT v.vehicle_id,v.registration_no,v.make,v.model,v.year,v.fuel_type,
                              v.odometer_km,c.full_name FROM vehicles v JOIN customers c ON v.customer_id=c.customer_id
                              ORDER BY v.vehicle_id DESC""",fetch=True)
        for r in rows: tree.insert("", "end", values=(r["vehicle_id"],r["registration_no"],r["make"],r["model"],
                                                       r["year"] or "",r["fuel_type"],r["odometer_km"],r["full_name"]))

    def add_vehicle(self):
        customers=self.db.query("SELECT customer_id,full_name FROM customers ORDER BY full_name",fetch=True)
        if not customers:
            return messagebox.showwarning("Customer first","Add a customer before adding a vehicle.")
        self.form_window("Add Vehicle",[
            ("Registration No",""),("Make","Toyota"),("Model",""),("Year","2025"),
            ("Fuel type","Petrol"),("Odometer km","0"),("VIN",""),("Customer ID",str(customers[0]["customer_id"]))
        ],self.save_vehicle)

    def save_vehicle(self, vals, win):
        try:
            odometer_text = vals[5].replace(",", "").lower().replace("km", "").strip()
            odometer_km = int(odometer_text or 0)

            self.db.query(
                """
                INSERT INTO vehicles(
                    customer_id, registration_no, make, model, year,
                    fuel_type, odometer_km, vin
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    int(vals[7]), vals[0], vals[1], vals[2],
                    int(vals[3] or 0), vals[4], odometer_km, vals[6]
                )
            )

            messagebox.showinfo("Success", "Vehicle saved successfully!")
            win.destroy()
            self.show_vehicles()
        except ValueError:
            messagebox.showerror("Invalid Input", "Year, Customer ID and Odometer must be valid numbers.")
        except Exception as e:
            messagebox.showerror("Could not save", str(e))

    def show_jobs(self):
        self.clear(); self.header("Service Jobs","Workshop workflow from check-in to delivery")
        bar=tk.Frame(self.content,bg=BG);bar.pack(fill="x",padx=32)
        tk.Button(bar,text="+ Create Service Job",command=self.add_job,bg=ACCENT,fg="#07130d",
                  bd=0,font=("Segoe UI",10,"bold"),padx=15,pady=9).pack(side="left")
        tree=self.table(self.content,("Job","Registration","Customer","Complaint","Status","Priority","Total","Payment"),[60,120,180,260,120,90,110,100])
        rows=self.db.query("""SELECT j.job_id,v.registration_no,c.full_name,j.complaint,j.status,j.priority,
                              j.total_amount,j.payment_status FROM service_jobs j
                              JOIN vehicles v ON j.vehicle_id=v.vehicle_id JOIN customers c ON v.customer_id=c.customer_id
                              ORDER BY j.job_id DESC""",fetch=True)
        for r in rows: tree.insert("", "end", values=(r["job_id"],r["registration_no"],r["full_name"],r["complaint"] or "",
                                                     r["status"],r["priority"],f"₹{float(r['total_amount']):,.2f}",r["payment_status"]))

    def add_job(self):
        vehicles=self.db.query("SELECT vehicle_id,registration_no FROM vehicles ORDER BY registration_no",fetch=True)
        if not vehicles: return messagebox.showwarning("Vehicle first","Add a customer and vehicle before creating a job.")
        self.form_window("Create Service Job",[
            ("Vehicle ID",str(vehicles[0]["vehicle_id"])),("Advisor",""),("Complaint",""),
            ("Diagnosis",""),("Status","Booked"),("Priority","Normal"),("Promised date",str(date.today())),
            ("Next service date",str(date.today()+timedelta(days=180))),("Next service km","10000"),
            ("Labor cost","0"),("Notes","")
        ],self.save_job)

    def save_job(self, vals, win):
        try:
            self.db.query("""INSERT INTO service_jobs(vehicle_id,advisor_name,complaint,diagnosis,status,priority,
                             promised_date,next_service_date,next_service_km,labor_cost,notes,total_amount)
                             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                          (int(vals[0]),vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7],int(vals[8] or 0),
                           float(vals[9] or 0),vals[10],float(vals[9] or 0)))
            win.destroy(); self.show_jobs()
        except Exception as e: messagebox.showerror("Could not save",str(e))

    def show_catalog(self):
        self.clear(); self.header("Service Catalog","Reusable service menu for every make/model")
        tree=self.table(self.content,("ID","Service","Category","Default Price","Hours"),[60,280,200,130,100])
        rows=self.db.query("SELECT service_id,service_name,category,default_price,estimated_hours FROM service_catalog ORDER BY category,service_name",fetch=True)
        for r in rows: tree.insert("", "end", values=(r["service_id"],r["service_name"],r["category"],f"₹{float(r['default_price']):,.2f}",r["estimated_hours"]))

    def show_inventory(self):
        self.clear()

        self.header(
            "Inventory",
            "Parts and consumables stock control"
        )

        # ==============================
        # TOP ACTION BAR
        # ==============================

        bar = tk.Frame(
            self.content,
            bg=BG
        )

        bar.pack(
            fill="x",
            padx=32,
            pady=(0, 8)
        )

        tk.Button(
            bar,
            text="+ Add Part",
            command=self.add_part,
            bg=ACCENT,
            fg="#07130d",
            activebackground="#6bf0ae",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9
        ).pack(
            side="left"
        )

        # ==============================
        # INVENTORY TABLE
        # ==============================

        tree = self.table(
            self.content,
            (
                "ID",
                "Part",
                "Part Number",
                "Category",
                "Stock",
                "Reorder",
                "Unit Price"
            ),
            [60, 250, 140, 160, 90, 90, 120]
        )

        rows = self.db.query(
            """
            SELECT
                part_id,
                part_name,
                part_number,
                category,
                stock_qty,
                reorder_level,
                unit_price
            FROM parts
            ORDER BY part_id DESC
            """,
            fetch=True
        )

        for r in rows:
            tree.insert(
                "",
                "end",
                values=(
                    r["part_id"],
                    r["part_name"],
                    r["part_number"] or "",
                    r["category"] or "",
                    r["stock_qty"],
                    r["reorder_level"],
                    f"₹{float(r['unit_price']):,.2f}"
                )
            )

    def add_part(self):
        self.form_window(
            "Add Inventory Part",
            [
                ("Part Name", ""),
                ("Part Number", ""),
                ("Category", "Engine"),
                ("Stock Quantity", "0"),
                ("Reorder Level", "5"),
                ("Unit Price", "0")
            ],
            self.save_part
        )

    def save_part(self, vals, win):
        try:
            part_name = vals[0]
            part_number = vals[1]
            category = vals[2]
            stock_qty = int(vals[3] or 0)
            reorder_level = int(vals[4] or 5)
            unit_price = float(vals[5] or 0)

            if not part_name:
                return messagebox.showwarning("Required", "Please enter Part Name.")
            if stock_qty < 0:
                return messagebox.showwarning("Invalid Stock", "Stock quantity cannot be negative.")
            if reorder_level < 0:
                return messagebox.showwarning("Invalid Reorder Level", "Reorder level cannot be negative.")
            if unit_price < 0:
                return messagebox.showwarning("Invalid Price", "Unit price cannot be negative.")

            self.db.query(
                """
                INSERT INTO parts(part_name, part_number, category, stock_qty, reorder_level, unit_price)
                VALUES(%s,%s,%s,%s,%s,%s)
                """,
                (part_name, part_number, category, stock_qty, reorder_level, unit_price)
            )

            messagebox.showinfo("Success", "Part added to inventory successfully!")
            win.destroy()
            self.show_inventory()

        except ValueError:
            messagebox.showerror("Invalid Input", "Stock, reorder level and price must contain valid numbers.")
        except Exception as e:
            messagebox.showerror("Could Not Save", str(e))

    def show_billing(self):
        self.clear()
        self.header(
            "Billing & Payments",
            "Outstanding and completed payment overview"
        )

        # Billing table
        tree = self.table(
            self.content,
            ("Job", "Customer", "Vehicle", "Invoice Total", "Payment Status"),
            [70, 220, 130, 150, 150]
        )

        rows = self.db.query("""
            SELECT
                j.job_id,
                c.full_name,
                v.registration_no,
                j.total_amount,
                j.payment_status
            FROM service_jobs j
            JOIN vehicles v
                ON j.vehicle_id = v.vehicle_id
            JOIN customers c
                ON v.customer_id = c.customer_id
            ORDER BY j.job_id DESC
        """, fetch=True)

        for r in rows:
            status = r["payment_status"]

            tree.insert(
                "",
                "end",
                values=(
                    r["job_id"],
                    r["full_name"],
                    r["registration_no"],
                    f"₹{float(r['total_amount']):,.2f}",
                    status
                )
            )

        # PAY button area
        action_frame = tk.Frame(
            self.content,
            bg=BG
        )
        action_frame.pack(
            fill="x",
            padx=32,
            pady=15
        )

        tk.Button(
            action_frame,
            text="💰 PAY SELECTED",
            command=lambda: self.mark_selected_paid(tree),
            bg=ACCENT,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Label(
            action_frame,
            text="Select an Unpaid job and click PAY SELECTED",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=15)
    def mark_selected_paid(self, tree):
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Job",
                "Please select an Unpaid job first."
            )
            return

        item = tree.item(selected[0])
        values = item["values"]

        job_id = values[0]
        customer = values[1]
        amount_text = values[3]
        status = values[4]

        if status == "Paid":
            messagebox.showinfo(
                "Already Paid",
                f"Job #{job_id} is already Paid."
            )
            return

        amount = float(
            str(amount_text)
            .replace("₹", "")
            .replace(",", "")
        )

        confirm = messagebox.askyesno(
            "Confirm Payment",
            f"Customer: {customer}\n"
            f"Job: #{job_id}\n"
            f"Amount: ₹{amount:,.2f}\n\n"
            "Mark this payment as PAID?"
        )

        if not confirm:
            return

        try:
            # 1. Service job -> Paid
            self.db.query(
                """
                UPDATE service_jobs
                SET payment_status = 'Paid'
                WHERE job_id = %s
                """,
                (job_id,)
            )

            # 2. Add payment -> Revenue
            self.db.query(
                """
                INSERT INTO payments (job_id, amount, paid_at)
                VALUES (%s, %s, NOW())
                """,
                (job_id, amount)
            )

            messagebox.showinfo(
                "Payment Successful",
                f"₹{amount:,.2f} payment received successfully!"
            )

            # Refresh Billing page
            self.show_billing()

        except Exception as e:
            messagebox.showerror(
                "Payment Error",
                str(e)
            )

    def show_reminders(self):
        self.clear(); self.header("Maintenance Reminders","Upcoming service commitments")
        tree=self.table(self.content,("Job","Vehicle","Customer","Next Service Date","Next Service KM","Status"),[70,130,200,160,150,120])
        rows=self.db.query("""SELECT j.job_id,v.registration_no,c.full_name,j.next_service_date,j.next_service_km,j.status
                              FROM service_jobs j JOIN vehicles v ON j.vehicle_id=v.vehicle_id
                              JOIN customers c ON v.customer_id=c.customer_id
                              WHERE j.next_service_date IS NOT NULL ORDER BY j.next_service_date""",fetch=True)
        for r in rows: tree.insert("", "end", values=(r["job_id"],r["registration_no"],r["full_name"],
                                                       r["next_service_date"],r["next_service_km"],r["status"]))

    def form_window(self, title, fields, callback):

        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("620x720")
        win.minsize(560, 520)
        win.configure(bg=PANEL)
        win.transient(self)
        win.grab_set()

        # ==============================
        # HEADER
        # ==============================

        header = tk.Frame(win, bg=PANEL)
        header.pack(fill="x", padx=28, pady=(22, 10))

        tk.Label(
            header,
            text=title,
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Enter the information and save the record.",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(4, 0))

        # ==============================
        # SCROLLABLE FORM AREA
        # ==============================

        area = tk.Frame(win, bg=PANEL)
        area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 8)
        )

        canvas = tk.Canvas(
            area,
            bg=PANEL,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            area,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        body = tk.Frame(
            canvas,
            bg=PANEL
        )

        window_id = canvas.create_window(
            (0, 0),
            window=body,
            anchor="nw"
        )

        def update_scroll(event=None):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

            canvas.itemconfigure(
                window_id,
                width=canvas.winfo_width()
            )

        body.bind(
            "<Configure>",
            update_scroll
        )

        canvas.bind(
            "<Configure>",
            update_scroll
        )

        # ==============================
        # FORM FIELDS
        # ==============================

        entries = []

        for label, default in fields:

            tk.Label(
                body,
                text=label,
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w",
                pady=(8, 3)
            )

            # Fuel dropdown
            if label == "Fuel type":

                e = ttk.Combobox(
                    body,
                    values=[
                        "Petrol",
                        "Diesel",
                        "CNG",
                        "Electric",
                        "Hybrid",
                        "Other"
                    ],
                    state="readonly",
                    font=("Segoe UI", 10)
                )

                e.set(
                    default if default else "Petrol"
                )

            else:

                e = tk.Entry(
                    body,
                    bg="#0d1728",
                    fg=TEXT,
                    insertbackground=TEXT,
                    relief="flat",
                    font=("Segoe UI", 10)
                )

                e.insert(
                    0,
                    default
                )

            e.pack(
                fill="x",
                ipady=9
            )

            entries.append(e)

        # ==============================
        # FIXED BOTTOM BUTTON BAR
        # ==============================

        footer = tk.Frame(
            win,
            bg="#0d1728",
            height=78
        )

        footer.pack(
            fill="x",
            side="bottom"
        )

        footer.pack_propagate(False)

        # CANCEL BUTTON

        tk.Button(
            footer,
            text="CANCEL",
            command=win.destroy,
            bg="#26344d",
            fg=TEXT,
            activebackground="#33445f",
            activeforeground=TEXT,
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=22,
            pady=10
        ).pack(
            side="right",
            padx=(8, 28),
            pady=17
        )

        # SAVE BUTTON

        save_text = (
            "✓  SAVE VEHICLE"
            if title == "Add Vehicle"
            else "✓  SAVE RECORD"
        )

        tk.Button(
            footer,
            text=save_text,
            command=lambda: callback(
                [e.get().strip() for e in entries],
                win
            ),
            bg=ACCENT,
            fg="#07130d",
            activebackground="#6bf0ae",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=22,
            pady=10
        ).pack(
            side="right",
            pady=17
        )

        # ==============================
        # MOUSE WHEEL SCROLLING
        # ==============================

        def wheel(event):
            canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            wheel,
            add="+"
        )

        # ==============================
        # WINDOW CLOSE
        # ==============================

        def cleanup():

            try:
                canvas.unbind_all(
                    "<MouseWheel>"
                )
            except Exception:
                pass

            win.destroy()

        win.protocol(
            "WM_DELETE_WINDOW",
            cleanup
        )

