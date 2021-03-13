import logging
LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.DEBUG, format=LOG_FORMAT)
logging.disable(logging.NOTSET)

logging.debug("Imported Logging")
from tkinter import *
logging.debug("Imported tkinter *")
from tkinter import ttk
logging.debug("Imported ttk")
from tkinter import filedialog as fd
logging.debug("Imported Filedialog")
from tkcalendar import DateEntry
logging.debug("Imported DateEntry")
from pathlib import Path
logging.debug("Imported Path")
import tkinter.font as font
logging.debug("Imported tk.font")
import csv, codecs
logging.debug("Imported csv & codecs")
import datetime as dt
logging.debug("Imported DateTime")
import re
logging.debug("Imported Re")
logging.debug("Importing done!")

versionTag = 'demo'

INITPATH = str(Path.home() / 'Downloads')

# main
def main():
  root = Tk()
  # root.geometry('200x125') # main widow size
  style = ttk.Style(root)
  style.theme_use('clam')
  # root.iconbitmap(r'') # main window icon path
  root.title("Messiah")
  MainWindow(root)
  root.mainloop()

# CSV lang
ENTER = 'Dołączył'
EXIT = 'Opuścił(a)'

# window building
maxRows = 50
presenceTolDef = 3
lateTolDef = 10
validateToleranceMaxDef = 1 + 30
_padx = 5
_pady = 5
global C
global R
R = 0
C = 0
def nextRow(row = 1, column = 0):
  global R, C
  R += row
  C = column
def nextCol(column = 1):
  global C
  C += column
def newCol(column = 0):
  global C, R
  R = 0
  C = column

