import threading
import tkinter as tk
import traceback
from functools import partial
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename

import logic


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("D.I.D.A.R.S.C.P.G.U.I.")
        self.geometry("720x350")

        self.init_UI()

        self.inputs = {}

    def init_UI(self):
        # Create a frame for the buttons
        frame = ttk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)

        # create a label - select folder
        label_1 = ttk.Label(frame, text="Select a folder containing files to process:")
        label_1.grid(row=0, column=0, sticky="w", padx=10)

        # create a button - select folder
        button = ttk.Button(frame, text="Select Folder", command=partial(self.select_folder, "folder_containing_files"))
        button.grid(row=0, column=1, sticky="w")

        # --------------------------------------
        # create a label - enter mass tolerance
        label_2 = ttk.Label(frame, text="Enter mass tolerance in Da - recommended 0.002 for FT / 0.005 for TOF:")
        label_2.grid(row=1, column=0, sticky="w", padx=10)

        # create a entry - enter mass tolerance
        self.entry_1 = ttk.Entry(frame)
        self.entry_1.grid(row=1, column=1, sticky="w")

        # --------------------------------------
        # create label - Enter minimum number of diagnostic ions
        label_3 = ttk.Label(frame, text="Enter minimum number of diagnostic or reporter ions:")
        label_3.grid(row=2, column=0, sticky="w", padx=10)

        # create a entry - Enter minimum number of diagnostic ions
        self.entry_2 = ttk.Entry(frame)
        self.entry_2.grid(row=2, column=1, sticky="w")

        # --------------------------------------
        # create a label - Select reporter file
        label_4 = ttk.Label(frame, text="Select reporter file:")
        label_4.grid(row=3, column=0, sticky="w", padx=10)

        # create a button - select reporter file
        button_2 = ttk.Button(frame, text="Select File", command=partial(self.select_file, "reporter_file"))
        button_2.grid(row=3, column=1, sticky="w")

        # --------------------------------------
        # create a label - Select Glyco file
        label_5 = ttk.Label(frame, text="Select Glyco file:")
        label_5.grid(row=4, column=0, sticky="w", padx=10)

        # create a button - select Glyco file
        button_3 = ttk.Button(frame, text="Select File", command=partial(self.select_file, "glyco_file"))
        button_3.grid(row=4, column=1, sticky="w")

        # --------------------------------------
        # submit button
        button_4 = ttk.Button(frame, text="QC your SCP files!", command=self.submit)
        button_4.grid(row=5, column=1, sticky="w", pady=10)

        # --------------------------------------
        # create a label - output
        self.label_output = ttk.Label(frame, text="Output:")
        self.label_output.grid(row=6, column=0, sticky="ews", padx=10, columnspan=2)

        # configure the column and row grid
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        for i in range(6):
            frame.rowconfigure(i, weight=1)

    def select_folder(self, key: str):
        folder = askdirectory()
        if folder:
            self.inputs[key] = folder
            print(self.inputs)

    def select_file(self, key: str):
        file = askopenfilename()
        if file:
            self.inputs[key] = file
            print(self.inputs)

    def submit(self):
        working_directory = self.inputs["folder_containing_files"]
        try:
            mass_tolerance = float(self.entry_1.get())
        except ValueError:
            self.show_output("Please enter a valid mass tolerance")
            return
        try:
            min_num_diag_ions = int(self.entry_2.get())
        except ValueError:
            self.show_output("Please enter a valid number for the minimum number of diagnostic ions")
            return

        reporter_file = self.inputs["reporter_file"]
        glyco_file = self.inputs["glyco_file"]

        if not all((working_directory, mass_tolerance, reporter_file, glyco_file)):
            self.show_output("Please fill all fields before submitting")
            return

        # use threadpool executor to show output after processing is done
        threading.Thread(target=self.execute, args=(working_directory, reporter_file, glyco_file, mass_tolerance,
                                                    min_num_diag_ions)).start()

    @staticmethod
    def show_message(message: str):
        tk.messagebox.showinfo("Message", message)

    def show_output(self, output: str):
        self.label_output.configure(text=output)

    def execute(self, *args):
        try:
            output = logic.run(*args)
            self.show_output(output)
        except Exception as e:
            self.show_output(traceback.format_exc())


if __name__ == '__main__':
    w = Window()
    w.mainloop()
