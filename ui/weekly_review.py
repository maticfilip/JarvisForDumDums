import customtkinter as ctk

class WeeklyReviewPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent",**kwargs)

        ctk.CTkLabel(self, text="Weekly Review", font=ctk.CTkFont(size=20, weight="bold")).pack(
            anchor="w", pady=(0,12)
        )
        ctk.CTkLabel(
            self, text="Lorem ipsum dolor sit amet et dictatorum et burundurum.", text_color="gray60", justify="left").pack(anchor="w", pady=(0,20))
        
        ctk.CTkButton(self, text="Generate review", width=160, command=self.generate).pack(
            anchor="w", pady=(0,16)
        )

        self.output_box=ctk.CTkTextbox(self, height=300, state="disabled")
        self.output_box.pack(fill="both", expand=True)

    def generate(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0","[LLM output will appear here ]")
        self.output_box.configure(state="disabled")

