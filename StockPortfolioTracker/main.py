import tkinter as tk
from tkinter import messagebox
import csv
import os

# -------------------------------------
# Hardcoded Stock Prices
# -------------------------------------
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOG": 140,
    "AMZN": 130,
    "MSFT": 330
}

# -------------------------------------
# Main App Class
# -------------------------------------
class StockPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Stock Portfolio Tracker")
        self.root.geometry("650x500")
        self.root.config(bg="#1e1e2e")

        self.portfolio = {}

        # Title
        tk.Label(root, text="Stock Portfolio Tracker", font=("Helvetica", 24, "bold"), bg="#1e1e2e", fg="#00ffae").pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(root, bg="#1e1e2e")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Stock Symbol:", font=("Helvetica", 14), bg="#1e1e2e", fg="white").grid(row=0, column=0, padx=5)
        self.stock_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=10)
        self.stock_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Quantity:", font=("Helvetica", 14), bg="#1e1e2e", fg="white").grid(row=0, column=2, padx=5)
        self.qty_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=10)
        self.qty_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="Add Stock", bg="#00ffae", fg="black", font=("Helvetica", 12, "bold"),
                  command=self.add_stock).grid(row=0, column=4, padx=10)

        # Portfolio Display
        self.display = tk.Text(root, height=12, width=70, font=("Courier", 12), bg="#2a2a3d", fg="white")
        self.display.pack(pady=20)
        self.display.insert(tk.END, "📈 Portfolio Summary:\n\n")

        # Total Label
        self.total_label = tk.Label(root, text="Total Investment: $0", font=("Helvetica", 16, "bold"), bg="#1e1e2e", fg="#ffcc00")
        self.total_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save to CSV", bg="#3b82f6", fg="white", font=("Helvetica", 12, "bold"),
                  command=self.save_to_csv).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Clear All", bg="#ff4b5c", fg="white", font=("Helvetica", 12, "bold"),
                  command=self.clear_portfolio).grid(row=0, column=1, padx=10)

    # -------------------------------------
    # Add Stock
    # -------------------------------------
    def add_stock(self):
        stock = self.stock_entry.get().upper()
        qty = self.qty_entry.get()

        if not stock or not qty:
            messagebox.showwarning("Input Error", "Please enter both stock symbol and quantity.")
            return

        if stock not in STOCK_PRICES:
            messagebox.showerror("Invalid Stock", f"'{stock}' not found in stock list.")
            return

        try:
            qty = int(qty)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a number.")
            return

        self.portfolio[stock] = self.portfolio.get(stock, 0) + qty
        self.update_display()

        # Clear entry boxes
        self.stock_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)

    # -------------------------------------
    # Update Display
    # -------------------------------------
    def update_display(self):
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "📈 Portfolio Summary:\n\n")

        total = 0
        for stock, qty in self.portfolio.items():
            price = STOCK_PRICES[stock]
            investment = qty * price
            total += investment
            self.display.insert(tk.END, f"{stock:6} | Qty: {qty:<4} | Price: ${price:<4} | Value: ${investment}\n")

        self.total_label.config(text=f"Total Investment: ${total}")

    # -------------------------------------
    # Save Portfolio to CSV File
    # -------------------------------------
    def save_to_csv(self):
        if not self.portfolio:
            messagebox.showinfo("Empty Portfolio", "No stocks to save.")
            return

        # Ensure the "data" folder exists
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", "portfolio.csv")

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Stock", "Quantity", "Price", "Value"])

            total = 0
            for stock, qty in self.portfolio.items():
                price = STOCK_PRICES[stock]
                value = qty * price
                total += value
                writer.writerow([stock, qty, price, value])

            writer.writerow([])
            writer.writerow(["Total Investment", "", "", total])

        messagebox.showinfo("✅ Saved", f"Portfolio saved successfully in:\n{file_path}")

    # -------------------------------------
    # Clear Portfolio
    # -------------------------------------
    def clear_portfolio(self):
        self.portfolio.clear()
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "📈 Portfolio Summary:\n\n")
        self.total_label.config(text="Total Investment: $0")
        messagebox.showinfo("Cleared", "Portfolio cleared successfully.")


# -------------------------------------
# Main Program
# -------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioApp(root)
    root.mainloop()
