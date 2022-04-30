#!/usr/bin/env python   
from __future__ import division
from __future__ import print_function
import argparse
import codecs
import logging
import os
import sys
from impacket.examples import logger
from impacket.examples.utils import parse_target
from impacket.smbconnection import SMBConnection

from impacket.examples.secretsdump import  RemoteOperations, NTDSHashes
from impacket.krb5.keytab import Keytab



import subprocess


import hashlib,binascii
try:
    input = raw_input
except NameError:
    pass



wordliste = ""
hashcatPath = ""

def phase3(badUser):

    subprocess.run('./hashcat-6.2.5/')

    import os
    if os.path.exists("badUser.txt"):
        os.remove("badUser.txt")
    if os.path.exists("dumb.ntds"):
        os.remove("dumb.ntds")
    if os.path.exists("onlyHashes.txt"):
        os.remove("onlyHashes.txt")

    with open("badUser.txt","w") as f:
        for user, hash in badUser.items():
            f.write(user + "\n")
        
    pass


# Callback function for py7zr.SevenZipFile 





def phase2():


    print("[*] Reading found hashes...")
    foundHashesFile =  open('dumb.ntds',"r", encoding="utf8",errors="ignore") 
    foundHashes = {}  
    #loop through the file and find the hash
    for line in foundHashesFile:
        hash = line.split(":")[3].lower()
        user = line.split(":")[0]
        foundHashes[user] = hash
        
    print("Found {} hashes".format(len(foundHashes)))
    foundHashesFile.close()

    if os.path.exists("onlyHashes.txt"):
        os.remove("onlyHashes.txt")
    with open("onlyHashes.txt", "w") as f:
        for user, hash in foundHashes.items():
            f.write(user+":"+hash+"\n")

    

    # Print hashes into a file
    

    
    # Call subprocess to run hashcat
    file = open(wordliste,"r")
    wordlistPath = os.path.realpath(file.name)
    file.close()

    file = open("onlyHashes.txt","r")
    onlyHashPath = os.path.realpath(file.name)
    file.close()

    print("[*] Running hashcat...")
    file = open(hashcatPath,"r")
    hashcatPathFull = os.path.realpath(file.name)
    file.close()

    hashcatPathFullSplitted = hashcatPathFull.split("\\")
    binary = hashcatPathFullSplitted[-1]
    
    hashcatPathFull = hashcatPathFull.replace("\\"+binary,"")

    
    print("[*] Running " + binary + "...")
    print("[*] Folder " + hashcatPathFull)
    str = binary+' -m 1000 -a 0 --username --outfile-format=3 "' + onlyHashPath + '" "' + wordlistPath + '" -o ./badUser.txt -O -I'
    print(str)
    subprocess.run(str,cwd=hashcatPathFull,shell=True)
    os.abort()




    foundHashesFile =  open('dumb.ntds',"r", encoding="utf8",errors="ignore") 
    foundHashes = {}   

    print("[*] Reading found hashes...")
    #loop through the file and find the hash
    for line in foundHashesFile:
        hash = line.split(":")[3].lower()
        user = line.split(":")[0]
        foundHashes[user] = hash
        
    print("Found {} hashes".format(len(foundHashes)))
    foundHashesFile.close()

    wordlistFile = open(wordlist,"r", encoding="utf8",errors="replace")
    knownBadHashes = []
    print("[*] Reading wordlist...")
    for line in wordlistFile:
        line = line.strip("\n\t\r")
        
        ntlm_hash = binascii.hexlify(hashlib.new('md4', line.encode('UTF-16LE')).digest()).decode('utf-8').lower()
        knownBadHashes.append(ntlm_hash)
        
    print("Found hashes:", len(knownBadHashes))
    wordlistFile.close()

    print("[*] Comparing hashes...")
    #foreach key and value in foundHashes dictonary
    badUser = {}
    for user, hash in foundHashes.items():
        if hash in knownBadHashes:
            badUser[user] = hash
            print("[*] Hash found: " + hash + " for user: " + user)

    phase3(badUser)
    #print(knownBadHashes)


def phase1():
    
    if sys.stdout.encoding is None:
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    parser = argparse.ArgumentParser(add_help = True, description = "Performs various techniques to dump secrets from "
                                                      "the remote machine without executing any agent there.")

    parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
    parser.add_argument('-w', action='store',  help='A wordlist file (password per line) to try.')
    parser.add_argument('-hashcat', action='store',  help='Path to Hashcat Executable or Binary')
    group = parser.add_argument_group('authentication')

    group.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
    group.add_argument('-no-pass', action="store_true", help='don\'t ask for password (useful for -k)')
    group.add_argument('-k', action="store_true", help='Use Kerberos authentication. Grabs credentials from ccache file '
                             '(KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use'
                             ' the ones specified in the command line')
    group.add_argument('-aesKey', action="store", metavar = "hex key", help='AES key to use for Kerberos Authentication'
                                                                            ' (128 or 256 bits)')
    group = parser.add_argument_group('connection')
    group.add_argument('-dc-ip', action='store',metavar = "ip address",  help='IP Address of the domain controller. If '
                                 'ommited it use the domain part (FQDN) specified in the target parameter')
    group.add_argument('-target-ip', action='store', metavar="ip address",
                       help='IP Address of the target machine. If omitted it will use whatever was specified as target. '
                            'This is useful when target is the NetBIOS name and you cannot resolve it')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()
    options.ts = False
    options.debug = False
    options.system = None
    options.bootkey = None
    options.security = None
    options.sam = None
    options.ntds = None
    options.resumefile = None
    options.outputfile = 'dumb'
    options.use_vss = False
    options.exec_method = 'smbexec'
    options.just_dc = False
    options.just_dc_user = None
    options.just_dc_ntlm = True
    options.pwd_last_set = False #changed to false
    options.user_status = False # changed to false
    options.history = False
    options.hashes = None
    options.aesKey = None
    options.keytab = None
    options.dc_ip = None

  

    if options.w is None:
        print("[!] You have to specify the location of the password file (option -w)")
        sys.exit(1)
    if options.hashcat is None:
        print("[!] You have to specify the location of the hashcat binary (option -hashcat)")
        sys.exit(1)
    
    logger.init(options.ts)

    logging.getLogger().setLevel(logging.INFO)

    domain, username, password, remoteName = parse_target(options.target)

    if options.target_ip is None:
        options.target_ip = remoteName

    if domain is None:
        print("No domain is not possible, try specifying your credentials")
        sys.exit(1)

   

    if password == '' and username != '' and options.hashes is None and options.no_pass is False and options.aesKey is None:
        from getpass import getpass

        password = getpass("Password:")

   

    dumper = DumpSecrets(remoteName, username, password, domain, options)

    global wordliste
    wordliste = options.w
    global hashcatPath
    hashcatPath = options.hashcat
    try:
        dumper.dump()
        
        phase2()
    except Exception as e:
        if logging.getLogger().level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        logging.error(e)

    

