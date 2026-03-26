import customtkinter as ctk
from datetime import datetime

from journal import JournalPage
from dashboard import DashboardPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#.........sidebar............#

class NavButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            anchor="w",
            fg_color="transparent",
            text_color=("gray60","gray60"),
            hover_color=("gray85","gray25"),
            corner_radius=6,
            height=36,
            **kwargs,
        )

    def set_active(self, active:bool):
        if active:
            self.configure(
                fg_color=("gray80","gray20"),
                text_color=("gray10","white"),
                font=ctk.CTkFont(weight="bold")
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=("gray60","gray60"),
                font=ctk.CTkFont(weight="normal")
            )

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x620")
        self.minsize(800,500)
        self.title("Helper for stupid developers like me")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main()

        self.show_page("dashboard")


    def build_sidebar(self):
        self.sidebar=ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Dev Assistant",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(24,20), padx=16, anchor="w")

        self.nav_buttons:dict[str, NavButton]={}

        nav_items=[
            ("dashboard"," Dashboard"),
            ("journal", " Journal"),
            ("habits", " Habits"),
            ("review", " Weekly Review")
        ]
        
        for key, label in nav_items:
            btn=NavButton(
                self.sidebar,
                text=label,
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key]=btn

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").pack(
            fill="x", padx=10, pady=12, side="bottom"
        )

        NavButton(self.sidebar, text=" Settings", command=lambda: None).pack(
            fill="x", padx=10, pady=(0,12), side="bottom"
        )

    def build_main(self):
        self.main_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.topbar=ctk.CTkFrame(self.main_frame, height=52, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        self.page_title_label=ctk.CTkLabel(
            self.topbar, text="Dashboard", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.page_title_label.pack(side="left", padx=20, pady=14)

        self.content_area=ctk.CTkScrollableFrame(
            self.main_frame, corner_radius=0, fg_color="transparent"
        )
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=16)
        self.content_area.grid_columnconfigure(0, weight=1)


        self.pages:dict[str,ctk.CTkFrame]={
            "dashboard":DashboardPage(self.content_area),
            "journal":JournalPage(self.content_area),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")



    def show_page(self, key:str):
        titles={
            "dashboard":"Dashboard",
            "journal":"Journal",
            # "habits":"Habits",
            # "review":"Weekly Review"
        }

        self.page_title_label.configure(text=titles.get(key,key.title()))

        for k, btn in self.nav_buttons.items():
            btn.set_active(k==key)

        self.pages[key].tkraise()


if __name__=="__main__":
    app=App()
    app.mainloop()
