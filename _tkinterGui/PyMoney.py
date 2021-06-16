import threading
import time as Time
from tkinter import *
from Class.PyCategory import *
from Class.PyRecord import *

Quit = False
def Update(records):
    global Quit
    while not Quit:
        # delete all
        listBox.delete(0, END)
        # reload from showBox
        for i, data in enumerate(records.showBox):
            # change record into a string
            string = (f'{i+1:>3d} | {data.date:<10s}  {data.category:<10s}{data.description:<10s}{data.amount:>5d}')
            listBox.insert(i, string)
        Wallet.set(f'You have {records.wallet} dollars.')
        Time.sleep(1)

# init datas
categories = Categories()
records = Records()
##### tkinter
# Root, frame
Root = Tk()
Root.title('PyMoney')
frame = Frame(Root, borderwidth=2)
# listBox
listBox_title = Label(frame, text='No.   Date        Category  Item       Amount               ', font=('Consolas', 10))
listBox = Listbox(frame, width= 60, height=20, font=('Consolas', 10))
# wallet info. below listBox
Wallet = StringVar()
WalletText = Label(frame, textvariable=Wallet, font=('Consolas', 10))
# buttons
addStr = StringVar()
addEntry = Entry(frame, textvariable=addStr, font=('Consolas', 12))
addBtn = Button(text='Add', command=lambda:records.Add(addStr.get(), categories))
delStr = StringVar()
delEntry = Entry(frame, textvariable=delStr, font=('Consolas', 12))
delBtn = Button(text='Delete', command=lambda:records.Delete(delStr.get()))
findStr = StringVar()
findEntry = Entry(frame, textvariable=findStr, font=('Consolas', 12))
findBtn = Button(text='Find', command=lambda:records.Find(categories.Subcategories(findStr.get())))
btnReset = Button(frame, text='Reset', command=records.Reset)
btnSave = Button(frame, text='Save', command=records.Save)
###### layout
frame.grid(row=0, column=0)
listBox_title.grid(row=0, column=0)
listBox.grid(row=1, column=0, rowspan=4)
WalletText.grid(row=5, column=0)
addEntry.grid(row=1, column=1)
addBtn.grid(row=1, column=2)
delEntry.grid(row=2, column=1)
delBtn.grid(row=2, column=2)
findEntry.grid(row=3, column=1)
findBtn.grid(row=3, column=2)
btnReset.grid(row=4, column=1)
btnSave.grid(row=4, column=2)

th = threading.Thread(target=lambda:Update(records))
th.start()
mainloop()
Quit = True