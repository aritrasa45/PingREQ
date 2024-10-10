


# http request


import requests
import time
import sys
import socket
import argparse
import threading
import os
import random



R = '\033[31m' # red 
G = '\033[32m' # green 
Y = '\033[33m' # yellow
B = '\033[34m' # blue
C = '\033[36m' # cyan
M = '\033[35m' # magenta

E = '\033[0m' # end
BLD = '\033[1m' # bold




sock = socket.socket()


parser = argparse.ArgumentParser(description='pingREQ V1 How to use ------->>>')

parser.add_argument('url', type=str, help='the url to ping for ex (google.com) ', default=None)

parser.add_argument('--timeout', type=int, help= 'its the script timeout when the script exits after certain amount of get request',  default = 100000 )

parser.add_argument('--sleep', type=int, help= 'the short delay before doing next ping [default: 0]',  default = 0 )

parser.add_argument('--thread_value', type=int, help= 'to add multiple thread to run with given threads number [default: 0] ',  default = 0 )

parser.add_argument('--retry', type=int, help= 'to retry again if the script fails to run due to any errors',  default = 0 )

parser.add_argument('--data', type=str, help= ' to send some data to the given url',  default = None )

parser.add_argument('--proxy', type=str, help= ' to send get requests with given proxy',  default = None )




args = parser.parse_args()




sum = 0
average = []

processes = []


  
def avg_counter():
    
    global average 
    global sum
    
    for i in range(len(average)):
        sum += average[i]           
    sum = round(sum / len(average), 2 )       
   



def show_output(IP):
        
    
    db = [
    
    f"IP : {IP} | " , 
    f"timeout : {args.timeout} | " , 
    f"sleep : {args.sleep} | " , 
    f"thread_ value : {args.thread_value} | " , 
    f"data : {args.data} | " ,
    f"proxy : {args.proxy} | " ,
    f"retry : {args.retry} | " ,
    f"avg : {sum}\n" , 
    
    
    
    ]
       
  
    print(f"\n\t-- {args.url} | statistics -- \n")
    
    for _ in range(len(db)):
        print(db[_] , end="")




                  
def kill_processes(error):
    
    
    global processes
    
    if args.thread_value > 0 and args.retry == 0:
        
        for process in processes:
            process = None
        print(error)   
        sys.exit()         
        
    else:
        if args.retry > 1:
            
            args.retry -= 1
            print(error)
            
            
        else:
            if args.thread_value > 0:
                for process in processes:
                    process = None
                print(error)            
                sys.exit(0)
            
            else:
                print(error)           
                sys.exit()
   
                     

proxies_all = []
data_all = []


def get_ping():
    
    global average
    global sum
    global proxies_all
    
    
    if proxies_all:
        proxy_db = {
        
            "http": random.choice(proxies_all) , 
            "https" : random.choice(proxies_all) ,
            
      }

    else:        
        proxy_db = None                                                                                                         
    if data_all:
        data_db = [
        
            random.choice(data_all)
               
        ]    
        
    else:
        data_db = None        
    
    if not args.timeout > 0:
        
        Errmsg = "invalid number of timeout choosen"
        print(Errmsg)
        sys.exit()
        
        
    print(f"connecting to [{args.url}] {args} \n")
    while args.timeout != 0:
    
        try:
            
            host = socket.gethostbyname(args.url)            
        
            start_time = time.time()
            response = requests.get("https://" + args.url , data=data_db, proxies=proxy_db)
            end_time = time.time()
            
            
            total = round(end_time - start_time , 2)
            average.append(total)
            
            print(f"[{R}{host}{E}] : Mode : [{Y}GET{E}] count : {C}{len(average)}{E} {R}status_code{E} : [{G}{response.status_code}{E}] time={C}{total}ms{E}")
            args.timeout -= 1
            time.sleep(args.sleep)
            
            
            
            if args.timeout == 0:
                avg_counter()
                show_output(host)
       
            
             
        except socket.gaierror as sock_err:
            sock_msg = "ConnectionError or No IP associated with hostname"
            kill_processes(sock_msg)
                     
        except requests.exceptions.ChunkedEncodingError as EncodErr:
            kill_processes(EncodError)


        except requests.exceptions.ConnectionError as connect_error:
            kill_processes(connect_error)

                                                                           
        except requests.HTTPError:
            http_error = "Http protocol error"
            kill_processes(http_error)              
                                           

        except KeyboardInterrupt:
            avg_counter()
            show_output(host)
            sys.exit()

                                                                                                    
def main():
    
    global processes
    global proxies_all
    global data_all
    
#    if args.url is None:
#        
#        print(f"the argument is required url")
#        sys.exit()


                                                                  
                                 
    if not args.proxy is None and args.proxy.endswith(".txt"):
            
        try:
            
            with open(args.proxy,"r") as f:
                proxies_ = f.read().splitlines()
                proxies_all.clear()
                proxies_all.append(proxies_)
                    
                    
        except Exception as proxyf_excp:
                kill_processes(proxyf_excp)                          
                    
    elif not args.proxy is None:
            
        try:
            host , port = args.proxy.split(":")
            socket.inet_aton(host)
            print(f"Proxy Type is valid: Trying with proxy {host}:{port}\n")
            proxies_all.append(args.proxy)
          

                                                                        
        except Exception as proxy_excp:
            kill_processes(proxy_excp)
            print("proxy invalid : Trying without proxy \n")
            args.proxy = None
            
                     
    else:
        pass



    if not args.data is None and args.data.endswith(".txt"):
        try:
            with open (args.data,"r") as data:
                data = data.read().splitlines()
                
                data_all.clear()
                data_all.append(data)
                
                


        except Exception as file_excp:
            args.data = None
            kill_processes(file_excp)


    else:
        pass


    if args.thread_value > 0:
        
        for i in range(args.thread_value):
            process = threading.Thread(target=get_ping, daemon=True)
            process.start()
           
            
    for process in processes:
        process.join()

    else:
        get_ping()

if __name__ == '__main__':
    main()             
