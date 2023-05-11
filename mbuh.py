
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

PROXY_TYPES = {
    '1': 'http',
    '2': 'socks4',
    '3': 'socks5',
    '4': False
}

class ConfigAPI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Config API")
        self.window.geometry("800x600")
        self.window.resizable(0, 0)

        self.http_api_var = tk.BooleanVar()
        self.http_api_var.set(True)

        self.port_var = tk.StringVar()
        self.port_var.set("5000")


        self.database_var = tk.BooleanVar()
        self.database_var.set(True)

        self.views_var = tk.StringVar()
        self.views_var.set("100")

        self.minimum_var = tk.StringVar()
        self.minimum_var.set("85")

        self.maximum_var = tk.StringVar()
        self.maximum_var.set("95")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Apakah Anda ingin mengaktifkan HTTP API di server lokal?").pack(pady=10)

        tk.Radiobutton(self.window, text="Yes", variable=self.http_api_var, value=True).pack()
        tk.Radiobutton(self.window, text="No", variable=self.http_api_var, value=False).pack()

        tk.Label(self.window, text="Enter a free port:").pack(pady=10)
        tk.Entry(self.window, textvariable=self.port_var).pack()

        tk.Label(self.window, text="Apakah Anda ingin menyimpan jumlah tampilan harian yang dihasilkan dalam Database?").pack(pady=10)

        tk.Radiobutton(self.window, text="Yes", variable=self.database_var, value=True).pack()
        tk.Radiobutton(self.window, text="No", variable=self.database_var, value=False).pack()

        tk.Label(self.window, text="Jumlah tampilan yang Anda inginkan:").pack(pady=10)
        tk.Entry(self.window, textvariable=self.views_var).pack()

        tk.Label(self.window, text="Durasi menonton minimum dalam persentase:").pack(pady=10)
        tk.Entry(self.window, textvariable=self.minimum_var).pack()

        tk.Label(self.window, text="Durasi menonton maksimum dalam persentase:").pack(pady=10)
        tk.Entry(self.window, textvariable=self.maximum_var).pack()

        tk.Button(self.window, text="Save", command=self.save_config).pack(pady=20)


    def save_config(self):
        enabled = self.http_api_var.get()
        port = self.port_var.get()

        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return

        config = {
            "http_api": {
                "enabled": enabled,
                "host": "0.0.0.0",
                "port": port
            }
        }

        database = self.database_var.get()
        views = self.views_var.get()
        minimum = self.minimum_var.get()
        maximum = self.maximum_var.get()

        try:
            views = int(views)
        except ValueError:
            messagebox.showerror("Error", "Jumlah tampilan harus berupa angka")
            return

        try:
            minimum = float(minimum)
        except ValueError:
            messagebox.showerror("Error", "Durasi menonton minimum harus berupa angka")
            return

        try:
            maximum = float(maximum)
        except ValueError:
            messagebox.showerror("Error", "Durasi menonton maksimum harus berupa angka")
            return

        if minimum >= maximum:
            minimum = maximum - 5

        config = {
            "database": database,
            "views": views,
            "minimum": minimum,
            "maximum": maximum
        }

        with open("config.json", "w") as f:
            json.dump(config, f)

        messagebox.showinfo("Success", "Config saved")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ConfigAPI()
    app.run()


