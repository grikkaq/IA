
#   Assuming EOL control character is LF

import re
import sys

f = open(sys.argv[1], "r").read()
# Split file in 2 parts: headers & params @ f_splitted[0] and message body @ f_splitted[1]
file_splitted = f.split("\n\n", 1) 

# First line either METHOD + ARG + HTTP_Ver, or HTTP_Ver + STATUS + REASON_PHRASE
first_line = file_splitted[0].split("\n", 1)[0].split(" ", 2)
# Drop empty strings to ensure abs_path was provided or not
first_line = list(filter(None, first_line)) 

if re.match(r"HTTP+", first_line[0], re.I):
    message_type = "response"
    out = first_line[1] + " " + first_line[2]
else:
    message_type = "request"
    # Add LF to the end to find Host if it's the last header 
    x = re.search("Host:[^\\n]+", file_splitted[0] + "\n") 
    host =  file_splitted[0][x.start() + len("Host: ") : x.end()] if x else ""  # Port is included
    abs_path = first_line[1].split("?", 1)[0] if len(first_line) == 3 else "/"
    url = "http://" + host + abs_path if (first_line[0] != "OPTIONS" or first_line[1] != "*") else "*"
    out = first_line[0] + " " + url
    
request_headers = { "Accept-Charset", "Accept-Encoding", "Accept-Language", 
                   "Authorization", "Expect", "From", "Host", "If-Match", 
                   "If-Modified-Since", "If-None-Match", "If-Range", 
                    "If-Unmodified-Since", "Max-Forwards", "Proxy-Authorization", 
                    "Range", "Referer", "TE", "User-Agent" }
response_headers = { "Accept-Ranges", "Age", "ETag", "Location", "Proxy-Authenticate", 
                    "Retry-After", "Server", "Vary", "WWW-Authenticate" }
# Get first word of every line excluding 1st: headers them are
headers = [ line.split(":")[0] for line in file_splitted[0].split("\n")[1:] ] 
headers_matched = len(response_headers.intersection(headers)) if message_type == "response" \
                        else len(request_headers.intersection(headers))
body_size = len(file_splitted[1]) if len(file_splitted) > 1 else 0  

print(out, " (", headers_matched, " headers, ", body_size , "bytes )")
