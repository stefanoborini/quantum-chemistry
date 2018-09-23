#!/usr/bin/env python
# This script is run by cron. It checks the queue for existing jobs and performs
# the various required tasks for importing the associated submission

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..","..") ) )
import uuid

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from application import models
import subprocess
import logging
import settings

#logging.basicConfig(filename=os.path.join(settings.LOGDIR, "importer","importer.log"), level=logging.INFO)
logging.basicConfig(level=logging.INFO)
EXECUTABLE_BASE_DIR = os.path.realpath(os.path.join( os.path.realpath(os.path.dirname(__file__)), ".." ))

_GLOBAL_dry_run = False

def call(args):
    global _GLOBAL_dry_run
    if _GLOBAL_dry_run:
        logging.info( "Dry Run : "+str(args) )
        ret_status = 0
    else:
        logging.info( "Run : "+str(args) )
        ret_status = subprocess.call( args )
    return ret_status

def commit_to_rdfdb(identifier):
    logging.info("START : commit_to_rdfdb : "+str(identifier))
    ret_status = call( [ 
                       "python", 
                       os.path.join( EXECUTABLE_BASE_DIR, "commit_to_rdfdb", "commit_to_rdfdb.py"), 
                       "--id=%s" % str(identifier)
                     ] )
    logging.info("END : commit_to_rdfdb : "+str(identifier))
    if ret_status != 0:
        raise Exception("commit_to_rdfdb failed. ret_status = %d" % ret_status)

def generate_molecule_xyz(identifier):
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_molecule_xyz", "generate_molecule_xyz.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_molecule_xyz failed. ret_status = %d" % ret_status)
 
def generate_system_identifier(identifier):
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_system_identifier", "generate_system_identifier.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_system_identifier failed. ret_status = %d" % ret_status)

def generate_molecule_basicinfo(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_molecule_basicinfo", "generate_molecule_basicinfo.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_molecule_basicinfo failed. ret_status = %d" % ret_status)

def generate_molecule_icons(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_molecule_icons", "generate_molecule_icons.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_molecule_icons failed. ret_status = %d" % ret_status)

def generate_interconversion_icons(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_interconversion_icons", "generate_interconversion_icons.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_interconversion_icons failed. ret_status = %d" % ret_status)

def generate_interconversion_files(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_interconversion_files", "generate_interconversion_files.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_interconversion_files failed. ret_status = %d" % ret_status)

def generate_interconversion_xyz(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "generate_interconversion_xyz", "generate_interconversion_xyz.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("generate_interconversion_xyz failed. ret_status = %d" % ret_status)

def add_to_index(identifier): 
    ret_status = call( [ 
                        "python", 
                        os.path.join( EXECUTABLE_BASE_DIR, "add_to_index", "add_to_index.py"), 
                        "--id=%s" % str(identifier)
                      ] )
    if ret_status != 0:
        raise Exception("add_to_index failed. ret_status = %d" % ret_status)

def start_Xvfb(): 
    ret_status = call( [ 
                        "sh", 
                        os.path.join( EXECUTABLE_BASE_DIR, "start_Xvfb", "start_Xvfb.sh"), 
                      ] )
    if ret_status != 0:
        raise Exception("start_Xvfb failed. ret_status = %d" % ret_status)

def main():
    global _GLOBAL_dry_run
    logging.info("START")
    for t in models.QueuedTask.objects.filter(type="import", status="QUEUED"):
        logging.info("RUNNING : queue entry "+str(t.id))
        try:
            if not _GLOBAL_dry_run:
                t.status="RUNNING"
                t.save()
            identifier = str(uuid.UUID(t.parameters))

            commit_to_rdfdb(identifier)
            generate_system_identifier(identifier)
            generate_molecule_xyz(identifier)
            generate_molecule_basicinfo(identifier)
            start_Xvfb()
            generate_molecule_icons(identifier)
            generate_interconversion_icons(identifier)
            generate_interconversion_files(identifier)
            generate_interconversion_xyz(identifier)
            add_to_index(identifier)           
        except Exception, e:
            if not _GLOBAL_dry_run:
                t.status="FAILED"
                t.save()
            logging.info("FAILED : queue entry "+str(t.id)+" : exception = "+str(e))

        if not _GLOBAL_dry_run:
            t.status="SUCCESS"
            t.save()
        logging.info("SUCCESS : queue entry "+str(t.id))
    logging.info("COMPLETED")

if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
    _GLOBAL_dry_run = True
    print "Running dry"
    logging.info("Running dry")

main()
