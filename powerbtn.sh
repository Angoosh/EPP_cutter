#! /bin/sh

case "$1" in
  start)
    echo "Starting powerbtn.py & IP.py"
    python3 /usr/local/bin/powerbtn.py &
    python3 /usr/local/bin/IP.py &
    ;;
  stop)
    echo "Stopping powerbtn.py & IP.py"
    pkill -f /usr/local/bin/powerbtn.py
    pkill -f /usr/local/bin/IP.py
    ;;
  *)
    echo "Usage: /etc/init.d/powerbtn.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
