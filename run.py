from Project.MemoryClass.MemoryClass_model import mc

import tkinter
from tkinter import filedialog, StringVar


#TKINTER INITIATION + CONFIGURATION:
window = tkinter.Tk()
window.title("two phase analyser")
window.geometry('300x200')
window.configure(bg='#333333')
button_frame  =  tkinter.Frame(window,  width=200,  height=50,  bg='#333333')


#declaring stringvar values to be used later in labels:
text_label_number_experiments = StringVar()
text_label_number_gels = StringVar()
text_status = StringVar()

def select_directory():
    """tkinter event handling function that first asks user to select a directory. Then loads all files from that directory and does first calculations.
    """
    #label_status is used to warn the user that the operation will take some time
    label_status.config(bg = "red")
    text_status.set("Please wait... Loading in progress...")

    #dialog for selecting a directory
    folder_selected = filedialog.askdirectory()

    try:
        #load all files into memoryclass (created experimentdata lists with iondata lists)
        mc.load_from_directory(folder_selected + "/")
        #first calculations for memoryclass
        mc.set_ionnames_gels_peakdata_Eset()
        #give user feedback and update label_status
        text_label_number_experiments.set(f"Number of experimentdata's succefully loaded: {len(mc.listExperimentData)}")
        text_label_number_gels.set(f"Number of gels in dataset: {len(mc.listGelatinNames)}")
        label_status.config(bg='#333333')
        text_status.set("")
        window.update_idletasks()
    except:
        tkinter.messagebox.showerror("showerror", "could not read files from this directory")
        label_status.config(bg='#333333')
        text_status.set("")
        window.update_idletasks()


def create_excel():
    """tkinter event handling function to create the two-peak excel
    """
    #label_status is used to warn the user that the operation will take some time
    label_status.config(bg = "red")
    text_status.set("Please wait... Creating excel in progress...")
    window.update_idletasks()
    #check that there are experimentdatas loaded:
    if len(mc.listExperimentData) > 0:
        try:
            mc.make_excel()
            #give user feedback and update label_status
            tkinter.messagebox.showinfo("showinfo", "Excel succefully created!")
            label_status.config(bg='#333333')
            text_status.set("")
            window.update_idletasks()
        except:
            tkinter.messagebox.showerror("showerror", "error while creating excel!")
            label_status.config(bg='#333333')
            text_status.set("")
            window.update_idletasks()
    else:
        #give user feedback and update label_status
        tkinter.messagebox.showerror("showerror", "please load experiment data's before you make the excel!")
        label_status.config(bg='#333333')
        text_status.set("")
        window.update_idletasks()


#tkinter: initialise elements that will become widgets
label_status = tkinter.Label(window, textvariable=text_status, pady= 10, bd=5, bg='#333333', fg="white")
btn_select_directory = tkinter.Button(button_frame, text ="select directory", command=select_directory, pady= 10, 
                                      bd=5,bg='#333333', fg="white")
label_number_experiments = tkinter.Label(window, textvariable=text_label_number_experiments, pady= 10, bd=5,bg='#333333',fg="white")
label_number_gels = tkinter.Label(window, textvariable=text_label_number_gels, pady= 10, bd=5,bg='#333333',fg="white")
btn_create_excel = tkinter.Button(button_frame, text ="create excel", command=create_excel, pady= 10, bd=5,bg='#333333',fg="white")

#tkinter: set initial values for labels
text_status.set("Status bar... no calculations in progress... ")
text_label_number_experiments.set(f"Number of experimentdata's succefully loaded: {len(mc.listExperimentData)}")
text_label_number_gels.set(f"Number of gelatins succefully loaded: {len(mc.listGelatinNames)}")

#tkinter: create widgets in window
label_status.pack()
button_frame.pack()
btn_select_directory.pack(side = "left")
label_number_experiments.pack()
label_number_gels.pack()
btn_create_excel.pack(side="right")



if __name__ == "__main__":
    #tkinter: start window loop
    window.mainloop()


    