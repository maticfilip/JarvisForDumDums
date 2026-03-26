import customtkinter as ctk

class JournalPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text="Journal — coming soon", font=ctk.CTkFont(size=16)).pack(pady=40)