class ProxyConfigWindow(tk.Toplevel):
    def __init__(self, parent, category):
        super().__init__(parent)
        self.title("Proxy Configuration")
        self.category = category
        
        self.handle_proxy_var = tk.BooleanVar()
        self.filename_var = tk.StringVar()
        self.proxy_type_var = tk.StringVar(value="1")
        self.auth_required_var = tk.BooleanVar()
        self.proxy_api_var = tk.BooleanVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        handle_proxy_label = ttk.Label(self, text="Handle Proxy?")
        handle_proxy_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        handle_proxy_yes = ttk.Radiobutton(self, text="Yes", variable=self.handle_proxy_var, value=True)
        handle_proxy_yes.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        handle_proxy_no = ttk.Radiobutton(self, text="No", variable=self.handle_proxy_var, value=False)
        handle_proxy_no.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        filename_label = ttk.Label(self, text="Filename or API URL:")
        filename_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        filename_entry = ttk.Entry(self, textvariable=self.filename_var)
        filename_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        
        proxy_type_label = ttk.Label(self, text="Proxy Type:")
        proxy_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        proxy_type_menu = ttk.OptionMenu(self, self.proxy_type_var, *PROXY_TYPES.keys())
        proxy_type_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        auth_required_label = ttk.Label(self, text="Auth Required?")
        auth_required_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        auth_required_yes = ttk.Radiobutton(self, text="Yes", variable=self.auth_required_var, value=True)
        auth_required_yes.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        auth_required_no = ttk.Radiobutton(self, text="No", variable=self.auth_required_var, value=False)
        auth_required_no.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        proxy_api_label = ttk.Label(self, text="API Proxy?")
        proxy_api_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        proxy_api_yes = ttk.Radiobutton(self, text="Yes", variable=self.proxy_api_var, value=True)
        proxy_api_yes.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        proxy_api_no = ttk.Radiobutton(self, text="No", variable=self.proxy_api_var, value=False)
        proxy_api_no.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="we")
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=5, pady=5)
        
        ok_button = ttk.Button(button_frame, text="OK", command=self.ok)
        ok_button.pack(side="right", padx=5, pady=5)
        
    def cancel(self):
        self.destroy()
        
    def ok(self):
        handle_proxy = self.handle_proxy_var.get()
        filename = self.filename_var.get()
        proxy_type = PROXY_TYPES[self.proxy_type_var.get()]
        auth_required = self.auth_required_var.get()
        proxy_api = self.proxy_api_var.get()
        
        # Do something with the proxy configuration
        print(handle_proxy, filename, proxy_type, auth_required, proxy_api)
        
        self.destroy()

# Example usage:
root = tk.Tk()
config_window = ProxyConfigWindow(root, "YouTube")
root.mainloop()

class ProxyConfigWindow(tk.Toplevel):
    def __init__(self, parent, category):
        super().__init__(parent)
        self.title("Proxy Configuration")
        self.category = category
        
        self.auth_required_var = tk.BooleanVar(value=False)
        self.filename_var = tk.StringVar()
        self.handle_proxy_var = tk.BooleanVar(value=False)
        self.proxy_api_var = tk.BooleanVar(value=False)
        self.proxy_type_var = tk.StringVar(value="1")
        
        self.create_widgets()
        
    def create_widgets(self):
        if self.category == 'r':
            info_label = ttk.Label(self, text="If you're using a Proxy API URL, the script will scrape the proxy list at the start of each thread.\nAnd it will use one proxy randomly from that list to ensure session management.")
            info_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        filename_label = ttk.Label(self, text="Filename or API URL:")
        filename_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        filename_entry = ttk.Entry(self, textvariable=self.filename_var)
        filename_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        
        if self.category == 'r':
            auth_checkbutton = ttk.Checkbutton(self, text="Proxy requires authentication", variable=self.auth_required_var)
            auth_checkbutton.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            
            if self.auth_required_var.get():
                proxy_type_label = ttk.Label(self, text="Proxy type:")
                proxy_type_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
                
                proxy_type_combobox = ttk.Combobox(self, values=["HTTP", "SOCKS4", "SOCKS5"], textvariable=self.proxy_type_var, state="readonly")
                proxy_type_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="we")
                
            else:
                handle_proxy_checkbutton = ttk.Checkbutton(self, text="Handle proxy type", variable=self.handle_proxy_var)
                handle_proxy_checkbutton.grid(row=2, column=1, padx=5, pady=5, sticky="w")
                
                if self.handle_proxy_var.get():
                    proxy_type_label = ttk.Label(self, text="Proxy type:")
                    proxy_type_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
                    
                    proxy_type_combobox = ttk.Combobox(self, values=["HTTP", "SOCKS4", "SOCKS5"], textvariable=self.proxy_type_var, state="readonly")
                    proxy_type_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="we")
            
        else:
            auth_checkbutton = ttk.Checkbutton(self, text="Proxy requires authentication", variable=self.auth_required_var)
            auth_checkbutton.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            
            proxy_type_label = ttk.Label(self, text="Proxy type:")
            proxy_type_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            
            proxy_type_combobox = ttk.Combobox(self, values=["HTTP", "SOCKS4", "SOCKS5"], textvariable=self.proxy_type_var, state="readonly")
            proxy_type_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="we")
            
        proxy_api_checkbutton = ttk.Checkbutton(self, text="API URL", variable=self.proxy_api_var)
        proxy_api_checkbutton.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")
        
        ok_button = ttk.Button(self, text="OK", command=self.ok)
        ok_button.grid(row=5, column=2, padx=5, pady=5, sticky="e")
        
    def ok(self):
        proxy_type = self.proxy_type_var.get().lower()
        filename = self.filename_var.get()
        auth_required = self.auth_required_var.get()
        proxy_api = self.proxy_api_var.get()
        
        if self.category == 'r' and not proxy_api and not auth_required and not self.handle_proxy_var.get():
            # If using rotating proxies and not using API, authentication, or handling proxy type, show an error message
            ttk.messagebox.showerror("Error", "Please choose a proxy source or handle the proxy type.")
            return
        
        self.result = (proxy_type, filename, auth_required, proxy_api)
        self.destroy()

