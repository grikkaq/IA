#   Assuming EOL control character is LF

import re
#import io

f = fopen(sys.args[1], "rb")
f_splitted = re.split("\n\n", f) # headers @ f_splitted[0] + data @ f_splitted[1]
 
#   first line either METHOD + ARG + HTTP_Ver, or HTTP_Ver + STATUS + REASON_PHRASE
ffline = f_splitted[0].split("\n", 1)[0].split(" ", 2)
ffline = list(filter(None, ffline)) # drop empty strings

if ( re.match( r"HTTP+", ffline[0], re.I ) ):
    out1 = ffline[1] + " " + ffline[2]
else:
    x = re.search("Host: [^\\n]+", f_splitted[0] + "\n") # +"\n" in case and Host is the last header 
    host =  f_splitted[0][ x.start() + len("Host: ") : x.end() ] if x else ""  # port is included
    abs_path = ffline[1].split("?", 1)[0] if len(ffline) == 3 else "/"
    url = "http://" + host + abs_path if (ffline[0] != "OPTIONS" or ffline[1] != "*") else "*"
    out1 = ffline[0] + " " + url
    
print( out1, end = " " )



