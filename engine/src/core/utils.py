import time
from datetime import datetime

def isEmpty(text):
  return text is None or len(text) == 0
  
def isNotEmpty(text):
  return not isEmpty(text)
  
def get_timestamp():
  d = datetime.now()
  return time.mktime(d.timetuple())