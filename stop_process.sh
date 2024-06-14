var=$(ps -ef | grep -e 'python3 app.py' | grep -v $0)
pid=$(echo ${var} | cut -d " " -f2)
 
if [ -n "${pid}" ]
then
    kill -9 ${pid}
    echo $* is terminated.
 
else
    echo $* is not running.
fi

