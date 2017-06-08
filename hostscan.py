##
##

from fabric import tasks
import fabtask
import catchinfo

def main():
    dbhost = {}

    tasks.execute(fabtask.statistic, catchinfo.stats, dbhost, hosts=['hpchead', 'hpc-master', 'r-ufm189'])
    print json.dumps(dbhost, indent = 2, sort_keys=True)


if __name__ == '__main__':
    main()

