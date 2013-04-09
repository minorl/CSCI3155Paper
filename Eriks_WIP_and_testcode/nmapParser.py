#! /usr/bin/python

import sys              #includes the sys.arg[] command line options
import re               #includes the ability to use regular expressions
import subprocess       #includes ability to ping an ip address

#Originally Written by Erik Kierstead to Scan and Parse Network Devices
#for the Research Computing Group

#------------------------------------------------------------------------
#Pings Address:

def scan_ips(ip_address):

        #Empty Lists to Append Host Discovered by NMAP:
        seperateList = []
        findHosts = []

        #Loop Control Index Vars:
        j = 0
        k = 0

        #Calls NMAP to Scan IP / Range of IPs:
        nmap_out = subprocess.Popen(["nmap", "-sP", ip_address, "-oG", "-"], stdout=subprocess.PIPE)

        #Using Output Provided by subprocess.PIPE A String is Created:
        nmap_string = str(nmap_out.communicate())

        #Separates IP Address Into Four Variables:
        for i in nmap_string.split("\\n"):
                seperateList.append(i)

        #Sorts List for Hosts that Are Up:
        while (j < len(seperateList)):
                if "Host" in seperateList[j] and "Up" in seperateList[j]:
                        findHosts.append(seperateList[j])
                j +=1

        return findHosts

#------------------------------------------------------------------------

#------------------------------------------------------------------------
def parse_data(host_list, host_ips, host_names):

        #While Loop Index:
        i = 0;

        #Reg. Ex's Used to Sort Discovered IP Addresses and Host Names:
        byteIPPattern = "\d+\.\d+\.\d+\.\d+"
        byteHostPattern = "\(.+\)"
        IPExpression = re.compile(byteIPPattern, re.IGNORECASE)
        HOSTExpression = re.compile(byteHostPattern, re.IGNORECASE)

        #Pulls Results of NMAP Scan One Result at A Time
        #Seperates Using Regular Expressions Then Puts in Individual
        #Lists as Strings:

        while (i < len(host_list)):

                #Individual Line of NMAP Results:
                temp_var = str(host_list[i])

                #Search NMAP Results for Individual Block of IP / Host:
                temp_ips = IPExpression.search(temp_var)
                temp_hosts = HOSTExpression.search(temp_var)

                #Appends Into List, Converts To Str and Strips ()'s:
                host_ips.append(str(temp_ips.group()))

                if temp_hosts is not None:
                        host_names.append(str(temp_hosts.group()).strip('(' ')'))

                else:
                        host_names.append("unknown-host")
                i += 1

        #Lists Are Always Passed By Reference - No Need To Return Them:
        return;

#------------------------------------------------------------------------

#------------------------------------------------------------------------
#Main Script:

#Requires Start and Stop IP Ranges, or Individual IP/Hosts:

if len(sys.argv) <= 1:
        print( "IP Address(es)/Hosts, Ranges (10.0.0.1-10, etc.) Required" )
        sys.exit(1)

else:

	host_list = []
        host_names = []
	host_ips = []

        #Pulls IP and Range from Command Line Argument:
        get_ip = sys.argv[1]

        #Scans Network IP / Range (with NMAP) and Finds Valid IPs:
        host_list = scan_ips(get_ip);

	parse_data(host_list, host_ips, host_names)

	#Prints Valid IPs:
	print
	print("Original stdin:")
	print(host_list)
	print
	print("Parsed Input:")
	print(host_ips)
	print
	print(host_names)
#------------------------------------------------------------------------
