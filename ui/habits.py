import customtkinter as ctk
from core import add_habit, get_habits, delete_habit

class HabitsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent",**kwargs)
        self.build_habit_list()

        ctk.CTkLabel(
            self, text="TODAY'S HABITS", font=ctk.CTkFont(size=11), text_color="gray60").pack(anchor="w", pady=(0,10))
        
        #---------------------#
        
        add_card=ctk.CTkFrame(
            self
        )
        add_card.pack(fill="x", pady=(0,16))

        ctk.CTkLabel(
            add_card, text="Here you can add a new habit that you want to implement in your daily life.",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        ).pack(anchor="w",padx=14, pady=(12,6))
        
        self.habit_input=ctk.CTkTextbox(add_card, height=80, corner_radius=6)
        self.habit_input.pack(fill="x",padx=14,pady=(8,8))
        self.habit_input.insert("1.0","A new habit starts with a single step")

        btn_habit=ctk.CTkFrame(add_card, fg_color="transparent")
        btn_habit.pack(anchor="w", padx=14, pady=(0,12))
        ctk.CTkButton(btn_habit, text="Accept", width=100, command=self.save_habit).pack(
            side="left", padx=(0,8)
        )


        #----------------------#

    def build_habit_list(self):
        for row in getattr(self, "habit_rows",[]):
            row.destroy()
        self.habit_rows=[]

        habits=get_habits()

        for habit in habits:
            name = habit['name']
            created = habit['created']
            done = len(habit['history']) > 0  
            row=ctk.CTkFrame(self)
            row.pack(fill="x", pady=(0,8))

            ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=14)).pack(
                side="left", padx=14, pady=12
            )
            ctk.CTkButton(
                row, text="Delete", fg_color="transparent",border_width=1, text_color="gray60",hover_color="gray25",command=lambda n=name: self.remove_habit(n)
            ).pack(side="right",padx=(0,4), pady=8)

            check=ctk.CTkCheckBox(row, text="Mark as done for today", width=24)
            if done:
                check.select()
            check.pack(side="right", padx=14)
            self.habit_rows.append(row)


    def save_habit(self):
        text=self.habit_input.get("1.0","end").strip()

        if not text or text=="A new habit starts with a single step":
            return
        
        add_habit(text)

        self.habit_input.delete("1.0","end")
        self.habit_input.insert("1.0","A new habit starts with a single step")

        self.build_habit_list()
            
    def remove_habit(self, name:str):
        delete_habit(name)
        self.build_habit_list()