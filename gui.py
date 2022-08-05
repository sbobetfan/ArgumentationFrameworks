from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from copy import deepcopy
import grounded_labelling
import preferred_labelling
import framework
import save_framework
import open_framework

# initialise counters and records
graph_index = 0
all_graphs=[]
# dimensions of main window
window_width = 600
window_height = 900

all_relations = []
all_args = set()
favoured_preferences = []

# global flags
try_to_open = False
done_pressed = False
arg1_entered = False
arg2_entered = False

# Called when the Add Relation Button is pressed
def add_relation():
    global try_to_open, all_relations_after_preferences, arg1_entered, arg2_entered
    if try_to_open:
        argA = from_ent
        argB = to_ent
    else:
        argA = from_entry.get()
        argB = to_entry.get()

    if not argA or not argB or not arg1_entered or not arg2_entered:
        entry_output = "INVALID ENTRY"

    else:
        # duplicates ignored
        all_args.add(argA)
        all_args.add(argB)

        if (argA, argB) not in all_relations:
            all_relations.append((argA, argB))
            if done_pressed:
                all_relations_after_preferences.append((argA, argB))

            entry_output = argA + u" \u2192 " + argB
        else:
            entry_output = "Duplicate Entry - Will be ignored"
            print("Duplicate Entry - Will be ignored")
        # display relation in output box

        f = framework.create_graph(all_relations, [{},{},{}], [])
        add_to_canvas(f, graph_frame)

    output_msg(entry_output)
    print("Relation: %s" % (entry_output))
    arg1_entered = False
    arg2_entered = False

# Positions the window in the center of the screen
def center(window, w, h):
    # get screen width and height
    ws = window.winfo_screenwidth() # width of the screen
    hs = window.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

# Configure how each output message is displayed
def output_msg(msg):
    Output.configure(state="normal")
    Output.insert(END, msg + "\n")
    Output.configure(state="disabled")
    Output.see("end")

# Configure how each framework is displayed
def add_to_canvas(graph, frame):
    global canvas, graph_index, all_graphs
    try:
        canvas.get_tk_widget().pack_forget()
    except:
        pass
    canvas = FigureCanvasTkAgg(graph, frame)
    canvas.get_tk_widget().pack()
    update_displaying_message(graph_index+1, len(all_graphs))

# Hide and Show Button methods
def hide_button(button):
    button.grid_forget()
def show_button(button, button_type):
    # print(button)
    if button_type ==1:
        button.grid(row=1, column=0)
    elif button_type ==2:
        button.grid(row=1, column=1)

# Show the Next button
def show_next():
    global all_graphs, graph_index
    graph_index += 1
    add_to_canvas(all_graphs[graph_index], graph_frame)
    if graph_index==len(all_graphs)-1:
        # reached end
        # remove next button
        hide_button(next_btn)
    if graph_index ==1:
        # moved along by 1, so add option to go back again
        # add previous button
        show_button(previous_btn, 1)

# Show the Previous Button
def show_prev():
    global all_graphs, graph_index
    graph_index -= 1
    add_to_canvas(all_graphs[graph_index], graph_frame)
    if graph_index ==0:
        # at start of list
        # remove previous button
        hide_button(previous_btn)
    if graph_index==len(all_graphs)-2:
        # there is a graph ahead
        # add next button
        show_button(next_btn, 2)

# Called when the Done button is pressed
def done_btn_pressed():
    global all_relations_after_preferences, done_pressed
    done_pressed = True
    all_relations_after_preferences = deepcopy(all_relations)
    print("done btn pressed")
    if not all_args:
        output_msg("EMPTY FRAMEWORK!")
        print("Denied: Generate Labelling for Empty Framework")
        open_btn.config(state=NORMAL)
        return
    done_btn.pack_forget()
    add_arg_preferences_btn.pack(side = TOP)
    grounded_compute_btn.pack(side = LEFT, pady = 10)
    preferred_compute_btn.pack(side = LEFT, pady = 10)

