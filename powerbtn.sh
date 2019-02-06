#! /bin/sh

case "$1" in
  start)
    echo "Starting powerbtn.py"
    python3 /usr/local/bin/powerbtn.py &
    ;;
  stop)
    echo "Stopping powerbtn.py"
    pkill -f /usr/local/bin/powerbtn.py
    ;;
  *)
    echo "Usage: /etc/init.d/powerbtn.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
