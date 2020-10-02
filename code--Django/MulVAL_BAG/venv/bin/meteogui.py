#!/Users/hongxing/PycharmProjects/MulVAL_BAG/venv/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:48:01 2013

@author: kshmirko
"""

from Tkinter import *
from tkFileDialog import asksaveasfilename
import ttk
from datetime import datetime, timedelta
import subprocess

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.title('Meteo_Downloader')
    #root.geometry('305x180+300+177')
    set_Tk_var()
    root.configure(relief="flat")
    root.grid()
    w = Meteo_Downloader (root)
    init()
    root.mainloop()

def set_Tk_var():
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global txtFName
    txtFName = StringVar()

    global txtStart
    txtStart = StringVar()
    txtStart.set(datetime.now().strftime('%Y-%m'))
    
    global txtStop
    txtStop = StringVar()
    txtStop.set('all')
    
    global txtStID
    txtStID = StringVar()
    txtStID.set('31977')


def init():
    pass


format = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&'
formaturl = 'YEAR=%04d&MONTH=%02d&FROM=all&TO=1312&STNM=%s'

class Meteo_Downloader:
    def __init__(self, master=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        TkFixedFont = "-family {DejaVu Sans Mono} -size -12 -weight normal -slant roman -underline 0 -overstrike 0"
        

        self.lblStID = Label(master)
        self.lblStID.grid(row=0, column=0, padx=3, pady=3, sticky='E')
        self.lblStID.configure(text='''WMID:''')
        
        self.entStID = Entry(master)
        self.entStID.grid(row=0, column=1, padx=3, pady=3, sticky='WE')
        self.entStID.configure(background="white")
        self.entStID.configure(font=TkFixedFont)
        self.entStID.configure(textvariable=txtStID)
        self.entStID.configure(width=25)

        self.lblStart = Label (master)
        self.lblStart.grid(row=1, column=0, padx=3, pady=3, sticky='E')
        self.lblStart.configure(text='''Start (yyyy-mm):''')

        self.entStart = Entry (master)
        self.entStart.grid(row=1, column=1,padx=3, pady=3, sticky='WE')
        self.entStart.configure(background="white")
        self.entStart.configure(font=TkFixedFont)
        self.entStart.configure(textvariable=txtStart)
        self.entStart.configure(width=25)

        self.lblStop = Label (master)
        self.lblStop.grid(row=2,column=0, padx=3, pady=3, sticky='E')
        self.lblStop.configure(text='''Stop (yyyy-mm):''')

        self.entStop = Entry (master)
        self.entStop.grid(row=2, column=1, padx=3, pady=3,sticky='WE')
        self.entStop.configure(background="white")
        self.entStop.configure(font=TkFixedFont)
        self.entStop.configure(textvariable=txtStop)
        self.entStop.configure(width=25)

        self.lblOutFName = Label (master)
        self.lblOutFName.grid(row=3, column=0, padx=3, pady=3,sticky='E')
        self.lblOutFName.configure(text='''FName:''')

        self.entFName = Entry (master)
        self.entFName.grid(row=3, column=1, padx=3, pady=3)
        self.entFName.configure(background="white")
        self.entFName.configure(font=TkFixedFont)
        self.entFName.configure(textvariable=txtFName)
        self.entFName.configure(width=25)

        self.btnSelFName = Button (master)
        self.btnSelFName.grid(row=3, column=2, padx=3, pady=3)
        self.btnSelFName.configure(activebackground="#d9d9d9")
        self.btnSelFName.configure(text='''File...''')
        self.btnSelFName.configure(width=5)
        self.btnSelFName.configure(command=self.on_selectfile)

        self.btnDownload = Button (master)
        self.btnDownload.grid(row=4,column=0, padx=3, pady=3, columnspan=2)
        self.btnDownload.configure(activebackground="#d9d9d9")
        self.btnDownload.configure(text='''Download''')
        self.btnDownload['command'] = self.on_download
        
        self.btnExit = Button (master)
        self.btnExit.grid(row=4,column=2, padx=3, pady=3)
        self.btnExit.configure(activebackground="#d9d9d9")
        self.btnExit.configure(text='''Cancel''')
        self.btnExit.configure(command='exit')

        master.grid_columnconfigure(0,weight=1)
        master.resizable(False,False)
        self.root = master
        
    def on_selectfile(self):
        global txtFName
        filetypes = ( ('NetCDF4 files','*.nc4'), )
        self.ncfname = asksaveasfilename(filetypes=filetypes)
        txtFName.set(self.ncfname)
        
    def on_download(self):
        lines = []
        startt = datetime.strptime(txtStart.get(),'%Y-%m')
        if not ('all' in txtStop.get()):
    	    stopt  = datetime.strptime(txtStop.get(),'%Y-%m')
    	
    	    for year in range(startt.year, stopt.year+1):
    		for month in range(1,13):
    		    dt = datetime(year,month,1)
		    if (dt>=startt)&(dt<=stopt):
			url = format+ (formaturl % (dt.year, dt.month, txtStID.get()))
    			print url
    			lines.append('output/%04d-%02d.nc4'%(year,month))
    			lines.append(url)
    			
	else:
	    url = format+ (formaturl % (startt.year, startt.month, txtStID.get()))
	    lines.append(txtFName.get())
	    lines.append(url)
	    
	    
	
    	with open('meteo.ini','wt') as f:
    	    for i in lines:
    		print >> f, i         
	    
        p = subprocess.Popen(['python2', 'download.py'])
        
        


if __name__ == '__main__':
    vp_start_gui()