# Configure the message shown after framework appears
def update_displaying_message(num1, num2):
    for widget in graph_label_frame.winfo_children():
        widget.destroy()
    if num2 ==0:
        disp_label = Label(graph_label_frame, text="Displaying Framework:")
    else:
        disp_label = Label(graph_label_frame, text="Displaying generated labelling %s of %s:" %(num1, num2))
    disp_label.pack()

# What to do when a window closes
def on_closing(window, btn):
    btn.config(state=NORMAL)
    window.destroy()

# Main method called to compute the grounded or preferred labellings
def compute_labelling(selected_semantics):
    global canvas, framework_generated, all_graphs, graph_index, all_relations_after_preferences, favoured_preferences
    all_graphs = []
    graph_index = 0
    hide_button(previous_btn)
    hide_button(next_btn)

    try:
        canvas.get_tk_widget().pack_forget()
    except:
        pass
    # 1 = grounded, 2 = preferred
    if selected_semantics == 1:
        output_msg("Generating Grounded Labelling...")
        framework_generated = True
        labelling = grounded_labelling.compute_labelling(all_relations_after_preferences, all_args)
    else:
        output_msg("Generating Preferred Labelling(s)...")
        framework_generated = True
        labelling = preferred_labelling.compute_labelling(all_relations_after_preferences, all_args)

    output_msg("Done")
    if all_relations_after_preferences != all_relations:
        output_msg("-------------------------------------")
        output_msg("NOTE: Argument Preferences remain \n      until reset.")
        output_msg("")
        output_msg("See option above to Reset Argument \nPreferences.")
        output_msg("-------------------------------------")


    for l in labelling:
        f = framework.create_graph(all_relations_after_preferences, l, favoured_preferences)
        all_graphs.append(f)
    print("All graphs successfully generated.")
    print(len(all_graphs))

    add_to_canvas(all_graphs[0], graph_frame)

    if len(all_graphs)>1:
        # add next button
        show_button(next_btn,2)

# Called when the Reset button is pressed
def reset_window():
    global all_relations, all_args, all_graphs, graph_index
    all_graphs = []
    graph_index = 0
    clear_box(from_entry, to_entry)

    done_btn.pack()
    reset_btn_text()
    add_arg_preferences_btn.pack_forget()
    grounded_compute_btn.pack_forget()
    preferred_compute_btn.pack_forget()
    # clear outputs currently displayed
    Output.configure(state="normal")
    Output.delete("1.0", END)
    Output.configure(state="disabled")
    for widget in graph_label_frame.winfo_children():
        widget.destroy()
    try:
        global canvas
        canvas.get_tk_widget().pack_forget()
    except:
        pass

    all_relations = []
    all_args = set()
    hide_button(previous_btn)
    hide_button(next_btn)
    from_entry.focus()

    print("======================== RESET ========================")

# Called when the Save button is pressed
def save(window, filename):
    if save_framework.save(all_relations, filename):
        output_msg("Framework Saved")
        window.destroy()
        save_btn.config(state=NORMAL)

# Displays the small Save Framework window
def get_save_name():
    if not all_args:
        output_msg("EMPTY FRAMEWORK!")
        save_btn.config(state=NORMAL)
        return

    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)
    center(newWindow, 200, 200)
    # sets the title of the
    # Toplevel widget
    newWindow.title("Save Framework")
    newWindow.resizable(False, False)

    # handle the user pressing the red x (close window)
    newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(newWindow, save_btn))

    # User instructions to enter title
    Label(newWindow,
          text ="Enter Framework Title").pack()

    # Text box
    usr_save_entry = Entry(newWindow, width=15)
    usr_save_entry.pack()

    save_btn1 = Button(newWindow,
            text="Save",
            command=lambda: save(newWindow, usr_save_entry.get()))
    save_btn1.pack()

# Called during the Open Framework process
def get_file(counter, window):
    global from_ent, to_ent, try_to_open, arg1_entered, arg2_entered
    reset_window()
    file = open_framework.get_file(counter)
    parts = file.split("\n")
    for line in parts:
        try:
            entry=line.split("->")
            from_ent = entry[0]
            to_ent = entry[1]
            try_to_open = True
            arg1_entered = True
            arg2_entered = True
            add_relation()
            try_to_open = False
            arg1_entered = False
            arg2_entered = False

        except:
            pass
    open_btn.config(state=NORMAL)
    window.destroy()


