# mm_stdinDB_logger
logging from stdin into a database table

## Purpose
This is a tiny programm which allows to write log information into a sqlite database table which will be received from standard-in.
An initial idea for usage is to pipe log information produced by the rsync command into this programm which will write the log records into a database table.

The log line record format for the loging will currently contain 4 different fields separated by a space character:

```
1) Date           log entry date.  
2) Time           log entry time.
3) Process ID     log entry created by a process having this process-id.
4) Text           log text - the information of the log entry.

example:
2018/05/30 09:26:40 [33325] cd+++++++++ gro_test/t/
2018/05/30 09:26:40 [33325] >f+++++++++ gro_test/t/__init__.pyc
2018/05/30 09:26:40 [33325] sent 5,546,228,814 bytes  received 95,501 bytes  51,118,196.45 bytes/sec
2018/05/30 09:26:40 [33325] total size is 5,544,530,207  speedup is 1.00
```

the result in the sqlite database will look like in the picture below:

![alt text](https://github.com/marcel-gross/mm_stdinDB_logger/blob/master/sreenshot_mm_stdinDBlogger_2018-05-31_142819.png)

The sqlite database file name and table name can be given using the parameters -d and -t at program start. For detailed description see below. Within the table, there are again 4 fields but they do differ slightly from the above log line format:

```
1)  LOG_id          INTERGER        Primary Key which will be automatically be assigned by database
2)  LOG_TimeStamp   DATETIME        Date + Time in format YYYY-MM-DD HH:MM:SS
3)  LOG_Process     VARCHAR(50)     Process Information (in our case the process id)
4)  LOG_Text        VARCHAR(5000)   Text field 
````
while you can influence the DB-file and table name, the table structure and its column names are given.
If a given DB-file and/or table is not existing, it will be created at runtime, otherwise the log-entries will just be added to the table. There are no delete, update or reoganisation functions in place at this point in time.

## Usage

Most likely you could make use of this programm in many different ways, here we just show you an example.

The regular program call with its possible parameters are as follows:

```
stdinDB_logger_v01.py -d <output_DB_file> -t <table_name>

```

And here an example in conjunction with the rsync command:

```
rsync -avrq --log-file=/dev/stdout /home/gro/shares/VM_Share_nbch0052_001/ /home/gro/Documents/backup_20180530/ |./stdinDB_logger_v01.py -d lalalog -t log_t2_20180531
```

The rsync command will create an archive from a directory into a backup directory and creates a log-file to /dev/stdout which is piped to the stdinDB_logger_v01.py program. The given parameters are -d lalalog which will be the SQLite Database file located in the directory were the program is called. The -t parameter set to log_t2_20180531 will tell the program to log the information into a table with the given name.

























