# CyberRaven Securities

"""

    RavenBuster is a directory and file busting tool that has functionality to find
    directories and files using dictionary attack technique. In order to use this tool,
    you will be needed a dictionary or a wordlist file.

    Be careful using the tool in multi-threaded mode since it can be treated as DoS
    attack and your IP can be blocked by the cloud host.


    This tools is developed by Nitin Choudhury, Founder and CEO of CyberRaven Securities.

    Thank You.

"""

import requests
import threading
import argparse


def banner():
    poster = '''

__________                           ________  .__      __________                __                
\______   \_____ ___  __ ____   ____ \______ \ |__|_____\______   \__ __  _______/  |_  ___________ 
 |       _/\__  \\\\  \/ // __ \ /    \ |    |  \|  \_  __ \    |  _/  |  \/  ___/\   __\/ __ \_  __ \\
 |    |   \ / __ \\\\   /\  ___/|   |  \|    `   \  ||  | \/    |   \  |  /\___ \  |  | \  ___/|  | \/
 |____|_  /(____  /\_/  \___  >___|  /_______  /__||__|  |______  /____//____  > |__|  \___  >__|   
        \/      \/          \/     \/        \/                 \/           \/            \/      
01010010 01100001 01110110 01100101 01101110 01000100 01101001 01110010 01000010 01110101 01110011 01110100 01100101 01110010 
            
                                                        DEVELOPED BY                                                                                                            
                                                       Nitin Choudhury
                                                     Founder @RavenCyber
-------------------------------------------------------------------------------------------------------------------------------
    
    '''

    print(poster)

class Buster:

    def __init__(self, URL):
        self.URL = URL
        self.wordfile = "./wordlists/medium.txt"
        self.thread = 1
        self.recursive = False
        self.extenstions = None
        self.status_codes = [200]


    def check(self, word):
        url = '/'.join([self.URL, word])
        response = requests.get(url)

        if response.status_code in self.status_codes:
            print("URL:", url, "Status:", response.status_code)


    def runNonRecursive(self):
        wordlist = open(self.wordfile).read().split('\n')

        for wordID in range(len(wordlist)):
            t = threading.Thread(target=self.check, args=(wordlist[wordID], ))
            t.start()

            if wordID%self.thread==0:
                t.join()
            elif (wordID+1)%len(wordlist)==0:
                t.join()


    def runRecursive(self, URL):
        wordlist = open(self.wordfile).read().split('\n')

        for wordID in range(len(wordlist)):
            url = '/'.join([URL, wordlist[wordID]])

            response = requests.get(url)

            if response.status_code in self.status_codes:
                print("URL:", url, "Status:", response.status_code)
                self.runRecursive(url)


    def runExtension(self):
        wordlist = open(self.wordfile).read().split('\n')

        for wordID in range(len(wordlist)):
            for ext in self.extenstions:
                t = threading.Thread(target=self.check, args=(wordlist[wordID]+'.'+ext, ))
                t.start()

                if wordID%self.thread==0:
                    t.join()
                elif (wordID+1)%len(wordlist)==0:
                    t.join()



if __name__ == '__main__':

    try:
        banner()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-u", "--url",
            type=str,
            help="Set URL",
            required=True
        )

        parser.add_argument(
            "-w", "--wordlist",
            type=str,
            help="Set wordlist file [Default: ./wordlists/medium.txt]",
            required=False
        )

        parser.add_argument(
            "-t", "--thread",
            type=int,
            help="Set thread",
            required=False
        )

        parser.add_argument(
            "-e", "--extension",
            type=str,
            help="Set extensions",
            required=False
        )

        parser.add_argument(
            "-s", "--status",
            type=str,
            help="Set status code [Default: 200]",
            required=False,
        )

        parser.add_argument(
            "--recursion",
            type=bool,
            help="Set recursive mode: True/False [Default: False]",
            required=False,
        )

        args = parser.parse_args()


        URL = args.url


        buster = Buster(URL=URL)

        if args.wordlist:
            wordlist = args.wordlist
            buster.wordfile = wordlist

        if args.thread:
            thread = args.thread
            buster.thread = thread

        if args.extension:
            extensions = args.extension.split(',')
            buster.extenstions = extensions

        if args.status:
            status_codes = list(map(int, args.status.split(',')))
            buster.status_codes = status_codes

        if args.recursion:
            recursion = args.recursion
            buster.recursive = recursion


        if args.recursion and args.thread:
            print("Recursion and Thread can't run at the same time !")

        elif args.recursion and args.extension:
            print("Recursion and Extension can't run at the same time !")

        elif args.extension:
            buster.runExtension()

        elif args.recursion==True:
            buster.runRecursive(buster.URL)

        else:
            buster.runNonRecursive()

    except KeyboardInterrupt:
        pass

    except requests.exceptions.ConnectionError:
        print("[!] Check Your Internet Connectivity !")