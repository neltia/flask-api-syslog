var=$(ps -ef | grep -e 'python3 app.py' | grep -v $0)
pid=$(echo ${var} | cut -d " " -f2)

echo $var
echo $pid