class MainWindow(object):
  """Main window class"""
  def __init__(self, master):
    self.master = master
    self.master.resizable(width = False, height = False) # lock window resize
    # self.master.iconbitmap(r'./ico.ico') # icon
    self.frame = Frame(self.master)
    self.build(self.frame)
    self.frame.grid()
    logging.info("Start time: " + self.getTimeStr())
  def build(self, frame):
    global C, R
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
    self.datePick._set_text(self.datePick._date.strftime('%d.%m.%Y'))
    self.datePick['justify'] = CENTER
    self.datePick.grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
    # main / time start #
    # main / time start / label #
    nextRow()
    self.timeLabelStart = Label(frame)
    self.timeLabelStart['text'] = "Lesson start:"
    self.timeLabelStart.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / time start / time #
    nextCol()
    self.timePickStart = Entry(frame)
    # self.timePickStart['text'] = self.getTimeStr() # DEBUG in future
    # self.setTimeStr(self.timePickStart)
    self.timePickStart.insert(0, self.getTimeStr())
    self.timePickStart['width'] = 5
    self.timePickStart['justify'] = CENTER
    self.timePickStart['validate'] = 'key'
    validateTimePickStart = (self.master.register(self.timeValidate), '%i', '%P')
    self.timePickStart['validatecommand'] = validateTimePickStart
    self.timePickStart.grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
    # main / event duration #
    # main / event duration / label #
    nextRow()
    self.eventDurationLabel = Label(frame)
    self.eventDurationLabel['text'] = "Lesson duration [min]:"
    self.eventDurationLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # # main / event duration / time #
    nextCol()
    self.eventDurationScale = Scale(frame)
    self.eventDurationScale['from_'] = 30
    self.eventDurationScale['to_'] = 90
    self.eventDurationScale.set(45)
    self.eventDurationScale['orient'] = HORIZONTAL
    self.eventDurationScale['width'] = 6
    self.eventDurationScale.grid(row = R, column = C, sticky = 'W', padx = _padx, pady = _pady)
    # main / presence tolerance #
    # main / presence tolerance / label #
    nextRow()
    self.presenceTolLabel = Label(frame)
    self.presenceTolLabel['text'] = 'Presence tolerance [min]:'
    self.presenceTolLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / presence tolerance / scale #
    nextCol()
    self.presenceTolScale = Scale(frame)
    self.presenceTolScale['from_'] = 1
    self.presenceTolScale['to_'] = 9
    self.presenceTolScale.set(5)
    self.presenceTolScale['orient'] = HORIZONTAL
    self.presenceTolScale['width'] = 6
    self.presenceTolScale.bind('<ButtonRelease>', self.lateLimit)
    self.presenceTolScale.grid(row = R, column = C, sticky = 'W', padx = _padx, pady = _pady)
    # main / late tolerance #
    # main / late tolerance / label #
    nextRow()
    self.lateTolLabel = Label(frame)
    self.lateTolLabel['text'] = 'Late tolerance [min]:'
    self.lateTolLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / late tolerance / scale #
    nextCol()
    self.lateTolScale = Scale(frame)
    self.lateTolScale['from_'] = 6
    self.lateTolScale['to_'] = 30
    self.lateTolScale.set(15)
    self.lateTolScale['orient'] = HORIZONTAL
    self.lateTolScale['width'] = 6
    self.lateTolScale.grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
    # main / escape tolerance #
    # main / escape tolerance / label#
    nextRow()
    self.escTolLabel = Label(frame)
    self.escTolLabel['text'] = 'Escape tolerance [min]:'
    self.escTolLabel.grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
    # main / escape tolerance / scale #
    nextCol()
    self.ecsTolScale = Scale(frame)
    self.ecsTolScale['from_'] = 15
    self.ecsTolScale['to_'] = 0
    self.ecsTolScale.set(3)
    self.ecsTolScale['orient'] = HORIZONTAL
    self.ecsTolScale['width'] = 6
    self.ecsTolScale.grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
    # main / Import CSV #
    # main / Import CSV / button #
    nextRow()
    self.csvBtn = Button(frame)
    self.csvBtn['text'] = 'Import CSV'
    self.csvBtn['width'] = 20
    self.csvBtn['command'] = self.importCSV
    self.csvBtn.grid(row = R, column = C, columnspan = 2, sticky = '', padx = _padx, pady = _pady)
    # footer
    # footer / version
    self.version = Label(frame, font = self.footerFont)
    self.version['text'] = versionTag
    self.version.grid(row = 99, column = 0,  sticky = 'W')
    # footer / signature
    self.github = Label(frame, font = self.footerFont)
    self.github['text'] = "GitHub.com/Pixel48/Messiah"
    self.github['fg'] = 'grey'
    self.github.grid(row = 99, column = 0, columnspan = 3, sticky = 'E')
  def importCSV(self):
    """Imports CSV file and opens result window"""
    logging.info("=== import CSV button data ===")
    filename = fd.askopenfilename(
      title = "Select Teams-genereted CSV file",
      initialdir = INITPATH,
      filetypes = (('CSV file', '*.csv'),)
    )
    logging.info("filename = " + str(filename))
    timeStamp = (self.datePick.get().split('.'), self.timePickStart.get().split(':'))
    logging.debug(timeStamp[0][0] + ' ' + timeStamp[0][1] + ' ' + timeStamp[0][2] + ' ' + timeStamp[1][0] + ' ' + timeStamp[1][1])
    self.eventStart = dt.datetime(int(timeStamp[0][2]), int(timeStamp[0][1]), int(timeStamp[0][0]), int(timeStamp[1][0]), int(timeStamp[1][1]))
    logging.info("datePick = " + str(self.datePick.get()))
    logging.info("timePickStart = " + str(self.timePickStart.get()))
    self.eventDuration = dt.timedelta(0, self.timePickEnd.get() * 60)
    logging.info("timePickEnd = " + str(self.timePickEnd.get()))
    self.presenceTolerance = self.presenceTolBox.get()
    self.lateTolerance = self.lateTolBox.get()
    logging.info("Tolerance = " + str(self.presenceTolBox.get()) + " / " + str(self.lateTolBox.get()))
    logging.debug("=== import CSV ===")
    if filename:
      self.log = {}
      with codecs.open(filename, 'r', 'utf-16') as inputFile:
        inputFile.readline() # remove header
        currStudent = ''
        studentEnter = None
        studentExit = None
        for row in csv.reader(inputFile, delimiter = '\t'):
          if currStudent != ' '.join(row[0].split()[::-1]):
            if currStudent != '':
              self.log.update({currStudent: (studentEnter, studentExit)})
              logging.info("New student: " + currStudent + " form " + str(studentEnter) + " to " + str(studentExit))
            studentExit = None
            currStudent = ' '.join(row[0].split()[::-1])
            logging.debug("Importing student " + currStudent)
            timeStamp = row[-1].split(', ')
            enterDay = timeStamp[0].split('.')
            enterTime = timeStamp[1].split(':')
            del timeStamp
            studentEnter = dt.datetime(
              # date
              int(enterDay[2]),
              int(enterDay[1]),
              int(enterDay[0]),
              # time
              int(enterTime[0]),
              int(enterTime[1]),
              int(enterTime[2])
            )
            logging.debug("Enter at " + str(studentEnter))
            del enterDay, enterTime
          else:
            if row[1] == EXIT: # update studentExit datetime
              timeStamp = row[-1].split(', ')
              exitDay = timeStamp[0].split('.')
              exitTime = timeStamp[1].split(':')
              del timeStamp
              studentExit = dt.datetime(
                # date
                int(exitDay[2]),
                int(exitDay[1]),
                int(exitDay[0]),
                # time
                int(exitTime[0]),
                int(exitTime[1]),
                int(exitTime[2])
              )
              logging.debug("Exit at " + str(studentExit))
              del exitDay, exitTime
            else: continue
        self.log.update({currStudent: (studentEnter, studentExit)})
        logging.info("New student: " + currStudent + " form " + str(studentEnter) + " to " + str(studentExit))
      del currStudent, studentEnter, studentExit
      self.showResults()
  def showResults(self):
    """Open result window"""
    logging.debug("Opening Result window...")
    self.masterWindowResults = Toplevel(self.master)
    self.appWindowResults = ResultWindow(self.masterWindowResults, self)
  def lateLimit(self, arg):
    """Limits LateTolBox start range"""
    logging.debug("lateLimit(): presenceTolBox = " + str(self.presenceTolBox.get()))
    self.lateTolBox['from_'] = self.presenceTolBox.get() + 1
  def timeValidate(self, index, arg):
    logging.debug("timeValidate(): index '" + index + "', arg '" + arg + "'")
    self.timePattern = re.compile(r'^((([0-2]{0,1})|([0-2]\d{0,1})|([0-2]\d:)|([0-2]\d:\d)|([0-2]\d:[0-5]\d))|((\d{0,1})|(\d:)|(\d:\d)|(\d:[0-5]\d)))$')
    if index == 1 and arg[-1].isdigit(): self.fixTime(self.timePickStart)
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
  def getTimeStr(self, addMinutes = 0):
    """Returns time string in 'HH:MM' format"""
    now = dt.datetime.now() + dt.timedelta(minutes = addMinutes)
    hour = now.hour
    minute = now.minute
    hour = '0' + str(hour) if hour < 10 else str(hour)
    minute = '0' + str(minute) if minute < 10 else str(minute)
    return str(hour) + ':' + str(minute)
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

