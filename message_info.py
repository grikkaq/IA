#   Assuming EOL control character is LF
import re

f = fopen(sys.args[1], "rb")
f_splitted = re.split("\n\n", f) # headers + data

# first line either METHOD + ARG + HTTP_Ver, or HTTP_Ver + STATUS + REASON_PHRASE
ffline = f_splitted[0].readline().split(" ", 2)
if ( re.match( r"HTTP+", ffline[0], re.I ) ):
    out1 = ffline[1] + " " + ffline[2]
else:
    x = re.search("Host:[^\\n]*\\n", f_splitted[0] + "\n") # +"\n" in case and Host is the last header 
    host =  f_splitted[0][ x.start() + 5 : x.end() - 1] if x else ""  
    abs_path = ffline[1].split("?", 1)[0] if len(ffline) == 3 else "/"
    
print(  )
