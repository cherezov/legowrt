#!/usr/bin/python3.4
import sys
import time
from daemon import Daemon
from importlib import reload

import ev3server

if __name__ == "__main__":
   class Ev3ServerDaemon(Daemon):
      def run(self):
         ev3server.run()

      def status(self):
         try:
            with open(self.pidfile,'r') as pf:
               pid = int(pf.read().strip())
         except IOError:
            pid = None

         print('State:\t', 'Running' if pid is not None else 'Stopped')
         if pid is not None:
            print('PID file:\t', self.pidfile)
            print('PID:\t', pid)
            print('Version:', ev3server.__version__)

   daemon = Ev3ServerDaemon('/tmp/ev3server.pid')
   if len(sys.argv) == 2:
      if 'start' == sys.argv[1]:
         daemon.start()
      elif 'stop' == sys.argv[1]:
         daemon.stop()
      elif 'restart' == sys.argv[1]:
         daemon.restart()
      elif 'status' == sys.argv[1]:
         daemon.status()
      else:
         print("Unknown command")
         sys.exit(2)
      sys.exit(0)
   else:
      print("usage: %s start|stop|status|restart" % sys.argv[0])
      sys.exit(2)
