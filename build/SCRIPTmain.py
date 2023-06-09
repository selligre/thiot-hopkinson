import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

"""
BEFORE STARTING THE APPLICATION
1) physical test -> done
2) put censors output in a .txt file -> done
WITH-IN THE APPLICATION
3) select the file -> done
4) put the file content in a data set -> done
5) display data in a graph (to check if there is a visual early error) -> done
6) reduce the data by clicking on the graph -> done
7) create the new data set that contains only newly selected data (incident, reflected, transmitted) -> doing
8) import bar settings (menu with options: import, export, modification, add, suppress)
[traction/compression, size, diameter, volume, mass, density, celerity, Young's Modulus, distance between censor_1 and sample, distance between sample and censor_2]
9) define the 'apparent' Young's Modulus by selecting two spots on the new graph
10) check the Young's Modulus calculated
11) calculate the rest of the data
12) display all graphs
13) export data
"""

# CONSTANTS
FIG_WIDTH = 1280
FIG_HEIGHT = 720

# 3) SELECT FILE DIALOG
root = tk.Tk()
root.withdraw()
FILE_NAME = filedialog.askopenfilename()


def check_file(file):
    if not file:
        exit()


# 4) EXTRACT DATA FROM FILE
def extract_data(file):
    def load_txt(file_path):
        with open(file_path, "r") as f:
            return f.readlines()

    def clean_data(lines):
        # Keep only lines that contain only numbers
        result = []
        for line in lines:
            if ("a" not in line) and ("e" not in line):
                result.append(line)
        result_without_spaces = []
        for line in result:
            if ("\n" in line) and (line != "\n"):
                line = line.replace("\n", "")
            if line != "\n":
                result_without_spaces.append(line)
        return result_without_spaces

    def split_data(tab):
        # Split lines into time, ai1, and ai2 values
        split_time = []
        split_ai1 = []
        split_ai2 = []
        for line in tab:
            if " " in line:
                line = line.replace(" ", ",")
            if "," in line:
                line = line.split(",")
            line = list(filter(lambda x: x != "", line))
            split_time.append(float(line[0]))
            split_ai1.append(float(line[1]))
            split_ai2.append(float(line[2]))
        return [split_time, split_ai1, split_ai2]

    text = load_txt(file)
    numbers = clean_data(text)
    return split_data(numbers)


# Split data into its respective lists
check_file(FILE_NAME)
time, ai1, ai2 = extract_data(FILE_NAME)

# 5) CREATE GRAPH
fig, ax = plt.subplots(figsize=(FIG_WIDTH / 100, FIG_HEIGHT / 100))
ax.plot(time, ai1, label="ai1")
ax.plot(time, ai2, label="ai2")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.legend()