def open_fw():
    files = open_framework.get_files()

    if len(files) == 0:
        print("Open Framework Denied: No frameworks found")
        output_msg("NO FRAMEWORKS FOUND")
        open_btn.config(state=NORMAL)
        return
    newWindow = Toplevel(master)
    center(newWindow, 400, 400)

    newWindow.title("Open Framework")
    newWindow.resizable(False, False)

    newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(newWindow, open_btn))

    # User instructions to enter title
    Label(newWindow,
          text ="Frameworks Found:").pack()

    for file in files:
        # add a button for each file
        open_file_btn = Button(newWindow,
                text=file[2] + " " + file[0] + " " + file[1],
                command=lambda i=file[3]: get_file(i, newWindow))
        open_file_btn.pack()

# Called to add a new argument preference
def add_preference(A,B, output_box):
    global all_relations_after_preferences, favoured_preferences
    print(all_relations_after_preferences)
    print("trying to add preference")
    print(all_relations)
    found = False
    if A not in all_args:
        msg = "Argument %s not found in framework" % (A)
    elif B not in all_args:
        msg = "Argument %s not found in framework" % (B)
    else:
        if ((A,B)) in all_relations_after_preferences:
            print("found")
            if (B,A) in all_relations_after_preferences:
                found = True
                print("removing old relation")
                print((B,A))
                all_relations_after_preferences.remove((B,A))
                if (A,B) not in favoured_preferences:
                    favoured_preferences.append((A,B))
                print("removed")
                print(all_relations_after_preferences)
                msg = A + " preferred to " + B

        if not found:
            msg = "Invalid/Unnecessary preference"
    output_box.configure(state="normal")
    output_box.insert(END, msg + "\n")
    output_box.configure(state="disabled")
    output_box.see("end")

# Change a button label
def change_btn_text():
    # only change if all_relations different to all_relations_after_preferences
    if all_relations_after_preferences != all_relations:
        add_arg_preferences_btn["text"]= "Reset Argument Preferences?"

# Change the label of the Reset button
def reset_btn_text():
    add_arg_preferences_btn["text"]= "Include Argument Preferences?"

# Called when the Add Argument Preferences button is pressed
def add_argument_preferences():

    global all_relations_after_preferences, favoured_preferences
    favoured_preferences = []
    all_relations_after_preferences = deepcopy(all_relations)
    print(all_relations_after_preferences)

    preferences_window = Toplevel(master)
    center(preferences_window, 400, 300)
    # sets the title of the
    # Toplevel widget
    preferences_window.title("Enter Argument Preferences")
    preferences_window.resizable(False, False)

    preferences_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(preferences_window, add_arg_preferences_btn))

    instruction_frame = Frame(preferences_window)
    usr_entry_frame = Frame(preferences_window)
    done_button_frame = Frame(preferences_window)
    pref_output_frame = Frame(preferences_window)
    instruction_frame.pack()
    usr_entry_frame.pack()
    pref_output_frame.pack()
    done_button_frame.pack()

    preferredTo_label = Label(usr_entry_frame, text=" preferred to ")

    prefA_entry = Entry(usr_entry_frame, width=5, fg="grey")
    prefB_entry = Entry(usr_entry_frame, width=5, fg="grey")

    pref_Output = Text(pref_output_frame, height = 12, width = 37, bg = "light cyan")

    add_preference_btn = Button(usr_entry_frame,
              text="Add Preference", command=lambda:[add_preference(prefA_entry.get(), prefB_entry.get(), pref_Output),clear_box(prefA_entry, prefB_entry), focus_from(prefA_entry)])

    pref_done_btn = Button(done_button_frame,
              text="                             Done                             ", command=lambda:[preferences_window.destroy(), output_msg("Preferences updated"), change_btn_text(), add_arg_preferences_btn.config(state=NORMAL)])


    prefA_entry.pack(side = LEFT)
    preferredTo_label.pack(side = LEFT)
    prefB_entry.pack(side = LEFT)
    add_preference_btn.pack(side = LEFT)
    prefA_entry.insert(0, "arg1")
    prefB_entry.insert(0, "arg2")

    # Handle mouse/keyboard events
    prefA_entry.bind("<FocusIn>", lambda funct: handle_focus_in(prefA_entry, 0))
    prefA_entry.bind("<FocusOut>", lambda funct: handle_focus_out(prefA_entry, 0))
    prefA_entry.bind("<Return>", lambda funct:prefB_entry.focus())
    prefB_entry.bind("<FocusIn>", lambda funct: handle_focus_in(prefB_entry, 1))
    prefB_entry.bind("<FocusOut>", lambda funct: handle_focus_out(prefB_entry, 1))
    prefB_entry.bind("<Return>", lambda funct:[add_preference(prefA_entry.get(), prefB_entry.get(), pref_Output),clear_box(prefA_entry, prefB_entry),focus_from(prefA_entry)])

    pref_Output.pack(pady=4)
    pref_Output.configure(state="disabled")
    pref_done_btn.pack()

