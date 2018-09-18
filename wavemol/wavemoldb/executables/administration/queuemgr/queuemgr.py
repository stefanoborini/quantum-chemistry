import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..", "..") ) )
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from application import models
import getopt
import time
import datetime
import subprocess
def showStatus(status):
    if status is None:
        for t in models.QueuedTask.objects.all():
            print t
    else:
        for t in models.QueuedTask.objects.filter(status=status):
            print t

def showMonitor():
    print "Recent tasks "+str(datetime.datetime.now())
    print "-------------"
    for t in models.QueuedTask.objects.filter(modified__gte=datetime.datetime.now()-datetime.timedelta(days=1)):
        print t
    time.sleep(1)
    print chr(27) + "[2J"

opts, args = getopt.getopt(sys.argv[1:], "", [ "list", "status=", "delete-all", "id=", "set-status=", "monitor"])

list_queue = False
delete_all = False
id = None
status=None
set_status = None
monitor = False

for opt in opts:
    if opt[0] == "--list":
        list_queue = True
        
    if opt[0] == "--status":
        status = opt[1]

    if opt[0] == "--delete-all":
        delete_all = True

    if opt[0] == "--id":
        id = opt[1]

    if opt[0] == "--set-status":
        set_status = opt[1]
    if opt[0] == "--monitor":
        monitor = True
if monitor:
    while True:
        try:
            showMonitor()
        except KeyboardInterrupt:
            sys.exit(0)
if set_status and id:
    t = models.QueuedTask.objects.get(id=id)
    if set_status not in ["QUEUED", "RUNNING", "FINISHED"]:
        raise Exception("invalid status")
    t.status = set_status
    t.save()
    
if list_queue:
    showStatus(status)
    sys.exit(0)

if delete_all:
    for t in models.QueuedTask.objects.all():
        t.delete()
       
