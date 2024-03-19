import customtkinter as ctk
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox


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


class FTSApp:

    CURRENT_SERVER_PORT: int = -1
    CURRENT_SERVER_IP: str = ""
    # CURRENT_SERVER_FILE_COUNT: int = 0

    def __init__(self):
        self.interface_setup()

    def interface_setup(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.geometry("700x800")
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
                                     text="Conecte-se a um servidor",
                                     command=self.register_server_info)
        self.con_btn.pack(side="left", pady=20, padx=20)

        self.discon_btn = ctk.CTkButton(master=server_frame, text="Descontecar-se",
                                        command=self.reset_server_info)
        self.discon_btn.pack(side="left", pady=20, padx=0)
        self.discon_btn.configure(state="disabled", fg_color="gray")

        # Downloadable files section
        files_frame = ctk.CTkScrollableFrame(master=self.app, height=360)
        files_frame.pack(pady=10, padx=60, fill="x", anchor=ctk.N)

        files_label = ctk.CTkLabel(master=files_frame)
        files_label.pack(pady=(10, 0), padx=20, anchor=ctk.W)
        files_label.configure(text="Arquivos disponíveis", font=("Arial", 20))

        header = [["#", "Nome", "Tipo", "Tamanho"]]

        self.table = CTkTable(master=files_frame, row=1, column=4, values=header,
                              command=self.row_clicked, corner_radius=10)
        self.table.pack(padx=20, pady=(10, 20), anchor=ctk.N)

        if self.table.rows == 1:
            self.no_file_label = ctk.CTkLabel(master=files_frame, text_color="gray",
                                              text="Conecte-se a um servidor para ver seus arquivos.")
            self.no_file_label.pack(pady=(10, 0), padx=20, anchor=ctk.N)

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
        self.CURRENT_SERVER_PORT = self.port_entry.get()

        self.ip_entry.configure(state="disabled")
        self.port_entry.configure(state="disabled")

        self.con_btn.configure(text="Conectado", state="disabled")
        self.discon_btn.configure(state="normal", fg_color="gray")

        self.no_file_label.pack_forget()
        
        self.update_file_table()

    def reset_server_info(self):
        self.ip_entry.configure(state="normal")
        self.port_entry.configure(state="normal")

        self.ip_entry.delete(0, "end")
        self.port_entry.delete(0, "end")

        self.con_btn.configure(text="Conecte-se a um servidor", state="normal")
        self.discon_btn.configure(state="disabled", fg_color="gray")

        self.CURRENT_SERVER_PORT = -1
        self.CURRENT_SERVER_IP = ""

        self.no_file_label.pack()
        
        self.erase_table()
        
        self.ip_entry.focus()

    def row_clicked(self, event):
        if event.get("row") == 0:
            return None

        # if event.get("row") > self.CURRENT_SERVER_FILE_COUNT + 1:
        #     return None

        for i in range(self.table.rows):
            self.table.deselect_row(i)

        self.table.select_row(event.get("row"))

    def update_file_table(self):
        self.erase_table()

        data = [["1", "file1", "txt", "1.2MB"],
                ["2", "file2", "jpg", "2.3MB"],
                ["3", "file3", "pdf", "3.4MB"],
                ["4", "file4", "png", "4.5MB"],
                ["5", "file5", "mp3", "5.6MB"]]

        # file_count = len(data)

        for i, row in enumerate(data):
            self.table.add_row(index=i + 1, values=row)

    def erase_table(self):
        self.table.delete_rows(range(1, self.table.rows))
        