#!/usr/bin/python
#
###############################################################################
#
# stdinDB_logger_v01.py : standard-in DB logger
# ---------------------------------------------
#
# system .............: linux
# directory ..........: 
# program ............: stdinDB_logger_v01.py
# version / release ..: 0.1
# date ...............: 2018.05.30 mg version 0.1
#
# programmer .........: Marcel Gross
# department .........: IT
#
# application group...: 
# application ........: 
#
# usage ..............: stdinDB_logger_v01.py -d <output_DB_file> -t <table_name> 
#
#
#                       rsync -avrq --log-file=/dev/stdout /home/gro/shares/VM_Share_nbch0052_001/ /home/gro/Documents/backup_20180530/ |./stdinDB_logger_v01.py -d lalalog.db -t log_table_20180531
#
#
# special ............: 
#                       rsync -avrq --log-file=/dev/stdout /home/gro/shares/VM_Share_nbch0052_001/ /home/gro/Documents/backup_20180530/
#
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/objects/fc/
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/sql-database-python-manage/.git/objects/fc/b3ea48648ce089aea164a7fc96f58651b746f3
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/objects/fe/
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/sql-database-python-manage/.git/objects/fe/04ae152d78d3a823034f761ac14a9bd59612ee
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/objects/info/
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/objects/pack/
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/refs/
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/refs/heads/
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/sql-database-python-manage/.git/refs/heads/master
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/refs/remotes/
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/refs/remotes/origin/
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/sql-database-python-manage/.git/refs/remotes/origin/HEAD
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/sql-database-python-manage/.git/refs/tags/
#                       2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/t/
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/t/__init__.py
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/t/__init__.pyc
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/t/test_2ndcall_par.py
#                       2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/t/test_2ndcall_par.pyc
#                       2018/05/30 09:26:40 [33325] sent 5,546,228,814 bytes  received 95,501 bytes  51,118,196.45 bytes/sec
#                       2018/05/30 09:26:40 [33325] total size is 5,544,530,207  speedup is 1.00
#                       
#
#
# history ............: 2018.05.30 14:26 mg
#                       base version
#
### Libraries #################################################################
#
import sys
import getopt
import io
import socket
import sqlite3
#import hashlib
#import base64
#import uuid
import os
import re
#
from datetime  import datetime
from time      import sleep
#
### Functions #################################################################
#------------------------------------------------------------------------------ 
#
# MAIN sub : DMS_upload_doc : Document uploading Subroutine
#
def DMS_upload_doc(parameters):
#   
    PROC_id = os.getpid()
    HOST_id = socket.getfqdn()
#
# check : parameters
#
    FILENAME, TABLENAME = get_parameters(parameters)
#
# connect : to configured Database
#
    global db									# define variable db      for global usage
    global cursor 								# define variable cursor  for global usage
#
    try: 
        SQLite_database = FILENAME
        db = sqlite3.connect(SQLite_database)
#        db.isolation_level = None
        cursor = db.cursor()
        #print ('sqlite connection established')
    except:
        print ('sqlite connection failed')
        sys.exit(2)
#
# create : tables if not yet existing in the DB
#
#  db.isolation_level = None
    cursor = db.cursor()
    try:
        create_tables(TABLENAME)
        db.commit()								# Commit the change
    except Exception as e:							# DB Error handling
        # Roll back any change if something goes wrong
        db.rollback()
        db.close()
        raise e
#
# read : stdin line by line and split a line into 4 Fields subsequently write the record into the table of the DB-File
#    
    try: 
        for line in iter(sys.stdin.readline, b''):				# read stdin line by line
            #print str.split(' ', 1 )
            #print (line)
            fields = line.split( )						# split the line into fields using space as separator
            numfields = len(fields)						# evaluate the resulting number of fields in this line
            #print ("fields: " + str(numfields) + " " + str(fields))
            if numfields > 3:							# we need at least 4 fields for a log-record
