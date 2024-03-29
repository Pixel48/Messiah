import logging
LOG_FORMAT = '[%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.disable(logging.INFO)
logging.debug("Imported Logging")

from tkinter import *;                logging.debug("Imported tkinter.*")
import tkinter.font as font;          logging.debug("Imported tk.font")
from tkinter import ttk;              logging.debug("Imported ttk")
from tkinter import filedialog as fd; logging.debug("Imported tk.Filedialog")
from tkcalendar import DateEntry;     logging.debug("Imported tkcDateEntry")
import threading;                     logging.debug("Imported threading")
from pathlib import Path;             logging.debug("Imported Path")
import sys;                           logging.debug("Imported sys")
import re;                            logging.debug("Imported Re")
import datetime as dt;                logging.debug("Imported DateTime")
import os;                            logging.debug("Imported os")
import csv, codecs;                   logging.debug("Imported csv & codecs")
logging.debug("Importing done!")

versionTag = '0.3.2'
ICONPATH = 'icons/ico.ico' if '.exe' not in sys.argv[0] else 'Messiah.exe'

DOWNPATH = str(Path.home() / 'Downloads')
DOCSPATH = str(Path.home() / 'Documents')

timePattern = re.compile(r'''
  ^(
    (\d?)|            # H
    (                 # HH
      ([0-1]\d?)|
      (2[0-3]?)
    )|
    (\d{1,2}:\d?)|     # H(H): / H(H):M
    (\d{1,2}:[0-5]\d) # H(H):M(M)
  )$
  ''', re.VERBOSE)

# main
def main():
  root = Tk()
  style = ttk.Style(root)
  style.theme_use('clam')
  root.iconbitmap(ICONPATH) # main window icon path
  root.title("Messiah")
  MainWindow(root)
  root.mainloop()

# CSV lang
ENTER = 'Dołączył'
EXIT = 'Opuścił(a)'

# window building
presenceTolDef = 3
lateTolDef = 10
validateToleranceMaxDef = 1 + 30
_padx = 5
_pady = 5
def plane(a):
  out = a**(1/2)*2+1
  return out if a > out else a//2+1