# Called after the Help button is pressed
def app_help():
    newWindow = Toplevel(master)
    center(newWindow, 500, 200)
    # sets the title of the
    # Toplevel widget
    newWindow.title("Help")
    newWindow.resizable(False, False)

    newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(newWindow, help_btn))

    # User instructions to enter title
    Label(newWindow,
          text ="Enter the arguments of each attack relation \n of your framework (ie the arguments at each end \n of every edge of your directed graph) into the \n boxes labelled arg1 and arg2. When all relations \n have been entered, click Done. You will then be \n preseneted with further options in order to generate \n the framework labelling of your choosing.").pack()

    okay_btn = Button(newWindow,
            text="Okay",
            command=lambda:[newWindow.destroy(), help_btn.config(state=NORMAL)])
    okay_btn.pack()

# Focus handling - sets where the cursor is automatically placed
def focus_from(entry):
    print("trying to focus")
    entry.focus()
    entry.delete(0, END)
    entry.config(fg="black")

def handle_focus_in(entry, entryType):
    entry.delete(0, END)
    entry.config(fg="black")
    if entryType == 0:
        global arg1_entered
        arg1_entered = True
    else:
        global arg2_entered
        arg2_entered = True

def handle_focus_out(entry, entryType):
    if len(entry.get()) == 0:
        if entryType == 0:
            insertText = "arg1"
            arg1_entered = False
        else:
            insertText = "arg2"
            arg2_entered = False
        entry.delete(0, END)
        entry.config(fg="grey")
        entry.insert(0, insertText)

def handle_return_to(_):
    add_relation()
    clear_box(from_entry, to_entry)
    from_entry.focus()


# Clears the entries within all text boxes
def clear_box(A, B):
    A.delete(0, "end")
    A.config(fg="grey")
    A.insert(0, "arg1")
    B.delete(0, "end")
    B.config(fg="grey")
    B.insert(0, "arg2")



# HERE IS WHERE THE GUI IS SET UP, INCLUDING ALL BUTTONS AND TEXT ENTRY BOXES


master = Tk()
# master.geometry("600x775")
# master.eval("tk::PlaceWindow . center")
center(master, window_width, window_height)
master.title("Argumentation Framework Labelling")
master.resizable(False, False)
util_buttons_frame = Frame(master)
instruction_frame = Frame(master)
usr_entry_frame = Frame(master, highlightbackground="lightgrey", highlightcolor="gainsboro", highlightthickness=1, relief=RIDGE)

button_frame = Frame(master)


# argument_preferences = Frame(master)

labelling_selector_frame = Frame(master)
# grounded_button_frame = Frame(master)
# preferred_button_frame = Frame(master)
output_frame = Frame(master)
graph_label_frame = Frame(master)
graph_frame=Frame(master)
prev_and_nxt_buttons_frame=Frame(master)
reset_button_frame=Frame(master)

