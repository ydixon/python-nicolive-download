Python script to download nicolive timeshifted videos
=======================================================
Fetch rtmpdump parameters from NicoNico website and feed them directly to rtmpdump

Install
==============================
```
git clone https://github.com/ydixon/python-nicolive-download.git
cd python-nicolive-download
git submodule init
git submodule update
cd rtmpdump-ksv-nicolive
make
sudo make install
```

Usage
===============================
Set user login and password in **nicoliverecord.py**
```
mail_tel = "" #set login name
password = "" #set password
```

In terminal
```
python nicoliverecord.py -l <liveid>

Example:
python nicoliverecord.py -l lv54345634
```
