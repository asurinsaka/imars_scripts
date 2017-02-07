#!/usr/bin/python
## In order for this program to run you need to install this library
## yum install MySQL-python.x86_64

import sys, getopt
import MySQLdb
import datetime

class QueryDB:
    db_host = ''
    db_user = 'dsm'
    db_pass = 'b28c935'
    db_port = 3306
    conf_file = ''
    pass_id = ''
    spacecraft = ''

    def __init__(self, cf, pi, sp):
        self.conf_file = cf
        self.pass_id = pi
        self.spacecraft = sp
        self.load(conf_file)

    def load(self, filename):
        with open(filename) as fh:
            for line in fh:
                s = line.split()
                if len(s) > 0:
                    parameter = s[0]
                    if parameter == "DSM_DATABASE_HOST":
                        self.db_host = s[len(s) - 1]
                    elif parameter == "DSM_DATABASE_USER":
                        self.db_user = s[len(s) - 1]
                    elif parameter == "DSM_DATABASE_PASSWORD":
                        self.db_pass = s[len(s) - 1]
		    elif parameter == "DSM_DATABASE_PORT":
			self.db_port = int(s[len(s) - 1])


    def get_passes_dates(self):
        db = MySQLdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, port=self.db_port, db="DSM")
        cur = db.cursor()
        dates = []
        cur.execute(
            "select * from Passes where aos < (select aos from Passes where id = " + self.pass_id + ") and aos > (select SUBTIME(aos, '00:30:00') from Passes where id = " + self.pass_id + ") and spacecraft='" + self.spacecraft + "';")
        if cur.rowcount == 0:
            cur.execute(
                "select aos from Passes where aos >= (select aos from Passes where id = " + self.pass_id + ") and aos < (select ADDTIME(aos, '00:30:00') from Passes where id = " + self.pass_id + ") and spacecraft='" + self.spacecraft + "';")
            for index,row in enumerate(cur.fetchall()):
                dates.insert(index, str(row[0]).replace(' ', '_'))
        return dates

if __name__ == "__main__":
    conf_file = ''
    pass_id = ''
    argv = sys.argv[1:]
    spacecraft = "NPP"

    try:
        opts, args = getopt.getopt(argv, "hi:p:s:", ["ifile=", "passid=", "spacecraft="])
    except getopt.GetoptError:
        print('querydb.py -i <conf_file> -p <pass_id>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('querydb.py -i <conf_file> -p <pass_id> -s <spacecraft>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            conf_file = arg
        elif opt in ("-p", "--passid"):
            pass_id = arg
        elif opt in ("-s", "--spacecraft"):
            spacecraft = arg.upper()

    objQuery_DB = QueryDB(conf_file, pass_id, spacecraft)
    dates = objQuery_DB.get_passes_dates()
    if len(dates) > 0:
        print "dates =" + " ".join(dates)
    	# Asurin: those 2 lines are added for true color h2g, asurin 122216
    	print "inputs = input.data " + " ".join(["input.data"+str(idx+1) for idx, value in enumerate(dates) if idx > 0])
        print "geos = geo " + " ".join(["geo"+str(idx+1) for idx, value in enumerate(dates) if idx > 0])
        # Asurin 020717: The following lines are to check whether the pass is old pass so that we can skip mercators
        today = datetime.datetime.today().date()
        pass_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d_%H:%M:%S").date()
        if today - pass_date <= datetime.timedelta(days=2):
            print "new = true"