class MainWindow(object):
  """Main window class"""
  def __init__(self, master):
    self.master = master
    self.master.resizable(width=False, height=False) # lock window resize
    self.master.iconbitmap(ICONPATH) # icon
    self.frame = Frame(self.master)
    self.build(self.frame)
    self.frame.grid()
    self.log = {}
    self.list = []
    logging.info("Start time: " + self.getTimeStr())
  def build(self, frame):
    C, R = 0, 0
    self.footerFont = font.Font(size=7)
    # main #
    # main / date #
    # main / date / label #
    self.dateLabel = Label(frame)
    self.dateLabel['text'] = "Lesson date:"
    self.dateLabel.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # main / date / datepick #
    C += 1
    self.datePick = CustomDateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    self.datePick._set_text(self.datePick._date.strftime('%d.%m.%Y'))
    self.datePick['justify'] = CENTER
    self.datePick.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / time start #
    # main / time start / label #
    C = 0
    R += 1
    self.timeLabelStart = Label(frame)
    self.timeLabelStart['text'] = "Lesson start:"
    self.timeLabelStart.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # main / time start / time #
    C += 1
    self.timePickStart = Entry(frame)
    # self.timePickStart['text'] = self.getTimeStr() # DEBUG in future
    # self.setTimeStr(self.timePickStart)
    self.timePickStart.insert(0, self.getTimeStr())
    self.timePickStart['width'] = 5
    self.timePickStart['justify'] = CENTER
    self.timePickStart['validate'] = 'key'
    validateTimePickStart = (self.master.register(self.timeValidate), '%i', '%P')
    self.timePickStart['validatecommand'] = validateTimePickStart
    self.timePickStart.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / event duration #
    # main / event duration / label #
    C = 0
    R += 1
    self.eventDurationLabel = Label(frame)
    self.eventDurationLabel['text'] = "Lesson duration [min]:"
    self.eventDurationLabel.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # # main / event duration / time #
    C += 1
    self.eventDurationScale = Scale(frame)
    self.eventDurationScale['from_'] = 30
    self.eventDurationScale['to_'] = 90
    self.eventDurationScale.set(45)
    self.eventDurationScale['orient'] = HORIZONTAL
    self.eventDurationScale['width'] = 6
    self.eventDurationScale.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / presence tolerance #
    # main / presence tolerance / label #
    C = 0
    R += 1
    self.presenceTolLabel = Label(frame)
    self.presenceTolLabel['text'] = "Presence tolerance [min]:"
    self.presenceTolLabel.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # main / presence tolerance / scale #
    C += 1
    self.presenceTolScale = Scale(frame)
    self.presenceTolScale['from_'] = 1
    self.presenceTolScale['to_'] = 10
    self.presenceTolScale.set(5)
    self.presenceTolScale['orient'] = HORIZONTAL
    self.presenceTolScale['width'] = 6
    self.presenceTolScale.bind('<ButtonRelease>', self.lateLimit)
    self.presenceTolScale.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / late tolerance #
    # main / late tolerance / label #
    C = 0
    R += 1
    self.lateTolLabel = Label(frame)
    self.lateTolLabel['text'] = "Late tolerance [min]:"
    self.lateTolLabel.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # main / late tolerance / scale #
    C += 1
    self.lateTolScale = Scale(frame)
    self.lateTolScale['from_'] = 6
    self.lateTolScale['to_'] = 15
    self.lateTolScale.set(15)
    self.lateTolScale['orient'] = HORIZONTAL
    self.lateTolScale['width'] = 6
    self.lateTolScale.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / escape tolerance #
    # main / escape tolerance / label#
    C = 0
    R += 1
    self.escTolLabel = Label(frame)
    self.escTolLabel['text'] = 'Escape tolerance [min]:'
    self.escTolLabel.grid(row=R, column=C, sticky='E', padx=_padx, pady=_pady)
    # main / escape tolerance / scale #
    C += 1
    self.ecsTolScale = Scale(frame)
    self.ecsTolScale['from_'] = 15
    self.ecsTolScale['to_'] = 0
    self.ecsTolScale.set(3)
    self.ecsTolScale['orient'] = HORIZONTAL
    self.ecsTolScale['width'] = 6
    self.ecsTolScale.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / buttons #
    # main / buttons / list #
    C = 0
    R += 1
    self.listBtn = Button(frame)
    self.listBtn['text'] = "Attenders list"
    self.listBtn['command'] = self.importAttenders
    self.listBtn['width'] = 20
    self.listBtn.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # main / buttons / Import CSV #
    C += 1
    self.csvBtn = Button(frame)
    self.csvBtn['text'] = "Import CSV"
    self.csvBtn['command'] = self.importCSV
    self.csvBtn['width'] = 20
    self.csvBtn.grid(row=R, column=C, sticky='WE', padx=_padx, pady=_pady)
    # footer
    # footer / version
    self.version = Label(frame, font=self.footerFont)
    self.version['text'] = versionTag
    self.version.grid(row=99, column=0,  sticky='W')
    # footer / signature
    self.github = Label(frame, font=self.footerFont)
    self.github['text'] = "GitHub.com/Pixel48/Messiah"
    self.github['fg'] = 'grey'
    self.github.grid(row=99, column=0, columnspan=3, sticky='E')
  def importAttenders(self):
    """Import full list of attenders"""
    logging.info("=== import attenders ===")
    filename = fd.askopenfilename(
      title="Select full attenders list file",
      initialdir=DOCSPATH,
      filetypes=(
        ('Text file', '*.txt'),
        ('Perfect CSV', '*.csv'),
      )
    )
    logging.debug("filename attenders = " + str(filename))
    self.list = []
    if filename:
      if '.txt' in filename:
        with codecs.open(filename, 'r',  'utf-8') as attList:
          for line in attList.readlines():
            line = line.strip()
            if line != '': self.list.append(line)
      elif '.csv' in filename:
        with codecs.open(filename, 'r', 'utf-16') as attList:
          attList.readline()
          for line in attList.readlines():
            line = line.strip()
            line = line.split('\t')[0]
            if line != '': self.list.append(line)
      self.listBtn['text'] = os.path.basename(filename).split('.')[0]
    else:
      self.listBtn['text'] = "Attenders list"
  def importCSV(self):
    """Imports CSV file and opens result window"""
    logging.info("=== import CSV button data ===")
    filename = fd.askopenfilename(
      title="Select Teams-genereted attendance file",
      initialdir=DOWNPATH,
      filetypes=(('CSV file', '*.csv'),)
    )
    logging.info("filename CSV = " + str(filename))
    timeStamp = (self.datePick.get().split('.'), self.timePickStart.get().split(':'))
    logging.debug(timeStamp[0][0] + ' ' + timeStamp[0][1] + ' ' + timeStamp[0][2] + ' ' + timeStamp[1][0] + ' ' + timeStamp[1][1])
    self.eventStart = dt.datetime(int(timeStamp[0][2]), int(timeStamp[0][1]), int(timeStamp[0][0]), int(timeStamp[1][0]), int(timeStamp[1][1]))
    logging.info("datePick = " + str(self.datePick.get()))
    logging.info("timePickStart = " + str(self.timePickStart.get()))
    self.eventDuration = dt.timedelta(0, self.eventDurationScale.get() * 60)
    self.eventEnd = self.eventStart + self.eventDuration
    logging.info("eventDurationScale = " + str(self.eventDurationScale.get()))
    logging.info("eventEnd = " + str(self.eventEnd))
    self.presenceTolerance = self.presenceTolScale.get()
    self.lateTolerance = self.lateTolScale.get()
    logging.info("Tolerance = " + str(self.presenceTolScale.get()) + " / " + str(self.lateTolScale.get()))
    logging.debug("=== import CSV ===")
    if filename:
      self.log = {}
      if self.list:
        for attender in self.list:
          if attender: self.log.update({' '.join(x.capitalize() for x in attender.split()): (None, None)})
      with codecs.open(filename, 'r', 'utf-16') as inputFile:
        inputFile.readline() # remove header
        currStudent = ''
        studentEnter = None
        studentExit = None
        for row in csv.reader(inputFile, delimiter='\t'):
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
    self.masterWindowResults=Toplevel(self.master)
    self.masterWindowResults.title(self.datePick.get() + ' // ' + self.timePickStart.get())
    self.appWindowResults = ResultWindow(self.masterWindowResults, self)
  def lateLimit(self, arg):
    """Limits LateTolScale start range"""
    logging.debug("lateLimit(): presenceTolScale = " + str(self.presenceTolScale.get()))
    self.lateTolScale['from_'] = self.presenceTolScale.get() + 1
  def timeValidate(self, index, arg):
    logging.debug("timeValidate(): index '" + index + "', arg '" + arg + "'")
    return True if timePattern.match(arg) else False
  def makeHour(self, s):
    """Automaticlly adds ':' after hours""" # broken
    pass # TODO: make me
  def fixTime(self, timeWidget, first=2):
    """Fixes time format in time widget"""
    logging.debug("fixTime()")
    s = str(timeWidget.get())[:first]
    s += ':'
    timeWidget.delete(0, END)
    timeWidget.insert(0, s)
  def getTimeStr(self, timestamp=dt.datetime.now(), addMinutes=0):
    """Returns time string in 'HH:MM' format"""
    now = timestamp + dt.timedelta(minutes=addMinutes)
    hour = now.hour
    minute = now.minute
    hour = '0' + str(hour) if hour < 10 else str(hour)
    minute = '0' + str(minute) if minute < 10 else str(minute)
    return str(hour) + ':' + str(minute)

