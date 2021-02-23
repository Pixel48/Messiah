from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkcalendar import DateEntry
from pathlib import Path
import tkinter.font as font
import csv, codecs
import datetime as dt
import re
import logging

LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.DEBUG)

versionTag = '0.1.0'

INITPATH = str(Path.home() / 'Downloads')

# main
def main():
  root = Tk()
  # root.geometry('200x125') # main widow size
  style = ttk.Style(root)
  style.theme_use('clam')
  root.title("Warden")
  MainWindow(root)
  root.mainloop()

# window building
R = 0
C = 0
def nextRow(column = 0, row = 1):
  global C, R
  R += row
  C = 0
  C += column
def nextCol(column = 1):
  global C
  C += column
def newCol(column = 0):
  global C, R
  R = 0
  C = column

# CSV converting
def fixNull(file):
  """Fixes broken csv flie"""
  for line in file: yield line.replace('\0', ' ')

class MainWindow(object):
  """Main window class"""
  def __init__(self, master):
    self.master = master
    self.master.resizable(width=False, height=False) # lock window resize
    # self.master.iconbitmap(r'./ico.ico') # icon
    self.frame = Frame(self.master)
    self.build(self.frame)
    # self.timePattern = re.compile(r'^\d{1,2}([ |:]\d{0,2})?$')
    # self.timePattern = re.compile(r'')
    self.frame.grid()
  def build(self, frame):
    self.footerFont = font.Font(size = 7)
    # main
    # main / date
    # main / date / label
    newCol()
    self.dateLabel = Label(frame)
    self.dateLabel['text'] = "Lesson date:"
    self.dateLabel.grid(row = R, column = C, sticky = 'E', padx = 10, pady = 5)
    # main / date / datepick
    nextCol()
    self.datePick = DateEntry(frame, width = 12, background = 'darkblue', foreground = 'white', borderwidth = 2)
    self.datePick.grid(row = R, column = C, sticky = 'W', padx = 10, pady = 5)
    # main / time
    # main / time / label
    nextRow()
    self.timeLabel = Label(frame)
    self.timeLabel['text'] = "Time:"
    self.timeLabel.grid(row = R, column = C, sticky = 'E', padx = 10, pady = 5)
    # main / time / time
    nextCol()
    self.entryTime = Entry(frame)
    self.entryTime['text'] = self.getTimeStr()
    self.entryTime['justify'] = 'center'
    self.entryTime['width'] = 5
    self.entryTime['validate'] = 'key'
    vcmd = (self.master.register(self.timeValidate), '%i', '%P')
    self.entryTime['validatecommand'] = vcmd
    self.entryTime.grid(row = R, column = C, sticky = 'WE', padx = 10, pady = 5)
    # main / CSV button
    nextRow()
    self.csvBtn = Button(frame)
    self.csvBtn['text'] = 'Import CSV'
    self.csvBtn.grid(row = R, column = C, columnspan = 2, sticky = 'WE', padx = 10, pady = 5)
    # footer
    # footer / version
    self.version = Label(frame, font = self.footerFont)
    self.version['text'] = versionTag
    self.version.grid(row = 99, column = 0,  sticky = 'W')
    # footer / signature
    self.github = Label(frame, font = self.footerFont)
    self.github['text'] = "GitHub.com/Pixel48/Warden"
    self.github['fg'] = 'grey'
    self.github.grid(row = 99, column = 0, columnspan = 3, sticky = 'E')
  def timeValidate(self, index, arg):
    logging.debug("timeValidate(): " + index + ' --- ' + arg)
    if index == 0: return re.compile(r'\d').match(arg)
    if index == 1:
      if arg.isdigit(): self.fixTime(self.entryTime); return re.compile(r'[0-2]\d').match(arg)
      else: self.fixTime(self.entryTime, 1); return re.compile(r'\d[\s|:|;|,|.]').match(arg)
    # if index == 2: return re.compile(r'\d\d( :;)').match(arg); self.fixTime()
    if index == 3: return re.compile(r'\d').match(arg)
    if index == 4: return re.compile(r'\d').match(arg)
    # return True if self.timePattern.match(arg) else False
  def fixTime(self, timeWidget, first = 2):
    """Fixes time format in time widget"""
    s = timeWidget.get()[:first]
    s += ':'
    timeWidget.delete(0, END)
    timeWidget.insert(0, s)
  def getTimeStr(self):
    """Returns time string in 'HH:MM' format"""
    now = dt.datetime.now()
    hour = str(now.hour)
    minute = str(now.minute)
    if int(hour) < 10: hour = '0' + hour
    if int(minute) < 10: hour = '0' + minute
    return hour + ':' + minute

if __name__ == '__main__':
  main()