def main():
    phase1()

class DumpSecrets:
    def __init__(self, remoteName, username='', password='', domain='', options=None):
        self.__useVSSMethod = options.use_vss
        self.__remoteName = remoteName
        self.__remoteHost = options.target_ip
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = options.aesKey
        self.__smbConnection = None
        self.__remoteOps = None
        self.__SAMHashes = None
        self.__NTDSHashes = None
        self.__LSASecrets = None
        self.__systemHive = options.system
        self.__bootkey = options.bootkey
        self.__securityHive = options.security
        self.__samHive = options.sam
        self.__ntdsFile = options.ntds
        self.__history = options.history
        self.__noLMHash = True
        self.__isRemote = True
        self.__outputFileName = options.outputfile
        self.__doKerberos = options.k
        self.__justDC = options.just_dc
        self.__justDCNTLM = options.just_dc_ntlm
        self.__justUser = options.just_dc_user
        self.__pwdLastSet = options.pwd_last_set
        self.__printUserStatus= options.user_status
        self.__resumeFileName = options.resumefile
        self.__canProcessSAMLSA = True
        self.__kdcHost = options.dc_ip
        self.__options = options

        if options.hashes is not None:
            self.__lmhash, self.__nthash = options.hashes.split(':')

    def connect(self):
        self.__smbConnection = SMBConnection(self.__remoteName, self.__remoteHost)
        if self.__doKerberos:
            self.__smbConnection.kerberosLogin(self.__username, self.__password, self.__domain, self.__lmhash,
                                               self.__nthash, self.__aesKey, self.__kdcHost)
        else:
            self.__smbConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)

    def dump(self):
        try:
            
            self.__isRemote = True
            bootKey = None
            try:
                try:
                    self.connect()
                except Exception as e:
                    if os.getenv('KRB5CCNAME') is not None and self.__doKerberos is True:
                        # SMBConnection failed. That might be because there was no way to log into the
                        # target system. We just have a last resort. Hope we have tickets cached and that they
                        # will work
                        logging.debug('SMBConnection didn\'t work, hoping Kerberos will help (%s)' % str(e))
                        pass
                    else:
                        raise

                self.__remoteOps  = RemoteOperations(self.__smbConnection, self.__doKerberos, self.__kdcHost)
                self.__remoteOps.setExecMethod(self.__options.exec_method)
                
            except Exception as e:
                self.__canProcessSAMLSA = False
                if str(e).find('STATUS_USER_SESSION_DELETED') and os.getenv('KRB5CCNAME') is not None \
                    and self.__doKerberos is True:
                    # Giving some hints here when SPN target name validation is set to something different to Off
                    # This will prevent establishing SMB connections using TGS for SPNs different to cifs/
                    logging.error('Policy SPN target name validation might be restricting full DRSUAPI dump. Try -just-dc-user')
                else:
                    logging.error('RemoteOperations failed: %s' % str(e))
            NTDSFileName = None
           

            self.__NTDSHashes = NTDSHashes(NTDSFileName, bootKey, isRemote=self.__isRemote, history=self.__history,
                                           noLMHash=self.__noLMHash, remoteOps=self.__remoteOps,
                                           useVSSMethod=self.__useVSSMethod, justNTLM=self.__justDCNTLM,
                                           pwdLastSet=self.__pwdLastSet, resumeSession=self.__resumeFileName,
                                           outputFileName=self.__outputFileName, justUser=self.__justUser,
                                           printUserStatus= self.__printUserStatus)
            try:
                self.__NTDSHashes.dump()

            except Exception as e:
                logging.error(e)
                if self.__justUser and str(e).find("ERROR_DS_NAME_ERROR_NOT_UNIQUE") >=0:
                    logging.info("You just got that error because there might be some duplicates of the same name. "
                                 "Try specifying the domain name for the user as well. It is important to specify it "
                                 "in the form of NetBIOS domain name/user (e.g. contoso/Administratror).")
                
            self.cleanup()
        except (Exception, KeyboardInterrupt) as e:
            logging.error(e)
            try:
                self.cleanup()
                
            except:
                pass

    def cleanup(self):
        logging.info('Cleaning up... ')
        if self.__remoteOps:
            self.__remoteOps.finish()
        if self.__NTDSHashes:
            self.__NTDSHashes.finish()




if __name__ == '__main__':
    main()