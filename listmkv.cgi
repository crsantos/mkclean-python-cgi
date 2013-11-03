#!/usr/bin/env python
# Lists MKV on the DIR
 
import itertools as it, glob, os, datetime, fnmatch

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from Cheetah.Template import Template

NUMBER_OF_DAYS = 60
PATH_TO_SCAN = '/downloads' #/downloads
HOSTNAME = "http://localhost"

# Humanize byte size figures
# https://gist.github.com/moird/3684595
def humanize_bytes(bytesize, precision=0):
  abbrevs = (
      (1<<50, 'PB'),
      (1<<40, 'TB'),
      (1<<30, 'GB'),
      (1<<20, 'MB'),
      (1<<10, 'kB'),
      (1, 'bytes')
  )
  if bytesize == 1:
    return '1 byte'
  for factor, suffix in abbrevs:
    if bytesize >= factor:
        break
  return '%.*f %s' % (precision, bytesize / factor, suffix)


def multiple_file_types(*patterns):
  return it.chain.from_iterable(glob.glob(pattern) for pattern in patterns)

def check_for_old_files_and_notify_based_on_date( today = datetime.datetime.today() ):
  last_month = today - datetime.timedelta(days=NUMBER_OF_DAYS)

  matches = []  
  total_size = 0
  try:
    for root, dirnames, filenames in os.walk(PATH_TO_SCAN, followlinks=False):
      if root == PATH_TO_SCAN+"/autoseed": # avoid autoseed dir - TODO - optimize
        continue
      for filename in fnmatch.filter(filenames, '*.mkv'):
        afile = os.path.join(root, filename)
        
        modified =  datetime.datetime.fromtimestamp(os.path.getmtime(afile))
        created =   datetime.datetime.fromtimestamp(os.path.getctime(afile))
        accessed =  datetime.datetime.fromtimestamp(os.path.getatime(afile))
        size_bytes = os.path.getsize(afile)
        total_size += size_bytes
        human_size = humanize_bytes(size_bytes)

        matches.append({
          "filename"  : afile,
          "accessed"  : accessed,
          "created"   : created,
          "modified"  : modified,
          "size"      : human_size
        })

    t = Template(file="dir.tmpl", searchList={"matches":matches, "today":today, "last_month":last_month, "hostname":HOSTNAME, "total_size":humanize_bytes(total_size)})

    print "Content-type: text/html"
    print str(t)

  except Exception, e:
    print "<error>Failed: %s</error>" % e

def main():
  check_for_old_files_and_notify_based_on_date()

if __name__ == '__main__':
  main()