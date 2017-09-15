#http://stackoverflow.com/questions/22386072/capturing-netcat-shell-command-output-in-python
#import os
#output = os.popen("netcat -l 6000").read()
#print(output) #doesn't work as it's getting caught on the above

from sh import nc
output = nc("-l", "6000")
print(output)