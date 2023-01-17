import tkinter as tk
import os
import json
from randTimetable import randTimetable
from optimize import Optimize
from vehicle import Vehicle
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


root = tk.Tk()
root.title('App')
root.geometry("1300x300")

txt = ""

startPointVar=tk.StringVar(value="0")
endPointVar=tk.StringVar()
startTimeVar=tk.StringVar()
maxCostVar=tk.StringVar()
maxTabooLenVar=tk.StringVar()
aspirationVar=tk.StringVar(value="0")
nmaxVar=tk.StringVar()
busVVar=tk.StringVar(value="100")
busCostVar=tk.StringVar(value="1")
trainVVar=tk.StringVar(value="160")
trainCostVar=tk.StringVar(value="1.2")
planeVVar=tk.StringVar(value="800")
planeCostVar=tk.StringVar(value="5")

startPointlabel = tk.Label(root, text = 'Start point', font=('calibre',10, 'bold'))
startPointEntry = tk.Entry(root, textvariable = startPointVar, font=('calibre',10,'normal'))

endPointlabel = tk.Label(root, text = 'End point', font=('calibre',10, 'bold'))
endPointEntry = tk.Entry(root, textvariable = endPointVar, font=('calibre',10,'normal'))

startTimelabel = tk.Label(root, text = 'Start time', font=('calibre',10, 'bold'))
startTimeEntry = tk.Entry(root, textvariable = startTimeVar, font=('calibre',10,'normal'))

maxCostlabel = tk.Label(root, text = 'Max cost', font=('calibre',10, 'bold'))
maxCostEntry = tk.Entry(root, textvariable = maxCostVar, font=('calibre',10,'normal'))

maxTabooLenlabel = tk.Label(root, text = 'Max taboo len', font=('calibre',10, 'bold'))
maxTabooLenEntry = tk.Entry(root, textvariable = maxTabooLenVar, font=('calibre',10,'normal'))

aspirationlabel = tk.Label(root, text = 'Aspiration', font=('calibre',10, 'bold'))
aspirationEntry = tk.Entry(root, textvariable = aspirationVar, font=('calibre',10,'normal'))

nmaxlabel = tk.Label(root, text = 'Max iter', font=('calibre',10, 'bold'))
nmaxEntry = tk.Entry(root, textvariable = nmaxVar, font=('calibre',10,'normal'))

busVlabel = tk.Label(root, text = 'Bus vel', font=('calibre',10, 'bold'))
busVEntry = tk.Entry(root, textvariable = busVVar, font=('calibre',10,'normal'))

busCostlabel = tk.Label(root, text = 'Bus cost', font=('calibre',10, 'bold'))
busCostEntry = tk.Entry(root, textvariable = busCostVar, font=('calibre',10,'normal'))

trainVlabel = tk.Label(root, text = 'Train vel', font=('calibre',10, 'bold'))
trainVEntry = tk.Entry(root, textvariable = trainVVar, font=('calibre',10,'normal'))

trainCostlabel = tk.Label(root, text = 'Train cost', font=('calibre',10, 'bold'))
trainCostEntry = tk.Entry(root, textvariable = trainCostVar, font=('calibre',10,'normal'))

planeVlabel = tk.Label(root, text = 'Plane vel', font=('calibre',10, 'bold'))
planeVEntry = tk.Entry(root, textvariable = planeVVar, font=('calibre',10,'normal'))

planeCostlabel = tk.Label(root, text = 'Plane cost', font=('calibre',10, 'bold'))
planeCostEntry = tk.Entry(root, textvariable = planeCostVar, font=('calibre',10,'normal'))


def editSave():
    out = {
        "start": startPointEntry.get(),
        "end": endPointEntry.get(),
        "time": startTimeEntry.get(),
        "maxCost": maxCostEntry.get(),
        "maxTabooLen": maxTabooLenEntry.get(),
        "aspiration": aspirationEntry.get(),
        "nmax": nmaxEntry.get()
    }
    print(out)
    outJSON = json.dumps(out, sort_keys=True, indent=4)
    with open(f'{os.getcwd()}/src/data/save.json', 'w') as f:
        f.write(outJSON)


def useSave():
    with open(f'{os.getcwd()}/src/data/save.json', 'r') as f:
        data = json.load(f)
    print(data)

    startPointEntry.delete(0, 'end')
    startPointEntry.insert(0, data['start'])

    endPointEntry.delete(0, 'end')
    endPointEntry.insert(0, data['end'])

    startTimeEntry.delete(0, 'end')
    startTimeEntry.insert(0, data['time'])

    maxCostEntry.delete(0, 'end')
    maxCostEntry.insert(0, data['maxCost'])

    maxTabooLenEntry.delete(0, 'end')
    maxTabooLenEntry.insert(0, data['maxTabooLen'])

    aspirationEntry.delete(0, 'end')
    aspirationEntry.insert(0, data['aspiration'])

    nmaxEntry.delete(0, 'end')
    nmaxEntry.insert(0, data['nmax'])


