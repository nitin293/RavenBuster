# CyberRaven Securities

"""

    RavenBuster is a directory and file busting tool that has functionality to find
    directories and files using dictionary attack technique. In order to use this tool,
    you will be needed a dictionary or a wordlist file.

    Be careful using the tool in multi-threaded mode since it can be treated as DoS
    attack and your IP can be blocked by the cloud host.


    This tools is developed by Nitin Choudhury, Founder and CEO @CyberRaven Securities.

    Thank You.

"""


import requests
import threading
import argparse


def banner():
    poster = '''

██████╗  █████╗ ██╗   ██╗███████╗███╗   ██╗██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝
██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║██║  ██║ ╚████╔╝ ███████╗██║ ╚████║██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                             
01010010 01100001 01110110 01100101 01101110 01000010 01110101 01110011 01110100 01100101 01110010
            
                                         DEVELOPED BY                                                                                                            
                                        Nitin Choudhury
                                  Founder @RavenCyber Securities
                                        Version: 0.0.3
---------------------------------------------------------------------------------------------------
    
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


    def checkDIR(self, word):
        try:
            url = '/'.join([self.URL, word])
            response = requests.get(url)

            if response.status_code in self.status_codes:
                print("URL:", url, "Status:", response.status_code)

        except requests.exceptions.ConnectionError:
            pass

        except KeyboardInterrupt:
            pass


    def checkSUBDOMAIN(self, word):
        try:
            protocol = self.URL.split('://')[0]
            url = '.'.join([word, self.URL.split('://')[1]])
            url = '://'.join([protocol, url])
            response = requests.get(url)

            if response.status_code in self.status_codes:
                print("URL:", url, "Status:", response.status_code)

        except requests.exceptions.ConnectionError:
            pass

        except KeyboardInterrupt:
            pass


    def runNonRecursive(self, bustMode):
        wordlist = open(self.wordfile).read().split('\n')

        if bustMode=='dir':
            for wordID in range(len(wordlist)):
                t = threading.Thread(target=self.checkDIR, args=(wordlist[wordID], ))
                t.start()

                if wordID%self.thread==0:
                    t.join()
                elif (wordID+1)%len(wordlist)==0:
                    t.join()

        elif bustMode=='sub':
            for wordID in range(len(wordlist)):
                t = threading.Thread(target=self.checkSUBDOMAIN, args=(wordlist[wordID], ))
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
                t = threading.Thread(target=self.checkDIR, args=(wordlist[wordID]+'.'+ext, ))
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
            "-m", "--mode",
            type=str,
            help="Set buster mode [Directory: dir | Subdomain: sub]",
            choices=['sub', 'dir'],
            required=True
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
            help="Set recursive mode to True [Default: False]",
            choices=[True],
            required=False
        )

        args = parser.parse_args()


        URL = args.url
        bustMode = args.mode

        buster = Buster(URL=URL)

        if args.wordlist:
            wordlist = args.wordlist
            buster.wordfile = wordlist

        if args.thread:
            thread = args.thread
            buster.thread = thread

        if args.status:
            status_codes = list(map(int, args.status.split(',')))
            buster.status_codes = status_codes

        if bustMode=='dir':
            if args.extension:
                extensions = args.extension.split(',')
                buster.extenstions = extensions

            if args.recursion:
                recursion = args.recursion
                buster.recursive = recursion

            if args.extension:
                buster.runExtension()

            elif args.recursion:
                buster.runRecursive(buster.URL)

            else:
                buster.runNonRecursive(bustMode)

        elif bustMode=='sub':
            buster.runNonRecursive(bustMode)


    except KeyboardInterrupt:
        pass

    except requests.exceptions.ConnectionError:
        print("[!] Check Your Connectivity !")
