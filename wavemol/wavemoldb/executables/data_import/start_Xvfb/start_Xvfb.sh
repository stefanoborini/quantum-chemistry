pid=`ps uawx |grep "Xvfb :5" | grep -v grep | awk '{print $2}'`
if test "x$pid" != "x"; then
    echo "X vfb already running"
    exit 0
fi

echo "Starting X virtual framebuffer on :5"
Xvfb :5 &
sleep 5

pid=`ps uawx |grep "Xvfb :5" | grep -v grep | awk '{print $2}'`
if test "x$pid" != "x"; then
    echo "X vfb successfully started"
    exit 0
else
    echo "ERROR! X vfb cannot start."
    exit 1
fi