editSaveBtn=tk.Button(root,text = 'Edit saved', command = lambda:editSave())
useSaveBtn=tk.Button(root,text = 'Use saved', command = lambda:useSave())
generateBtn=tk.Button(root,text = 'New timetable', command = lambda:randTimetable())


def optimize():
    if isinstance(int(startPointEntry.get()), int) and isinstance(int(endPointEntry.get()), int) and isinstance(int(startTimeEntry.get()), int) and isinstance(float(maxCostEntry.get()), float) and isinstance(int(maxTabooLenEntry.get()), int) and isinstance(int(aspirationEntry.get()), int) and isinstance(int(nmaxEntry.get()), int) and isinstance(float(busVEntry.get()), float) and isinstance(float(busCostEntry.get()), float) and isinstance(float(trainVEntry.get()), float) and isinstance(float(trainCostEntry.get()), float) and isinstance(float(planeVEntry.get()), float) and isinstance(float(planeCostEntry.get()), float):

        opt = Optimize()
        opt.addVehicle(Vehicle('bus', float(busVEntry.get()), float(busCostEntry.get())))
        opt.addVehicle(Vehicle('train', float(trainVEntry.get()), float(trainCostEntry.get())))
        opt.addVehicle(Vehicle('plane', float(planeVEntry.get()), float(planeCostEntry.get())))

        with open(f'{os.getcwd()}/src/data/cities.json', 'r') as f:
            data = json.load(f)

        for i in data:
            opt.addCity(i)

        with open(f'{os.getcwd()}/src/data/timetable.json', 'r') as f:
            data = json.load(f)

        for i in range(len(data)):
            opt.cities[i].addTimetable(data[i]["timetable"])

        opt.calculateDist()

        opt.loadTimetable()

        o = opt.opt(int(startPointEntry.get()), int(endPointEntry.get()), int(startTimeEntry.get()), float(maxCostEntry.get()), int(maxTabooLenEntry.get()), int(aspirationEntry.get()), int(nmaxEntry.get()))

        print(o[:-1])
        print(o[3:])

        fig = Figure(figsize = (12, 6), dpi = 100)
        plot1 = fig.add_subplot(211)
        plot2 = fig.add_subplot(212)
        plot1.grid()
        plot2.grid()
        plot2.plot(o[6], label='Cost of all solutions')
        plot2.scatter(o[7], o[3], c='orange', label='Cost of best solutions')
        o[7].append(len(o[6]))
        o[3].append(o[3][-1])
        plot1.plot(o[7], o[3], label='Cost of best solutions')
        plot1.set_title('Best solutions')
        plot2.set_title('All solutions')
        plot1.legend()
        plot2.legend()

        graph = tk.Tk()
        graph.title('Graph')

        canvas = FigureCanvasTkAgg(fig, master = graph)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,graph)
        toolbar.update()
        canvas.get_tk_widget().pack()
        label1.config(text = o[0])
        label2.config(text = '[type of transport, city id, time spent in city]')
        label3.config(text = o[2])


optimizeBtn=tk.Button(root,text = 'Optimize', command = lambda:optimize())


startPointlabel.grid(row=0,column=0)
startPointEntry.grid(row=0,column=1)
endPointlabel.grid(row=1,column=0)
endPointEntry.grid(row=1,column=1)
startTimelabel.grid(row=2, column=0)
startTimeEntry.grid(row=2, column=1)
maxCostlabel.grid(row=3, column=0)
maxCostEntry.grid(row=3, column=1)
maxTabooLenlabel.grid(row=4, column=0)
maxTabooLenEntry.grid(row=4, column=1)
aspirationlabel.grid(row=5, column=0)
aspirationEntry.grid(row=5, column=1)
nmaxlabel.grid(row=6, column=0)
nmaxEntry.grid(row=6, column=1)

editSaveBtn.grid(row=7,column=0)
useSaveBtn.grid(row=7,column=1)


busVlabel.grid(row=0,column=4)
busVEntry.grid(row=0,column=5)
busCostlabel.grid(row=1, column=4)
busCostEntry.grid(row=1, column=5)
trainVlabel.grid(row=2, column=4)
trainVEntry.grid(row=2, column=5)
trainCostlabel.grid(row=3,column=4)
trainCostEntry.grid(row=3,column=5)
planeVlabel.grid(row=4, column=4)
planeVEntry.grid(row=4, column=5)
planeCostlabel.grid(row=5, column=4)
planeCostEntry.grid(row=5, column=5)

generateBtn.grid(row=6,column=5)

optimizeBtn.grid(row=7,column=3)

label1 = tk.Label(text='')
label2 = tk.Label(text='')
label3 = tk.Label(text='')
label1.grid(row=8,column=3)
label2.grid(row=9,column=3)
label3.grid(row=10,column=3)

root.mainloop()

# TODO
# vehicles with def value
# btn to generate rand timetable
# max cost
# max taboo len
# aspiration
# nmax
# start time
# optimize()
# graphs
# add cities?
