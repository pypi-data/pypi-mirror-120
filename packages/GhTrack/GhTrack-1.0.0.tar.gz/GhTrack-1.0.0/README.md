Introduction
============

github-track is a Python library to use the [Github API v3](http://developer.github.com/v3). With it, you can pull any public repositories pull requests from Python scripts. **Sending email currently work only with sendGrid**
The full documentation can be found here [github-track full docs](https://zinalacina.github.io/github-track/index.html)
In the examples section of the docs, you can learn how to parse a configuration file to the module and much more.

Download and install
--------------------

First of all make sure you have install python in your machine and the version is higher than `3.6`. If not please process as follow to install it. 
```bash 
brew install python@3.9
```

To use it please clone the [github-track](https://github.com/zinaLacina/github-track) repository.
```bash
git clone https://github.com/zinaLacina/github-track
```
Once it clone please cd into the directory 
```bash
cd  github-track
```
Once inside the direction check that you have the latest up to date of the setuptools. 
 ```bash
 python3 -m pip install --upgrade setuptools
 ```
 And lastly install the *module* 
 ```bash
 python3 setup.py install
 ``` 
 And you are all set for to run the application.

FYI: This package will be release in the [Python Package Index](https://github.com/zinaLacina/github-track), so, once done by using 
```bash 
pip install ghtrack
``` 
should be enough.

Short tutorial
--------------

Let's test the base features of the module, that consist to pull the last 7 days pull requests of a public repo. By default the module has default value in the settings located in the data folder. The default repo is `kubernetes`. So to get the list of the last 7 days pull requests of the `kubernetes` repo.

Open a terminal, and in the console please type.
```bash
>> python3
``` 
After that, import the `GhTrack` module 
```bash
>> from GhTrack import GhTrack
# create GhTrack object without any params(first of all the default params)
>> g = GhTrack() 
#Print on the console the html of the last 7 days pull requests 
>> g.sendEmailOrPrintConsole(emailNotConsole=False)
```

You can also get the json format of the last 7 days pull requests 
```bash
>> from GhTrack import GhTrack 
>> g = GhTrack() 
>> pulls = g.getPulls()
#Print the json format 
>> pulls
```
Then play with your GhTrack objects:
```bash
>> for pull in pulls:
>> ...print(pull["title"])
```

Licensing
---------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means. In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to \<<https://unlicense.org>\>
