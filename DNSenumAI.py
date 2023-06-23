# 18.06.2023
# Enum DNS using ChatGPT word list

import os
import openai
import dns
import dns.resolver
import socket
import argparse

def SetArgs():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-d", "--domain", help="domain to enumerate",required=True)
    argParser.add_argument("-l", "--list", help="custom domain file list",required=False)
    argParser.add_argument("-o", "--output", help="output file name",required=False)
    args = argParser.parse_args()
    return args.domain,args.list,args.output

# Set up OpenAI API key
api_key = "OpenAI_API_key"
openai.api_key = api_key
resDNS=[]

def SendToBot(domain):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    tok=3800
    message_log={"role": "system", "content": "you are a professional cyber security penetration tester"},{"role": "assistant", "content": 'Using the rules defined in RFC1034 and the other RFCs which impact fully qualified domain names (FQDN), generate a list of 50 more potential DNS names based on any observable patterns based on domain:'+domain+ ' Do not explain, orginize as list, with bulets'}
    print('Quering ChatGPT for subdomains on: '+domain)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=message_log,max_tokens=tok,stop=None, temperature=0.9)
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message.content

def ReadFile(d):
    try:
        with open(d,"r") as f:
            dictionary = f.read().splitlines()
    except:
        print('error opening file: '+ d)

def ReverseDNS(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return None

def SubdomainSearch(domain, dictionary,nums):
    successes = []
    for word in dictionary:
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)

def prntans(ans):
    resDNS.append(ans)
    resDNS.append("Domain Names: %s" % ReverseDNS(ans.to_text())) # do reverse lookup
    resDNS.append('--- --- ---')


def DNSRequest(domain):
    ips = []
    try:
        result = dns.resolver.resolve(domain)
        if result:
            resDNS.append(domain)
            for answer in result:
                prntans(answer)
                print (domain+' is valid')
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips

def SaveToFile(fn,txt): #saving list to file
    print('Saving results to file: '+fn)
    file_path = os.path.dirname(os.path.realpath(__file__))
    LogFile=file_path+'/'+fn
    with open(LogFile, "w") as file1:
        for lin in txt:
            file1.write(str(lin)+ '\n')
    file1.close

def main():
    dom=SetArgs()
    # dom[0]=domain to check
    # dom[1]= subdomain list file
    #  dom[2]= output file name
    ans=SendToBot(dom[0])
    splt1=ans[2:].split('\n- ')
    SubDo=[]
    splt2=[]
    x=0
    print('ChatGPT subsomains are:')
    for lst in splt1:
        splt2.append(lst.split('.')) #Adding subdomains from ChatGPT
        SubDo.append(splt2[x][0])
        x+=1
    SubDo = list(dict.fromkeys(SubDo)) # removing duplicates
    for item in SubDo:
        print(item) # printing items
    if dom[1] is not None:
        SubDo.append(ReadFile(dom[1]))# adding subdomains from file
    print('Checking DNS subdomains ...')
    SubdomainSearch(dom[0],SubDo,True)
    print('results:')
    for line in resDNS:
        print(line)
    if dom[2] is not None:
        SaveToFile(dom[2],resDNS)

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