# CREATE CANVAS AND TOOLBAR
# Create window
graph_window = tk.Tk()
graph_window.title("Graph")
# Create graph canvas in window
canvas = FigureCanvasTkAgg(fig, master=graph_window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# Create toolbar
toolbar = NavigationToolbar2Tk(canvas, graph_window)
toolbar.update()
toolbar.pack(side="top", fill="both", expand=1)
# Remove Home, Subplots and Save buttons from toolbar
toolbar._buttons["Home"].pack_forget()
toolbar._buttons["Subplots"].pack_forget()
toolbar._buttons["Save"].pack_forget()


# CLOSE WINDOW BUTTON
def window_close():
    graph_window.destroy()
    graph_window.quit()


close_button = tk.Button(master=graph_window, text="Close", command=window_close)
close_button.pack()

# SELECT POINT BUTTON
left_border_time = None
right_border_time = None
cid = None


def find_closest_index(x):
    # Find the index of the closest point to x
    distances = []
    for line in ax.lines:
        xdata = line.get_xdata()
        distances.append((((xdata - x) ** 2) ** 0.5))
    min_distance = float("inf")
    for j in range(len(distances[0])):
        if min_distance > distances[0][j]:
            min_distance = distances[0][j]
    closest_index = None
    for j in range(len(distances[0])):
        if distances[0][j] == min_distance:
            closest_index = j
    return closest_index


def select_point(event):
    global left_border_time, right_border_time
    if (left_border_time is not None) and (right_border_time is not None):
        print(f"The two borders have already been defined.")
        return
    closest_index = find_closest_index(event.xdata)
    closest_time = time[closest_index]
    if (left_border_time is not None) and (right_border_time is None):
        right_border_time = closest_time
    if (left_border_time is None) and (right_border_time is None):
        left_border_time = closest_time
    ax.axvline(x=closest_time, color="r")
    canvas.draw()
    fig.canvas.mpl_disconnect(cid)


def start_selection():
    global cid
    cid = fig.canvas.mpl_connect("button_press_event", select_point)


select_point_button = tk.Button(
    master=graph_window, text="Select a point", command=start_selection
)
select_point_button.pack()

# MAIN LOOP
tk.mainloop()

# 6) REDUCE THE GRAPH DATA
left_border_index = -1
right_border_index = -1

for index in range(len(time)):
    if time[index] == left_border_time:
        left_border_index = index
    if time[index] == right_border_time:
        right_border_index = index

data_time_cropped = []
data_ai1_cropped = []
data_ai2_cropped = []
for index in range(len(time)):
    if left_border_index <= index <= right_border_index:
        data_time_cropped.append(time[index])
        data_ai1_cropped.append(ai1[index])
        data_ai2_cropped.append(ai2[index])


# get bars parameters
# use bar parameters and signal's length to get incident, reflected and transmitted signals lengths


def extract_parameters(file):
    """
    bar_parameters[material, type, length, diameter, volume, mass, density, celerity, young modulus, j1-sample, sample-j2]
    :param file: txt file containing the bar parameters data
    :return: list containing the parameters' values in order
    """

    def load_txt(file_path):
        with open(file_path, "r") as f:
            return f.readlines()

    def clear_data(lines):
        result = []
        for line in lines:
            line = line.replace("\n", "")
            line = line.split("=")
            result.append(line[1])
        return result

    return clear_data(load_txt(file))


# bar parameters from file
root = tk.Tk()
root.withdraw()
FILE_NAME = filedialog.askopenfilename()
check_file(FILE_NAME)
bar_parameters = extract_parameters(FILE_NAME)
for index in range(len(bar_parameters)):
    if index >= 2:
        bar_parameters[index] = float(bar_parameters[index])

# specimen parameters from file
root = tk.Tk()
root.withdraw()
FILE_NAME = filedialog.askopenfilename()
check_file(FILE_NAME)
specimen_parameters = extract_parameters(FILE_NAME)
for index in range(len(specimen_parameters)):
    specimen_parameters[index] = float(specimen_parameters[index])

bar_material = bar_parameters[0]
if bar_parameters[1] == "compression":
    bar_type = -1
else:
    bar_type = 1
bar_length = bar_parameters[2]
bar_diameter = bar_parameters[3]
bar_volume = bar_parameters[4]
bar_mass = bar_parameters[5]
bar_density = bar_parameters[6]
bar_signal_celerity = bar_parameters[7]
bar_young_modulus = bar_parameters[8]
bar_j1_sample = bar_parameters[9]
bar_j2_sample = bar_parameters[10]

specimen_length = specimen_parameters[0]
specimen_diameter = specimen_parameters[1]

index_step = time[1] - time[0]
transmitted_start_index = left_border_index + (bar_j1_sample + bar_j2_sample) / (
    bar_signal_celerity * 1000 * index_step
)
reflected_start_index = left_border_index + (2 * bar_j1_sample) / (
    bar_signal_celerity * 1000 * index_step
)
incident_start_index = left_border_index
transmitted_end_index = right_border_index
reflected_end_index = right_border_index
incident_end_index = left_border_index + transmitted_end_index - transmitted_start_index

incident_signal = []
reflected_signal = []
transmitted_signal = []
incident_signal_time = []
reflected_signal_time = []
transmitted_signal_time = []
for t in range(len(time)):
    temp_time = time[t]
    for temp_index in range(len(time)):
        if temp_time == time[temp_index]:
            if incident_start_index <= t <= incident_end_index:
                incident_signal.append(bar_type * ai1[temp_index])
                incident_signal_time.append(time[temp_index])
            if reflected_start_index <= t <= reflected_end_index:
                reflected_signal.append(-bar_type * ai1[temp_index])
                reflected_signal_time.append(time[temp_index])
            if transmitted_start_index <= t <= transmitted_end_index:
                transmitted_signal.append(bar_type * ai2[temp_index])
                transmitted_signal_time.append(time[temp_index])

strain_rate = []
for t in range(len(reflected_signal)):
    strain_rate.append(
        ((2 * bar_signal_celerity * 1000) / specimen_length)
        * reflected_signal[t]
        * 0.000001
    )
stress = []
for t in range(len(transmitted_signal)):
    stress.append(
        (
            (bar_young_modulus * (bar_diameter * bar_diameter))
            / (specimen_diameter * specimen_diameter)
        )
        * transmitted_signal[t]
        * 0.000001
    )


def trapezoidal_integration(data):
    integral = 0
    integral_list = []
    for i in range(len(data) - 1):
        integral += (data[i] + data[i + 1]) / 2
        integral_list.append(integral)
    return integral_list


strain = trapezoidal_integration(strain_rate)

if len(strain) > len(stress):
    strain = strain[: len(stress)]
else:
    stress = stress[: len(strain)]

fig2, ax2 = plt.subplots(figsize=(FIG_WIDTH / 100, FIG_HEIGHT / 100))
ax2.plot(strain, stress)
ax2.set_xlabel("Strain")
ax2.set_ylabel("Stress")

graph_window2 = tk.Tk()
graph_window2.title("Graph: Strain / Stress")
# Create graph canvas in window
canvas2 = FigureCanvasTkAgg(fig2, master=graph_window2)
canvas2.draw()
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# Create toolbar
toolbar2 = NavigationToolbar2Tk(canvas2, graph_window2)
toolbar2.update()
toolbar2.pack(side="top", fill="both", expand=1)
# Remove Home, Subplots and Save buttons from toolbar
toolbar2._buttons["Home"].pack_forget()
toolbar2._buttons["Subplots"].pack_forget()
toolbar2._buttons["Save"].pack_forget()


# CLOSE WINDOW BUTTON
def window_close2():
    graph_window2.destroy()
    graph_window2.quit()


close_button2 = tk.Button(master=graph_window2, text="Close", command=window_close2)
close_button2.pack()

# SELECT POINT BUTTON
left_border_index2 = -1
right_border_index2 = -1
left_border_time2 = None
right_border_time2 = None
cid2 = None


def find_closest_index2(x):
    # Find the index of the closest point to x
    distances2 = []
    for line2 in ax2.lines:
        xdata2 = line2.get_xdata()
        distances2.append((((xdata2 - x) ** 2) ** 0.5))
    min_distance2 = float("inf")
    for j in range(len(distances2[0])):
        if min_distance2 > distances2[0][j]:
            min_distance2 = distances2[0][j]
    closest_index2 = None
    for j in range(len(distances2[0])):
        if distances2[0][j] == min_distance2:
            closest_index2 = j
    return closest_index2


def select_point2(event):
    global left_border_time2, right_border_time2
    global left_border_index2, right_border_index2
    if (left_border_time2 is not None) and (right_border_time2 is not None):
        print(f"The two borders have already been defined.")
    closest_index2 = find_closest_index2(event.xdata)
    closest_time2 = time[closest_index2]
    if (left_border_time2 is not None) and (right_border_time2 is None):
        right_border_index2 = closest_index2
        right_border_time2 = closest_time2
    if (left_border_time2 is None) and (right_border_time2 is None):
        left_border_index2 = closest_index2
        left_border_time2 = closest_time2
    ax2.axvline(x=closest_time2, color="r")
    canvas2.draw()
    fig2.canvas.mpl_disconnect(cid2)


def start_selection2():
    global cid2
    cid2 = fig2.canvas.mpl_connect("button_press_event", select_point2)


select_point_button2 = tk.Button(
    master=graph_window2, text="Select a point", command=start_selection2
)
select_point_button2.pack()

# MAIN LOOP
tk.mainloop()

apparent_modulus = (stress[right_border_index2] - stress[left_border_index2]) / (
    strain[right_border_index2] - strain[left_border_index2]
)

# calculer nouveau stress avec le apparent_modulus et afficher dans une nouvelle fenetre avec juste close_button
# passer a l'interface

apparent_stress = []
for t in range(len(transmitted_signal)):
    apparent_stress.append(
        (
            (apparent_modulus * (bar_diameter * bar_diameter))
            / (specimen_diameter * specimen_diameter)
        )
        * transmitted_signal[t]
        * 0.000001
    )

if len(strain) > len(apparent_stress):
    strain = strain[: len(apparent_stress)]
else:
    apparent_stress = apparent_stress[: len(strain)]

fig3, ax3 = plt.subplots(figsize=(FIG_WIDTH / 100, FIG_HEIGHT / 100))
ax3.plot(strain, apparent_stress)
ax3.set_xlabel("Strain")
ax3.set_ylabel("Apparent Stress")

graph_window3 = tk.Tk()
graph_window3.title("Graph: Strain / Apparent Stress")
# Create graph canvas in window
canvas3 = FigureCanvasTkAgg(fig3, master=graph_window3)
canvas3.draw()
canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# Create toolbar
toolbar3 = NavigationToolbar2Tk(canvas3, graph_window3)
toolbar3.update()
toolbar3.pack(side="top", fill="both", expand=1)
# Remove Home, Subplots and Save buttons from toolbar
toolbar3._buttons["Home"].pack_forget()
toolbar3._buttons["Subplots"].pack_forget()
toolbar3._buttons["Save"].pack_forget()


# CLOSE WINDOW BUTTON
def window_close3():
    graph_window3.destroy()
    graph_window3.quit()


close_button3 = tk.Button(master=graph_window3, text="Close", command=window_close3)
close_button3.pack()

# MAIN LOOP
tk.mainloop()


"""
hopkinson's project progress meeting on wednesdays at 4pm
switch graph display to Figure() -> integrated zooming, probably possible to hide only some buttons, maybe easier to get cursor coords -> done
priority is to end the calculus part asap -> doing
do the ModelViewController separation at the end
do the interface dev at the end
do the bar parameter settings at the end
do the errors try catch at the end
"""