# open, save, quit buttons
util_buttons_frame.pack(pady=10)
# Framework Edge Format displayed message
instruction_frame.pack()
# Entry boxes for argument A and B, with Add Edge button
usr_entry_frame.pack(fill=Y, pady=10, ipady=15)

button_frame.pack()

# Light-Blue coloured box, displays output messages
output_frame.pack()
# Displaying Labelling NO of NO message
graph_label_frame.pack()
# Displayed Labelled Framework
graph_frame.pack()
# Previous and Next buttons to cycle through more than one labelling
prev_and_nxt_buttons_frame.pack()
# Reset button - clears all entries and outputs
reset_button_frame.pack()


# instruction_label = Label(instruction_frame, text=u"Framework Edge Format: arg1 \u2192 arg2    ")
instruction_label = Label(instruction_frame, text="Enter each relation of the framework here:")

attacks_label = Label(usr_entry_frame, text=" attacks ")

from_entry = Entry(usr_entry_frame, width=5, fg="grey")
to_entry = Entry(usr_entry_frame, width=5, fg="grey")

Output = Text(output_frame, height = 12, width = 37, bg = "light cyan")

open_btn = Button(util_buttons_frame,
            text="Open",
            command=lambda:[open_btn.config(state=DISABLED), open_fw()])
save_btn = Button(util_buttons_frame,
            text="Save",
            command=lambda:[save_btn.config(state=DISABLED), get_save_name()])
help_btn = Button(util_buttons_frame,
            text="Help",
            command=lambda:[app_help(),
            help_btn.config(state=DISABLED)])
quit_btn = Button(util_buttons_frame,
          text="Quit",
          command=master.quit)

add_relation_btn = Button(usr_entry_frame,
          text="Add Relation", command=lambda:[add_relation(), clear_box(from_entry, to_entry), focus_from(from_entry)])

done_btn = Button(button_frame,
          text="                            Done                            ",
          command=done_btn_pressed)

add_arg_preferences_btn = Button(button_frame,
          command=lambda:[add_argument_preferences(), add_arg_preferences_btn.config(state=DISABLED)])
add_arg_preferences_btn["text"] = "Include Argument Preferences?"

grounded_compute_btn = Button(button_frame,
          text="     Compute Grounded Labelling     ",
          command=lambda: compute_labelling(1))

preferred_compute_btn = Button(button_frame,
          text="   Compute Preferred Labelling(s)   ",
          command=lambda: compute_labelling(2))

previous_btn = Button(prev_and_nxt_buttons_frame, text="Previous", command=show_prev)
next_btn = Button(prev_and_nxt_buttons_frame, text="Next", command=show_next)
reset_btn = Button(reset_button_frame,
          text="Reset", command= lambda: [reset_window(), focus_from(from_entry)])


# LABELS
instruction_label.pack(side = BOTTOM)

# ENTRIES
from_entry.pack(side=LEFT)
attacks_label.pack(side=LEFT)
to_entry.pack(side=LEFT)
add_relation_btn.pack(side=LEFT)
from_entry.insert(0, "arg1")
to_entry.insert(0, "arg2")
# Handle mouse/keyboard events
from_entry.bind("<FocusIn>", lambda funct: handle_focus_in(from_entry, 0))
from_entry.bind("<FocusOut>", lambda funct: handle_focus_out(from_entry, 0))
from_entry.bind("<Return>", lambda funct:to_entry.focus())
to_entry.bind("<FocusIn>", lambda funct: handle_focus_in(to_entry, 1))
to_entry.bind("<FocusOut>", lambda funct: handle_focus_out(to_entry, 1))
to_entry.bind("<Return>", handle_return_to)

# BUTTONS
open_btn.pack(side = LEFT)
save_btn.pack(side = LEFT)
help_btn.pack(side = LEFT)
quit_btn.pack(side = LEFT)
done_btn.pack()

reset_btn.pack()
# OUTPUT
Output.pack(pady=4)
Output.configure(state="disabled")


mainloop()