class ResultWindow(object):
  """Popup window with results"""
  def __init__(self, master, above):
    self.master = master
    self.master.resizable(width=False, height=False) # lock window resize
    self.master.iconbitmap(ICONPATH) # icon
    self.above = above
    self.frame = Frame(self.master)
    self.log = self.above.log
    self.build(self.frame)
    self.frame.grid()
  def build(self, frame):
    """Create Result window (scrollable in future)"""
    C, R = 0, 0
    row = plane(len(self.log))
    legalPresence = dt.timedelta(0, 60 * self.above.presenceTolScale.get())
    legalLate = dt.timedelta(0, 60 * self.above.lateTolScale.get())
    longDelta = dt.timedelta(0, -60 * 25)
    maxLen = 0
    for key in self.log.keys():
      if len(key) > maxLen: maxLen = len(key)
    for key in sorted(self.log.keys()):
      if R >= row:
        R = 0
        C += 2
      if self.log[key][0]: entryDelta = self.log[key][0] - self.above.eventStart
      escTol = self.above.ecsTolScale.get() * 60
      if self.log[key][1]:
        escapeDelta = self.above.eventEnd - self.log[key][1]
      else:
        escapeDelta = dt.timedelta()
      statusID = {
        0: 'On time',
        1: 'Absent',
        2: 'Late',
        3: 'Too late'
      }
      statusBG = {
        0: '#0d0',
        1: '#d00',
        2: '#fd0',
        3: '#ea0'
      }
      status = None
      haveEscaped = False
      # checkout logs
      if not self.log[key][0]: status = 1
      else:
        if longDelta < entryDelta < legalPresence: status = 0
        elif legalPresence < entryDelta < legalLate: status = 2
        else: status = 3
      if self.log[key][1] and self.log[key][1] < self.above.eventEnd and escapeDelta.seconds > escTol: haveEscaped = True
      # setup logs
      C += 1
      Label(frame, text=statusID.get(status), bg=statusBG.get(status)).grid(row=R, column=C, sticky='WE')
      C += 1
      if haveEscaped:
        Label(frame, text=key, width=maxLen, anchor='w', fg='#fff', bg='#000').grid(row=R, column=C, padx=_padx, pady=_pady)
      else:
        Label(frame, text=key, width=maxLen, anchor='w').grid(row=R, column=C, padx=_padx, pady=_pady)
      C -= 2
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