def config_premium_proxy_gui(category):
    window = ProxyConfigWindow(parent=None, category=category)
    window.wait_window()
    return window.result

def config_proxy(config):
    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Proxy Configuration")

    # Add a label for the proxy category
    category_label = tk.Label(window, text="Proxy Category:")
    category_label.pack()

    # Add radio buttons for the proxy category
    category_var = tk.StringVar(value="F")
    free_button = tk.Radiobutton(window, text="Free", variable=category_var, value="F")
    premium_button = tk.Radiobutton(window, text="Premium", variable=category_var, value="P")
    rotating_button = tk.Radiobutton(window, text="Rotating", variable=category_var, value="R")
    free_button.pack()
    premium_button.pack()
    rotating_button.pack()

    # Add a label for the proxy type
    type_label = tk.Label(window, text="Proxy Type:")
    type_label.pack()

    # Add radio buttons for the proxy type
    type_var = tk.StringVar(value="HTTP")
    http_button = tk.Radiobutton(window, text="HTTP", variable=type_var, value="HTTP")
    socks4_button = tk.Radiobutton(window, text="SOCKS4", variable=type_var, value="SOCKS4")
    socks5_button = tk.Radiobutton(window, text="SOCKS5", variable=type_var, value="SOCKS5")
    http_button.pack()
    socks4_button.pack()
    socks5_button.pack()

    # Add a checkbox for authentication
    auth_var = tk.BooleanVar()
    auth_check = tk.Checkbutton(window, text="Authentication Required", variable=auth_var)
    auth_check.pack()

    # Add an input field for the proxy location
    location_label = tk.Label(window, text="Proxy Location:")
    location_label.pack()
    location_entry = tk.Entry(window)
    location_entry.pack()

    # Add an input field for the refresh interval
    refresh_label = tk.Label(window, text="Refresh Interval (minutes):")
    refresh_label.pack()
    refresh_entry = tk.Entry(window)
    refresh_entry.pack()

    # Add a button to submit the configuration
    def submit_config():
        category = category_var.get()
        proxy_type = type_var.get()
        auth_required = auth_var.get()
        location = location_entry.get()
        refresh = float(refresh_entry.get()) if refresh_entry.get() != "" else 0.0

        if category == 'F':
            proxy_type, filename, auth_required, proxy_api = config_free_proxy(category)

        elif category == 'P' or category == 'R':
            proxy_type, filename, auth_required, proxy_api = config_premium_proxy(category)

        config["proxy"] = {
            "category": category,
            "proxy_type": proxy_type,
            "filename": filename,
            "authentication": auth_required,
            "location": location,
            "proxy_api": proxy_api,
            "refresh": refresh
        }
        window.destroy()

    submit_button = tk.Button(window, text="Submit", command=submit_config)
    submit_button.pack()

    # Start the Tkinter event loop
    window.mainloop()

    return config



def config_gui(config):
    def set_background():
        if background_var.get() == 1:
            config["background"] = True
        else:
            config["background"] = False
        root.destroy()

    root = tk.Tk()
    root.title("Configuration")
    root.geometry("400x200")

    label = tk.Label(root, text="Apakah Anda ingin menjalankan dalam mode latar belakang.? (recommended=No)")
    label.pack()

    background_var = tk.IntVar()
    background_var.set(0)
    radio1 = tk.Radiobutton(root, text="No", variable=background_var, value=0)
    radio2 = tk.Radiobutton(root, text="Yes", variable=background_var, value=1)
    radio1.pack()
    radio2.pack()

    ok_button = tk.Button(root, text="OK", command=set_background)
    ok_button.pack()

    root.mainloop()

    return config
