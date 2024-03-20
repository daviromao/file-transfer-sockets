import json
import customtkinter as ctk
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox
from client import get_file_list, send_file, download_file


def validate_ip(ip: str) -> bool:
    """Validates an IP address. Returns True if the IP is valid, False otherwise."""
    ip_parts = ip.split(".")
    if len(ip_parts) != 4:
        return False

    for part in ip_parts:
        try:
            part_int = int(part)
            if part_int < 0 or part_int > 255:
                return False
        except ValueError:
            return False

    return True


def validate_port(port: str) -> bool:
    """Validates a port number. Returns True if the port is valid, False otherwise."""
    try:
        port_int = int(port)
    except ValueError:
        return False

    return port_int > 0 and port_int < 65536


def get_formatted_size(size):
    if size is None:
        return "0 KB"

    for size_unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {size_unit}'
        size = size / 1024.0


def process_file_list(file_list: list) -> list:
    """Process the file list received from the server. Returns a list of dictionaries."""
    data = []

    for i, file in enumerate(file_list):
        data.append([
            i + 1,
            file["name"][:40],
            file["name"].split(".")[-1].upper(),
            f"{get_formatted_size(file["size"])}"
        ])

    return data


class FTSApp:

    CURRENT_SERVER_PORT: int = -1
    CURRENT_SERVER_IP: str = ""

    def __init__(self):
        self.interface_setup()

    def interface_setup(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.geometry("680x750")
        self.app.title("Network File Sharing")

        title = ctk.CTkLabel(master=self.app, text="Transferência de Arquivos",
                             font=("Arial", 32))
        title.pack(pady=20)

        # Server information section
        server_frame = ctk.CTkFrame(master=self.app)
        server_frame.pack(pady=10, padx=60, fill="x", anchor=ctk.N)

        server_label = ctk.CTkLabel(master=server_frame, text="Dados do servidor",
                                    font=("Arial", 20))
        server_label.pack(pady=(10, 10), padx=20, anchor=ctk.W)

        ip_label = ctk.CTkLabel(master=server_frame, text="IP do servidor")
        ip_label.pack(side="top", anchor=ctk.W, padx=20)

        self.ip_entry = ctk.CTkEntry(master=server_frame,
                                     placeholder_text="Server IP")
        self.ip_entry.pack(side="top", fill="x", pady=(0, 10), padx=20)

        port_label = ctk.CTkLabel(master=server_frame,
                                  text="Porta do servidor")
        port_label.pack(side="top", anchor=ctk.W, padx=20)

        self.port_entry = ctk.CTkEntry(master=server_frame,
                                       placeholder_text="Server port")
        self.port_entry.pack(side="top", fill="x", pady=(0, 10), padx=20)

        self.con_btn = ctk.CTkButton(master=server_frame,
                                     text="Conecte-se",
                                     command=self.register_server_info)
        self.con_btn.pack(side="left", pady=20, padx=20)

        self.discon_btn = ctk.CTkButton(master=server_frame, text="Descontecar-se",
                                        command=self.reset_server_info)
        self.discon_btn.pack(side="left", pady=20, padx=0)
        self.discon_btn.configure(state="disabled", fg_color="gray")

        # Downloadable files section
        files_frame = ctk.CTkScrollableFrame(master=self.app, height=300)
        files_frame.pack(pady=10, padx=60, fill="x", anchor=ctk.N)
        files_frame.bind_all(
            "<Button-4>", lambda e: files_frame._parent_canvas.yview("scroll", -1, "units"))
        files_frame.bind_all(
            "<Button-5>", lambda e: files_frame._parent_canvas.yview("scroll", 1, "units"))

        files_frame.columnconfigure(0, weight=1)
        files_frame.columnconfigure(1, weight=1)

        files_label = ctk.CTkLabel(master=files_frame)
        files_label.grid(row=0, column=0, sticky=ctk.W, padx=10, pady=(10, 0))
        files_label.configure(text="Arquivos disponíveis", font=("Arial", 20))

        self.refresh_btn = ctk.CTkButton(master=files_frame, text="Refresh", width=20,
                                         command=self.update_file_table)
        self.refresh_btn.grid(row=0, column=1, padx=10, sticky=ctk.E,
                              pady=(10, 0))
        self.refresh_btn.configure(state="disabled")

        # File table
        header = [["#", "Nome", "Tipo", "Tamanho"]]

        self.table = CTkTable(master=files_frame, row=1, column=4, values=header,
                              command=self.row_clicked, corner_radius=0)
        self.table.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 20))

        if self.table.rows == 1:
            self.no_file_label = ctk.CTkLabel(master=files_frame, text_color="gray",
                                              text="Conecte-se a um servidor para ver seus arquivos.")
            self.no_file_label.grid(row=2, column=0, columnspan=2)

        self.download_btn = ctk.CTkButton(master=self.app,
                                          text="Download",
                                          command=self.download)
        self.download_btn.pack(side="left", pady=10,
                               padx=(60, 20), anchor=ctk.N)
        self.download_btn.configure(state="disabled")

        self.upload_btn = ctk.CTkButton(master=self.app, text="Upload",
                                        command=self.upload)
        self.upload_btn.pack(side="left", pady=10, padx=0, anchor=ctk.N)
        self.upload_btn.configure(fg_color="gray")
        self.upload_btn.configure(state="disabled")

    def run(self):
        self.app.mainloop()

    def register_server_info(self):
        server_ip = self.ip_entry.get()
        server_port = self.port_entry.get()

        if validate_ip(server_ip) == False and validate_port(server_port) == False:
            CTkMessagebox(title="Error",
                          message="Número de porta ou IP inválidos.",
                          icon="cancel")

            self.ip_entry.delete(0, "end")
            self.port_entry.delete(0, "end")

            self.ip_entry.focus()

            return

        print(f"Server IP: {self.ip_entry.get()}")
        print(f"Server Port: {self.port_entry.get()}")

        self.CURRENT_SERVER_IP = self.ip_entry.get()
        self.CURRENT_SERVER_PORT = int(self.port_entry.get())

        self.ip_entry.configure(state="disabled")
        self.port_entry.configure(state="disabled")

        self.con_btn.configure(state="disabled")
        self.discon_btn.configure(state="normal", fg_color="gray")

        self.upload_btn.configure(state="normal")
        self.download_btn.configure(state="normal")
        self.refresh_btn.configure(state="normal")

        self.no_file_label.grid_forget()

        self.update_file_table()

    def reset_server_info(self):
        self.ip_entry.configure(state="normal")
        self.port_entry.configure(state="normal")

        self.ip_entry.delete(0, "end")
        self.port_entry.delete(0, "end")

        self.con_btn.configure(state="normal")
        self.discon_btn.configure(state="disabled", fg_color="gray")

        self.CURRENT_SERVER_PORT = -1
        self.CURRENT_SERVER_IP = ""

        self.no_file_label.grid(row=2, column=0, columnspan=2)

        self.upload_btn.configure(state="disabled")
        self.download_btn.configure(state="disabled")
        self.refresh_btn.configure(state="disabled")

        self.erase_table()

        self.ip_entry.focus()

    def row_clicked(self, event):
        if event.get("row") == 0:
            return None

        for i in range(self.table.rows):
            self.table.deselect_row(i)

        self.table.select_row(event.get("row"))

    def update_file_table(self):
        if self.CURRENT_SERVER_IP == "" or self.CURRENT_SERVER_PORT == -1:
            CTkMessagebox(title="Error",
                          message="Você precisa se conectar a um servidor para ver seus arquivos.",
                          icon="cancel")
            return

        self.erase_table()

        # get file list from server
        files = json.loads(get_file_list(self.CURRENT_SERVER_IP,
                                         self.CURRENT_SERVER_PORT))
        data = process_file_list(files)

        for i, row in enumerate(data):
            self.table.add_row(index=i + 1, values=row)

        self.set_table_column_size()

    def erase_table(self):
        self.table.delete_rows(range(1, self.table.rows))

    def download(self):
        selected_filename = self.table.get_selected_row()["values"][1]
        print(f"Selected file to download from server: {selected_filename}")
        download_file(selected_filename, self.CURRENT_SERVER_IP,
                      self.CURRENT_SERVER_PORT)

        msg = CTkMessagebox(message="Download finalizado com sucesso.",
                            icon="check", option_1="Ok")

        print(msg.get())

    def upload(self):
        filename = ctk.filedialog.askopenfilename()

        print(f"Selected file to upload to server: {filename}")

        send_file(filename, self.CURRENT_SERVER_IP, self.CURRENT_SERVER_PORT)

        msg = CTkMessagebox(message="Upload finalizado com sucesso.",
                            icon="check", option_1="Ok")

        print(msg.get())
        self.update_file_table()

    def set_table_column_size(self):
        self.table.edit_column(0, width=20)
        self.table.edit_column(1, width=250, anchor=ctk.W)
        self.table.edit_column(2, width=100, anchor=ctk.W)
        self.table.edit_column(3, width=140)
