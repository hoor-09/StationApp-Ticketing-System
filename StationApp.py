import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime

FARE_RATES={"Adult":2105,"Child":1410,"Senior":1025,"Student":1750}

STATIONS={
    "Central": ["Centrala", "Rede", "Yaen" ,"Ninia","Tallan","Jaund","Frestin","Lomil"],
    "Midtown": ["Rilya","Quthiel","Agralle","Stonyam","Obelyn","Riladia","Wicyt"],
    "Downtown": ["Zord","Keivia","Perinad","Erean","Brunad", "Elyot", "Adohad" ,"Holmer" , "Marend", "Ryall" ,"Ederif", "Pryn","Ruril" , "Vertwall"]
}

def calculate_fare(zones,travelers):
    total_fare=0
    breakdown={}
    for category,count in travelers.items():
        fare=zones*FARE_RATES[category]*count
        breakdown[category]=fare
        total_fare+=fare
    return total_fare,breakdown

class TravelApp:
    def __init__(self, root):
        self.root=root
        self.root.title("Centrala Underground Ticketing System")
        self.current_frame=None
        self.boarding_zone=tk.StringVar()
        self.destination_zone=tk.StringVar()
        self.travelers={
            "Adult":tk.IntVar(value=0),
            "Child":tk.IntVar(value=0),
            "Senior":tk.IntVar(value=0),
            "Student":tk.IntVar(value=0),
        }
        self.show_stations()

    def switch_frame(self,frame_func):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame=frame_func()
    def show_stations(self):
        frame=tk.Frame(self.root)
        frame.pack(fill="both",expand=True)

        tk.Label(frame,text="Stations Board", font=("Arial",16)).pack(pady=10)

        text_widget=tk.Text(frame,wrap=tk.WORD,height=15)
        for zone,stations in STATIONS.items():
            text_widget.insert(tk.END,f"{zone} Zone:{','.join(stations)}\n")
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(pady=10)

        tk.Button(frame,text="Next:Select Zones",command=lambda:self.switch_frame(self.select_zones)).pack(pady=5)
        self.current_frame=frame

    def select_zones(self):
        frame =tk.Frame(self.root)
        frame.pack(fill="both",expand=True)

        tk.Label(frame,text="Select Your Zones",font=("Arial",16)).pack(pady=10)

        tk.Label(frame,text="Boarding Zone:").pack()
        ttk.Combobox(frame,textvariable=self.boarding_zone,values=list(STATIONS.keys())).pack()

        tk.Label(frame,text="Destination Zone:").pack()
        ttk.Combobox(frame,textvariable=self.destination_zone,values=list(STATIONS.keys())).pack()

        tk.Button(frame,text="Next: Enter Traveler Details",command=lambda:self.switch_frame(self.enter_travelers)).pack(pady=5)
        tk.Button(frame,text="Back: Stations Board",command=lambda:self.switch_frame(self.show_stations)).pack(pady=5)
        self.current_frame=frame

    def enter_travelers(self):
        frame=tk.Frame(self.root)
        frame.pack(fill="both",expand=True)

        tk.Label(frame,text="Enter Number of Travelers",font=("Arial",18)).pack(pady=10)

        for category,var in self.travelers.items():
            tk.Label(frame,text=f"{category}:").pack()
            tk.Spinbox(frame,from_=0,to=10, textvariable=var).pack()

        tk.Button(frame,text="Next: Display Voucher",command=lambda:self.switch_frame(self.display_voucher)).pack(pady=5)
        tk.Button(frame,text="Back:Select Zones",command=lambda:self.switch_frame(self.select_zones)).pack(pady=5)
        self.current_frame=frame

    def display_voucher(self):
        frame=tk.Frame(self.root)
        frame.pack(fill="both",expand=True)

        boarding =self.boarding_zone.get()
        destination =self.destination_zone.get()
        zones=abs(list(STATIONS.keys()).index(boarding) - list(STATIONS.keys()).index(destination))

        travelers = {category: var.get() for category,var in self.travelers.items()}
        total_cost,breakdown=calculate_fare(zones,travelers)

        voucher_text=f"""
        TRAVEL VOUCHER
        Boarding Zone:{boarding}
        Destination Zone:{destination}
        Zones Traveled:{zones}

        Traveler Details:
        """
        for category,count in travelers.items():
            voucher_text += f"- {category}:{count} traveler(s)\n"

        voucher_text += "\nFare Breakdown:\n"
        for category, fare in breakdown.items():
            voucher_text +=f"-{category}: ${fare / 100:.2f}\n"

        voucher_text +=f"\nTotal Cost: ${total_cost/100:.2f}"

        text_frame= tk.Frame(frame)
        text_frame.pack(fill="both",expand=True, padx=10, pady=10)

        text_widget= tk.Text(text_frame,wrap="word",height=15)
        text_widget.insert("1.0",voucher_text)
        text_widget.config(state="disabled")
        text_widget.pack(side="left",fill="both",expand=True)

        scrollbar=tk.Scrollbar(text_frame,command=text_widget.yview)
        scrollbar.pack(side="right",fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        tk.Button(frame, text="Save Voucher",command=lambda:self.save_voucher(voucher_text)).pack(pady=5)
        tk.Button(frame, text="New Voucher",command=lambda:self.switch_frame(self.show_stations)).pack(pady=5)
        tk.Button(frame, text="Exit",command=self.root.quit).pack(pady=5)
        self.current_frame=frame

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()