class ResultWindow(object):
  """Popup window with results"""
  def __init__(self, master, above):
    self.master = master
    self.master.resizable(width = False, height = False) # lock window resize
    # self.master.iconbitmap(r'./ico.ico') # icon
    self.above = above
    self.frame = Frame(self.master)
    self.log = self.above.log
    self.build(self.frame)
    self.frame.grid()
  def build(self, frame):
    """Create Result window (scrollable in future)"""
    R, C = 0, 0
    row = 15
    legalPresence = dt.timedelta(0, 60 * self.above.presenceTolBox.get())
    legalLate = dt.timedelta(0, 60 * self.above.lateTolBox.get())
    longDelta = dt.timedelta(0, -60 * 25)
    for key in sorted(self.log.keys()):
      if R >= row:
        R = 0
        C += 2
      Label(frame, text = key).grid(row = R, column = C, sticky = 'E', padx = _padx, pady = _pady)
      newCol()
      C += 1
      entryDelta = self.log[key][0] - self.above.eventStart
      if self.log[key][1]: exitDelta = self.log[key][1] - self.log[key][0]
      else: exitDelta = None
      if entryDelta < legalLate: # before start / late / ok
        if entryDelta < longDelta: # before 25' -> absent
          Label(frame, text = 'Absent', bg = '#d00').grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
        elif longDelta < entryDelta < legalPresence: # before <25' & before legalPresence -> present
          Label(frame, text = 'Present', bg = '#0d0').grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
        elif legalPresence < entryDelta < legalLate: # after legalPresence & before legalLate -> late
          Label(frame, text = 'Late', bg = '#fd0').grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
      else:
        Label(frame, text = 'Absent', bg = '#d00').grid(row = R, column = C, sticky = 'WE', padx = _padx, pady = _pady)
      C -= 1
      R += 1

class CustomDateEntry(DateEntry):
  def _select(self, event=None):
    date = self._calendar.selection_get()
    if date is not None:
      self._set_text(date.strftime('%d.%m.%Y'))
      self.event_generate('<<DateEntrySelected>>')
    self._top_cal.withdraw()
    if 'readonly' not in self.state():
      self.focus_set()

if __name__ == '__main__':
  main()
