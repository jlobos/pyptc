#pyptc
The pyptc is a simple script that automates work platforms ptc, written in python by [@27sawyer] .

    > PTC supported: neobux(required page in Spanish)

### Installation
```sh
:~# pip install selenium
:~# pip install beautifulsoup4
:~# pip install requests
:~$ git clone https://github.com/27Sawyer/pyptc.git
:~$ cd pyptc
:~$ python pyptc.py -h
               __  .__                 __________  __
______ ___.___/  |_|  |__   ____   ____\______   _/  |_  ____
\____ <   |  \   __|  |  \ /  _ \ /    \|     ___\   ___/ ___\.
|  |_> \___  ||  | |   Y  (  <_> |   |  |    |    |  | \  \___
|   __// ____||__| |___|  /\____/|___|  |____|    |__|  \___  >
|__|   \/               \/            \/        bot for ptc \/

Version     :   beta 1.0
Author      :   @27Sawyer

usage: pyptc.py [-h] -ptc ptc -u user -p pass

optional arguments:
  -h, --help            show this help message and exit
  -ptc ptc, --ptc ptc   [required] ptc name (neobux)
  -u user, --user user  [required] user
  -p pass, --password pass
                        [required] password
:~$ python pyptc.py -ptc neobux -u user -p password
```

### License
GPLv2


[@27sawyer]:https://twitter.com/27Sawyer
