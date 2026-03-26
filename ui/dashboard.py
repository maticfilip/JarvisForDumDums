import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent",**kwargs)

        stats_frame=ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0,12))
        stats_frame.grid_columnconfigure((0,1,2),weight=1)

        stats=[
            ("12","Journal entries this week"),
            ("4/5", "Habits done today"),
            ("14","Day streak")
        ]
        # for col, (val, label) in enumerate(stats):

