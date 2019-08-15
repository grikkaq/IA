
#   Assuming EOL control character is LF

import re
import sys
#import io

f = open(sys.argv[1], "rb").read()
f_splitted = re.split("\n\n", f) # headers @ f_splitted[0] + data @ f_splitted[1]
 
# first line either METHOD + ARG + HTTP_Ver, or HTTP_Ver + STATUS + REASON_PHRASE
ffline = f_splitted[0].split("\n", 1)[0].split(" ", 2)
ffline = list(filter(None, ffline)) # drop empty strings to ensure abs_path was provided or not

if ( re.match( r"HTTP+", ffline[0], re.I ) ):
    message_type = "response"
    summary = ffline[1] + " " + ffline[2]
else:
    message_type = "request"
    x = re.search("Host: [^\\n]+", f_splitted[0] + "\n") # +"\n" in case and Host is the last header 
    host =  f_splitted[0][ x.start() + len("Host: ") : x.end() ] if x else ""  # port is included
    abs_path = ffline[1].split("?", 1)[0] if len(ffline) == 3 else "/"
    url = "http://" + host + abs_path if (ffline[0] != "OPTIONS" or ffline[1] != "*") else "*"
    summary = ffline[0] + " " + url
    
print( summary, end = " " )

body_size = len(f_splitted[1]) if f_splitted[1] else 0

request_headers = { "Accept-Charset", "Accept-Encoding", "Accept-Language", \
                    "Authorization", "Expect", "From", "Host", "If-Match", \
                    "If-Modified-Since", "If-None-Match", "If-Range", \
                    "If-Unmodified-Since", "Max-Forwards", "Proxy-Authorization", \
                    "Range", "Referer", "TE", "User-Agent" }
response_headers = { "Accept-Ranges", "Age", "ETag", "Location", "Proxy-Authenticate", \
                    "Retry-After", "Server", "Vary", "WWW-Authenticate" }
                    
headers = [line.split(":", 1)[0] for line in f_splitted[0].split("\n")[1:] ] 
x = len(set(headers).intersection(request_headers if message_type == "request" else response_headers))
print("(", x, "headers, ", body_size, "bytes)" )
