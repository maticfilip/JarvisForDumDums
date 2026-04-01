import customtkinter as ctk
from core.habits import get_habits,get_last_7_days
from datetime import date

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
        for col, (val, label) in enumerate(stats):
            card=ctk.CTkFrame(stats_frame)
            card.grid(row=0, column=col, padx=(0,8) if col < 2 else 0, sticky="ew")
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=26, weight="bold")).pack(
                anchor="w", padx=14, pady=(12,0)
            )
            ctk.CTkLabel(
                card, text=label, font=ctk.CTkFont(size=12), text_color="gray60"
            ).pack(anchor="w",padx=14,pady=(0,12))


        log_card=ctk.CTkFrame(self)
        log_card.pack(fill="x", pady=(0,12))

        ctk.CTkLabel(
            log_card, text="QUICK LOG", font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w",padx=14, pady=(12,6))

        self.log_input=ctk.CTkTextbox(log_card, height=80, corner_radius=6)
        self.log_input.pack(fill="x",padx=14, pady=(0,8))
        self.log_input.insert("1.0","What are you working on?")

        btn_frame=ctk.CTkFrame(log_card, fg_color="transparent")
        btn_frame.pack(anchor="w", padx=14, pady=(0,12))
        ctk.CTkButton(btn_frame, text="Log entry", width=100, command=self.log_entry).pack(
            side="left", padx=(0,8)
        )
        ctk.CTkButton(
            btn_frame,
            text="Rubber duck",
            width=130, 
            fg_color="transparent",
            border_width=1,
            text_color=("gray10","gray90")
        ).pack(side="left")

        #-----------------#

        recent_card=ctk.CTkFrame(self)
        recent_card.pack(fill="x")

        ctk.CTkLabel(
            recent_card,
            text="RECENT JOURNAL ENTRIES",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12,6))

        entries=[
            ("2:35 PM", "Test test test Test test test Test test test ","bug fix"),
            ("2:35 PM", "Test test test Test test test Test test test ","bug fix"),
        ]

        for time, text,tag in entries:
            entry_frame=ctk.CTkFrame(recent_card, corner_radius=6)
            entry_frame.pack(fill="x", padx=14, pady=(0,8))

            ctk.CTkLabel(
                entry_frame, text=time, font=ctk.CTkFont(size=11), text_color="gray60"
            ).pack(anchor="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(
                entry_frame, text=text, wraplength=560, justify="left", font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=10, pady=(2, 4))
            ctk.CTkLabel(
                entry_frame,
                text=f"  {tag}  ",
                font=ctk.CTkFont(size=11),
                fg_color=("#DDDAFC", "#3D3780"),
                text_color=("#3D3780", "#DDDAFC"),
                # corner_radius=99,
            ).pack(anchor="w", padx=10, pady=(0, 8))

        #-----------------#

        todays_habits=ctk.CTkFrame(self)
        todays_habits.pack(fill="x")

        ctk.CTkLabel(
            todays_habits,
            text="Today's habits",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        ).pack(anchor="w", padx=14, pady=(12,6))

        today=str(date.today())
        raw_habits=get_habits()
        habits=[]
        for h in raw_habits:
            name=h["name"]
            history=h["history"]
            history_bools=get_last_7_days(h)
            history_bools=history_bools[:7]
            done_today=today in h["history"]
            habits.append((name, history_bools, done_today))

        for name, history, done_today in habits:
            row=ctk.CTkFrame(todays_habits, fg_color="gray17", corner_radius=8)
            row.pack(fill="x", padx=14,pady=(0,8))

            left=ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(
                left, text=name, font=ctk.CTkFont(size=13)
            ).pack(anchor="w")

            dots_frame=ctk.CTkFrame(left,fg_color="transparent")
            dots_frame.pack(anchor="w",pady=(4,0))

            for did in history:
                color="#534AB7" if did else "gray30"
                dot=ctk.CTkFrame(
                    dots_frame,
                    width=8, height=8,
                    corner_radius=2,
                    fg_color=color
                )
                dot.pack(side="left", padx=(0,3))
                dot.pack_propagate(False)


            check_color="#534AB7" if done_today else "gray30"
            check=ctk.CTkFrame(
                row,
                width=22,height=22,
                corner_radius=11,
                fg_color=check_color,
                border_width=0
            )

            check.pack(side="right", padx=14)
            check.pack_propagate(False)

            if done_today:
                ctk.CTkLabel(
                    check, text="✓",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="white"
                ).place(relx=0.5,rely=0.5, anchor="center")



        #-----------------#

        

    def log_entry(self):
        text=self.log_input.get("1.0","end").strip()
        if text:
            print(f"[LOG] {text}")

    