#
               logdate = str(fields[0])						# Field 1 -> Date  (usualy comming in format 2018/05/27)
               logtime = str(fields[1])						# Field 2 -> Tiime (usualy comming in format 12:27:02)
               logproc = str(fields[2])						# Field 3 -> Process ID (usualy comming in format [31258]
               logtext = ' '.join(map(str, fields[3:]))				# Field 4-bis should all be merged and end up in the LOG_Text
#
               logdate = re.sub('[/._]','-', logdate)           		# replace / and . by - string
               logproc = re.sub('[\[\]]'   ,'', logproc)			# replace [ and ] by empty string (remove [ and ] from the string)
#
               LOG_TimeStamp = str(logdate + " " + logtime)
               LOG_Process   = str(logproc)
               LOG_Text      = str(logtext)
#
               #print ("date: " + str(logdate) + " time: " + str(logtime) + " process: "+ str(logproc) + " text: "+ str(logtext) + ".")
               write_data_into_table(TABLENAME, LOG_TimeStamp, LOG_Process, LOG_Text)
    except KeyboardInterrupt:
        sys.stout.flush()
        pass
        return
#
# close : DB Connection
#
    
    #sleep(DELAY)
    db.close()
    return
#
#------------------------------------------------------------------------------ 
#
# sub : get parameters
#
def get_parameters(argv):
    FILENAME = ""
    TABLENAME = ""
    #print (argv)
    try:
       opts, args = getopt.getopt(argv,"hd:t:",["DBfile=","table="])
    except getopt.GetoptError:
       print 'stdinDB_logger_v01.py -d <DBfile> -t <table>'
       sys.exit(2)
    #print (opts)
    for opt, arg in opts:
       if opt == '-h':
          print 'stdinDB_logger_v01.py -d <DBfile> -t <table>'
          sys.exit()
       elif opt in ("-d", "--DBfile"):
          FILENAME = arg
       elif opt in ("-t", "--table"):
          TABLENAME = arg
    #print 'DBfile is ', FILENAME
    #print 'Table  is ', TABLENAME
    if FILENAME == '':
       print 'parameter -d <DBfile> is missing'
       sys.exit(2)
    if TABLENAME == '':
       TABLENAME = "log_data"
    if "-" in TABLENAME: 
       print 'parameter -t <table> contains nonvalid characters. (- not allowed)'
       sys.exit(2)    
       
    return (FILENAME, TABLENAME)
#
#------------------------------------------------------------------------------ 
#
# sub : write_data_into_table 
# 
def write_data_into_table(TABLENAME, LOG_TimeStamp, LOG_Process, LOG_Text):
#
#  
#
    sql_command = """INSERT INTO """ + TABLENAME + \
                  """   (LOG_TimeStamp, LOG_Process, LOG_Text) 
                         values (?, ?, ?)"""
#
    #print (sql_command)
#
    try:
        cursor.execute(sql_command, [LOG_TimeStamp, LOG_Process, LOG_Text])
        db.commit()
    except Exception as e:
        print ("error 205")
        # Roll back any change if something goes wrong
        db.rollback()
        db.close()
        raise e
        sys.exit(2)
#
    return
#
#------------------------------------------------------------------------------ 
#
# sub : create_tables
# 
def create_tables(TABLENAME):
#
#      cursor.execute('''DROP TABLE IF EXISTS tablename''')
#
# 
    #print (TABLENAME)
#
# prepair : sql statement
#
    sql_command = """ CREATE TABLE IF NOT EXISTS """ + TABLENAME + \
		  """      (
		          LOG_id       		INTEGER PRIMARY KEY AUTOINCREMENT,
			  LOG_TimeStamp		DATETIME,
			  LOG_Process		VARCHAR(50),
			  LOG_Text		VARCHAR(5000)
			);
		  """
#
    #print (sql_command)
#
# execute : sql statement
#
    cursor.execute(sql_command)
#    
    return
#
### Main Program ##############################################################
#
if __name__ == '__main__':
#
    parameters  = sys.argv[1:]
    #print "sys.argv : " + str(sys.argv[1:]) + "\n"
    #print "parameter: " + str(parameters) + "\n"
    DMS_upload_doc(parameters)
#
### END #######################################################################
