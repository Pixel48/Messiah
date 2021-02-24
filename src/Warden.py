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
logging.basicConfig(level = logging.DEBUG, format=LOG_FORMAT)
# disable logging
# logging.disable(logging.CRITICAL)

versionTag = '0.1.0'

INITPATH = str(Path.home() / 'Downloads')

# main
def main():
  root = Tk()
  # root.geometry('200x125') # main widow size
  style = ttk.Style(root)
  style.theme_use('clam')
  # root.iconbitmap(r'') # main window icon path
  root.title("Warden")
  MainWindow(root)
  root.mainloop()

# window building
presenceTolDef = 3
lateTolDef = 10
validateToleranceMaxDef = 1 + 30
_padx = 5
_pady = 5
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
    self.frame.grid()
  def build(self, frame):
    self.footerFont = font.Font(size = 7)
    # main #
    # main / date #
    # main / date / label #
    newCol()
    self.dateLabel = Label(frame)
    self.dateLabel['text'] = "Lesson date:"
    self.dateLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / date / datepick #
    nextCol()
    self.datePick = CustomDateEntry(frame, width = 12, background = 'darkblue', foreground = 'white', borderwidth = 2)
    self.datePick._set_text(self.datePick._date.strftime('%d-%m-%Y'))
    self.datePick['justify'] = 'center'
    self.datePick.grid(row = R, column = C, sticky = 'W', padx = _padx, pady = _pady)
    # main / time #
    # main / time / label #
    nextRow()
    self.timeLabel = Label(frame)
    self.timeLabel['text'] = "Lesson beginning:"
    self.timeLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / time / time #
    nextCol()
    self.timePick = Entry(frame)
    # self.timePick['text'] = self.getTimeStr() # DEBUG in future
    # self.setTimeStr(self.timePick)
    self.timePick.insert(0, self.getTimeStr())
    self.timePick['width'] = 5
    self.timePick['justify'] = 'center'
    self.timePick['validate'] = 'key'
    validateTimePick = (self.master.register(self.timeValidate), '%i', '%P')
    self.timePick['validatecommand'] = validateTimePick
    self.timePick.grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
    # main / presence tolerance #
    # main / presence tolerance / label #
    nextRow()
    self.presenceTolLabel = Label(frame)
    self.presenceTolLabel['text'] = 'Presence tolerance [min]:'
    self.presenceTolLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / presence tolerance / box #
    nextCol()
    self.presenceTolBox = Entry(frame)
    self.presenceTolBox['width'] = 6
    self.presenceTolBox['justify'] = 'center'
    self.presenceTolBox.insert(0, str(presenceTolDef))
    self.presenceTolBox['validate'] = 'key'
    validatePresenceTolBox = (self.master.register(self.validateTolerance), '%i', '%P')
    self.presenceTolBox['validatecommand'] = validatePresenceTolBox
    self.presenceTolBox.grid(row = R, column = C, sticky = 'W', padx = _padx, pady = _pady)
    # main / late tolerance
    # main / late tolerance / label #
    nextRow()
    self.lateTolLabel = Label(frame)
    self.lateTolLabel['text'] = 'Late tolerance [min]:'
    self.lateTolLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / late tolerance / slider #
    nextCol()
    self.lateTolBox = Entry(frame)
    self.lateTolBox['width'] = 6
    self.lateTolBox['justify'] = 'center'
    self.lateTolBox.insert(0, str(lateTolDef))
    self.lateTolBox['validate'] = 'key'
    validateLateTolBox = (self.master.register(self.validateTolerance), '%i', '%P', int(self.presenceTolBox.get()))
    self.lateTolBox['validatecommand'] = validateLateTolBox
    self.lateTolBox.grid(row = R, column = C, sticky = 'W', padx = _padx, pady = _pady)
    # main / Import CSV #
    # main / Import CSV / button #
    nextRow()
    self.csvBtn = Button(frame)
    self.csvBtn['text'] = 'Import CSV'
    self.csvBtn['width'] = 20
    self.csvBtn['command'] = self.importCsv
    self.csvBtn.grid(row = R, column = C, columnspan = 2, sticky = '', padx = _padx, pady = _pady)
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
  def importCsv(self):
    """Imports CSV file and opens result window"""
    logging.debug("datePick makes " + str(self.datePick.get()))
    logging.debug("timePick makes " + str(self.timePick.get()))
    logging.debug("Tolerance: " + self.presenceTolBox.get() + " / " + self.lateTolBox.get())
  def timeValidate(self, index, arg):
    logging.debug("timeValidate(): index '" + index + "', arg '" + arg + "'")
    self.timePattern = re.compile(r'^((([0-2]{0,1})|([0-2]\d{0,1})|([0-2]\d:)|([0-2]\d:\d)|([0-2]\d:[0-5]\d))|((\d{0,1})|(\d:)|(\d:\d)|(\d:[0-5]\d)))$')
    if index == 1 and arg[-1].isdigit(): self.fixTime(self.timePick)
    return True if self.timePattern.match(arg) else False
  def makeHour(self, s):
    """Automaticly adds ':' after hours"""
    pass # TODO: make me
  def fixTime(self, timeWidget, first = 2):
    """Fixes time format in time widget"""
    logging.debug("fixTime()")
    s = str(timeWidget.get())[:first]
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
    logging.info("Start time: " + hour + ':' + minute)
    return hour + ':' + minute
  def validateTolerance(self, index, arg, limit = 0, top = validateToleranceMaxDef):
    """Validates tolerances"""
    logging.debug('validateTolerance(): ' + str(index) + ', ' + str(arg) + ' (' + str(limit) + ', ' + str(top) + ')')
    # limit = int(limit)
    regex = re.compile(r'')
    return regex.match(arg)
    # if not arg: return True
    # if arg.isdigit():
    #   arg = int(arg)
    #   return 
    # return False

class CustomDateEntry(DateEntry):
  def _select(self, event=None):
    date = self._calendar.selection_get()
    if date is not None:
      self._set_text(date.strftime('%d-%m-%Y'))
      self.event_generate('<<DateEntrySelected>>')
    self._top_cal.withdraw()
    if 'readonly' not in self.state():
      self.focus_set()

if __name__ == '__main__':
  main()
