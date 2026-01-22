"""
This program takes input through a GUI to control the peristaltic pump
This code is still in-progress
Part of this code was copied and modified from the Custom Tkinter example image_example.py by 
Tom Schimansky https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/image_example.py
"""

"""
TODO:
    exception handling for invalid input or grey out start button
    handle when pump needs to be on for longer than interval
    
    exception handling may not be as necessary with validate input entry methods
    
   entry wont let delete the first entered number

    
"""

import customtkinter
import os
from PIL import Image
#import pump_control_timed as pc
from pump_control_timed import PumpControlTimed as Pct
import threading

"""
Interface for peristaltic pump control
Some code copied from the Cutstom Tkinter example page
"""
class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.run_time = 600
        self.interval = 60
        self.sample_vol = 200
        self.rate = .38
        
        #creates a thread event for stopping the loop
        self.stop_event = threading.Event()
        self.thread = None

        self.title("image_example.py")
        self.geometry("800x450")

        # set grid layout one row, 2 columns 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight = 1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Pump Control",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        #self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                #command=self.change_appearance_mode_event)
        #self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create frame for pump control
        self.pump_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pump_frame.grid_columnconfigure(0, weight=1)
        self.pump_frame.grid_columnconfigure(1, weight=1)
        self.pump_frame.grid_columnconfigure(2, weight=1)
        
        #run time section
        self.runtime_label = customtkinter.CTkLabel(self.pump_frame, text="Run Time", fg_color="transparent", font = ("Arial", 20) )
        self.runtime_label.grid(row = 0, column = 0, padx=10, pady=10)
        
        self.radio_var_runtime = customtkinter.IntVar(value=1) #value is a window object?
        self.radio_var_interval = customtkinter.IntVar(value=2)
        self.radio_var_vol = customtkinter.IntVar(value=3)
        
        self.radiobutton_7day = customtkinter.CTkRadioButton(self.pump_frame, text="7 Days", command=self.radiobutton_runtime_event, 
                                                             variable= self.radio_var_runtime, value=604800, font = ("Arial",15))
        self.radiobutton_7day.grid(row = 3, column = 0, padx = 10, pady = 10)    ,
        self.radiobutton_1h = customtkinter.CTkRadioButton(self.pump_frame, text="1 Hour", command=self.radiobutton_runtime_event,
                                                           variable= self.radio_var_runtime, value=3600, font = ("Arial",15))
        self.radiobutton_1h.grid(row = 2, column = 0, padx = 10, pady = 10)  
        self.radiobutton_10min = customtkinter.CTkRadioButton(self.pump_frame, text="10 Minuets", command=self.radiobutton_runtime_event, 
                                                              variable= self.radio_var_runtime, value=600, font = ("Arial",15))
        self.radiobutton_10min.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.radiobutton_other = customtkinter.CTkRadioButton(self.pump_frame, text="Other (sec)", command=self.radio_other_runtime_event, 
                                                              variable= self.radio_var_runtime, value=0, font = ("Arial",15))
        self.radiobutton_other.grid(row = 4, column = 0, padx = 10, pady = 10) 
        self.radio_var_runtime.set(600) #sets default selection
        self.other_runtime_input = customtkinter.CTkEntry(self.pump_frame, width=100)
        
        #sampling interval section
        self.vol_label = customtkinter.CTkLabel(self.pump_frame, text="Sampling Interval", fg_color="transparent", font = ("Arial", 20))
        self.vol_label.grid(row = 0, column = 1, padx=10, pady=10)
        self.radiobutton_1min = customtkinter.CTkRadioButton(self.pump_frame, text="1 Minuet", command=self.radio_interval_event, 
                                                             variable= self.radio_var_interval, value=60, font = ("Arial",15))
        self.radiobutton_1min.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.radiobutton_1h = customtkinter.CTkRadioButton(self.pump_frame, text="1 Hour", command=self.radio_interval_event, 
                                                           variable= self.radio_var_interval, value=3600, font = ("Arial",15), state = "disabled")
        self.radiobutton_1h.grid(row = 2, column = 1, padx = 10, pady = 10)  
        self.radiobutton_other = customtkinter.CTkRadioButton(self.pump_frame, text="Other (sec)", command=self.radio_other_interval_event,
                                                              variable= self.radio_var_interval, value=1, font = ("Arial",15))
        self.radiobutton_other.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.radio_var_interval.set(60) #sets default selection
        self.other_interval_input = customtkinter.CTkEntry(self.pump_frame, width = 100)
        
        #sample volume section
        self.vol_label = customtkinter.CTkLabel(self.pump_frame, text="Sample Volume", fg_color="transparent",  font = ("Arial", 20))
        self.vol_label.grid(row = 0, column = 2, padx=10, pady=10)
        self.radiobutton200 = customtkinter.CTkRadioButton(self.pump_frame, text="200uL", command = self.radio_vol_event, 
                                                           variable=self.radio_var_vol,value = 200, font = ("Arial",15))
        self.radiobutton200.grid(row = 1, column = 2, padx=10, pady=10)
        self.radiobutton_1ml = customtkinter.CTkRadioButton(self.pump_frame, text="1mL", command = self.radio_vol_event, 
                                                            variable=self.radio_var_vol,value = 1000, font = ("Arial",15))
        self.radiobutton_1ml.grid(row = 2, column = 2, padx=10, pady=10)
        self.radiobutton_other = customtkinter.CTkRadioButton(self.pump_frame, text="Other (uL)", command = self.radio_other_vol_event, 
                                                              variable=self.radio_var_vol, value=1, font = ("Arial",15))
        self.radiobutton_other.grid(row = 3, column = 2, padx=10, pady=10)
        self.radio_var_vol.set(200)
        self.other_vol_input = customtkinter.CTkEntry(self.pump_frame, width = 100)
        
        #rate section
        self.rate_label = customtkinter.CTkLabel(self.pump_frame, text = "Rate", padx = 10, pady = 10, fg_color = "transparent", font = ("Arial", 20))
        self.rate_label.grid(row = 0, column = 3)
        self.rate_entry = customtkinter.CTkEntry(self.pump_frame,  width = 100, border_color = "black")
        self.rate_entry.bind("<Return>", self.rate_entry_event)
        self.rate_entry.grid(row = 2, column = 3, padx = 10, pady = 10)
        self.rate_val_label = customtkinter.CTkLabel(self.pump_frame, text = ("Rate:", self.rate, "mL/s"), padx = 10, pady = 10, 
                                                     fg_color = "transparent", font = ("Arial", 15))
        self.rate_val_label.grid(row = 1, column = 3,  padx = 10, pady = 10)
        
        #start button
        self.start_button = customtkinter.CTkButton(self.pump_frame, text="Start", 
                                                    command= lambda : self.button_start(app, pump_control), font = ("Arial",20)) #don't know how it works, but lambda prevents from start activating on run
        self.start_button.grid(row=6, column=1, padx=10, pady=10, columnspan = 2, sticky='EW')
        #stop button
        self.stop_button = customtkinter.CTkButton(self.pump_frame, text="Stop", command=self.button_click, font = ("Arial",20))
        self.stop_button.grid(row=7, column=1, padx=10, pady=10, columnspan = 2, sticky='EW')

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.pump_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.pump_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
     # add methods to app
    
    #can I customize what this does for each radio button based on unique value outputs from each?
    def radiobutton_runtime_event(self):
        print("radiobutton toggled, current value:", self.radio_var_runtime.get() )
        self.run_time = self.radio_var_runtime.get()
        if(self.run_time == 600 or 3600):
            self.radiobutton_1h.configure(state = "disabled")
        if(self.run_time == 604800):
            self.radiobutton_1h.configure(state = "normal")
      
    def radio_other_runtime_event(self):
        self.enable_entry(self.other_runtime_input)
        self.other_runtime_input.grid(row = 5, column = 0, padx = 10, pady = 0)
        self.other_runtime_input.bind("<Return>", self.submit_runtime_val)
        self.radiobutton_1h.configure(state = "normal")
    
    def submit_runtime_val(self, val): #what is val?
        self.run_time = float(self.other_runtime_input.get())
        self.disable_entry(self.other_runtime_input)
        print("runtime radio val is", self.run_time)
        
    def radio_interval_event(self):
        self.interval = self.radio_var_interval.get()
        self.disable_entry(self.other_interval_input)
        print("interval radio val is", self.interval)
        
    def radio_other_interval_event(self):
        self.enable_entry(self.other_interval_input)
        self.other_interval_input.grid(row = 4, column = 1, padx = 10, pady = 0)
        self.other_interval_input.bind("<Return>", self.submit_interval_val)
        
    def submit_interval_val(self, val):
        self.interval = float(self.other_interval_input.get())
        self.disable_entry(self.other_interval_input)
        print("interval radio val is", self.interval)
        
    def radio_vol_event(self):
        print("volume radio pressed, value is", self.radio_var_vol.get())
        self.sample_vol = self.radio_var_vol.get()
    
    def radio_other_vol_event(self):
        self.enable_entry(self.other_vol_input)
        self.other_vol_input.grid(row = 4, column = 2, padx=10, pady=0 )
        self.other_vol_input.bind("<Return>", self.submit_vol_val)
        
    def submit_vol_val(self, val):
        self.sample_vol = float(self.other_vol_input.get())
        #self.other_vol_input.configure(fg_color = "grey")
        self.disable_entry(self.other_vol_input)
        print("sample vol radio val is", self.sample_vol)
        
    def rate_entry_event(self, val):
        
        self.rate = float(self.rate_entry.get())
        self.rate_val_label.configure(text = ("rate:", self.rate, "mL/s"))
        print("rate changed to",self.rate)  
    
    def button_start(self, app, pump):
        #if thread is already running  exit out of function
        if app.thread and app.thread.is_alive():
            return  
        
        #clears stop event if there is one from previous stop
        app.stop_event.clear()
        #creates a thread that points to the function with the for loop and passes argugments app and pump
        app.thread = threading.Thread(target=app.runPumpLoop, args=(app, pump), daemon=True)
        
        print("start pressed\n")
        print("values are: run time", app.run_time,"interval", app.interval, "volume", app.sample_vol, "rate", app.rate)
        #sets all of the necessary values based on user input
        pump.set_vals(app.run_time, app.interval, app.sample_vol, app.rate)
        #throws exceptions if user input is not valid
        pump.validate_input()
        #prints start and end times
        pump.print_time()
        
        #starts an external thread to run the for loop so the GUI doesn't freeze
        app.thread.start()
        app.start_button.configure(state = "disabled")
        
        #app.start_button.configure(state = "normal")
    
    def button_click(self):
        print("stop button click")
        #self.stop = True
        self.stop_event.set()
        pump_control.end_run()
        
        self.start_button.configure(state = "normal")
                   
        #check for valid parameters or only activate start when everything is entered
        #can i just sent values from the interface to built code?
        #disable changes to options
        #run the main code
        #pump_control_timed.runStart(self, self.run_time, self.interval, self.sample_vol)  
    
    # grays out and disables an entry box. The entry box variable is passed in through entry
    def disable_entry(self, entry):
         entry.configure(insertontime = 0)
         entry.configure(state = "disabled")
         entry.configure(fg_color = "gray80")
   # returns the entry box to white and allows for input
    def enable_entry(self, entry):
        entry.configure(insertontime = 1000)
        entry.configure(state = "normal")
        entry.configure(fg_color = "white")
        
    def doNothing():
        pass
    
    def close(self):
        self.destroy()
    
    # this method is called by entry boxes.
    # if the input/val can be a float and is >=0
    # The user can input the value
    def validate_entry(val):
        try:
            if float(val) >= 0:
                return True
        except ValueError:
            return False
    
    #threaded method
    def runPumpLoop(self, app, pump):
        #disables exiting the window through the x button while thread is running
        app.protocol("WM_DELETE_WINDOW", lambda : None)
        #iterates how many times the given interval fits in the given run time - 1
        stop = False
        for i in range(int(pump.run_time / pump.interval) - 1):
            # If the stop button is pressed and the stop_event gets set, 
            # the for loop is broken out of and the thread finishes
            if(self.stop_event.is_set()):
                stop = True
                break
            else: 
                #turns pump on
                pump.write_to(pump.to_arduino)
                print("sent", pump.to_arduino, "to arduino at ", Pct.print_current_time())
                # if stop event triggered within time frame returns true, otherwise returns false
                # keeps pump on for time unless stop event triggered
                if(self.stop_event.wait(pump.pump_on)): 
                    break     
                pump.write_to(0)
                print("sent 0 to arduino at", Pct.print_current_time())
                #waits for time unless stop event triggered
                if(self.stop_event.wait(pump.wait_time)): 
                    break
        if not stop:
            pump.run_last() 
        #Resets the GUI from thread
        app.button_click()
        # enables exiting out again once thread it done running
        app.protocol("WM_DELETE_WINDOW", app.close)
    
if __name__ == "__main__":
    #creates a custom tkinter object
    app = App()
    #create object for pump control
    pump_control = Pct()
    reg = app.register(App.validate_entry)
    app.rate_entry.configure(validate="key", validatecommand=(reg, '%P'))
    app.other_vol_input.configure(validate="key", validatecommand=(reg, '%P'))
    app.other_interval_input.configure(validate="key", validatecommand=(reg, '%P'))
    app.other_runtime_input.configure(validate="key", validatecommand=(reg, '%P'))
    try:#doesn't work for input validation because exception doesnt bubble up to mainloop. 
        #opens GUI
        app.mainloop()
        app.stop_event.set()
        #when GUI is closed stops pump and closes the serial port
        pump_control.end_run()
        pump_control.close_serial()
        
    except (KeyboardInterrupt):
        print("keyboard interrupt")
        pump_control.end_run()
        pump_control.close_serial()
        app.destroy()
   