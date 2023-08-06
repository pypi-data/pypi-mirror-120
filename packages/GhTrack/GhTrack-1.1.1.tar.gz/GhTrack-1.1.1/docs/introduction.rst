Introduction
============

github-track is a Python library to use the `Github API v3 <http://developer.github.com/v3>`__.
With it, you can pull any public repositories pull requests from Python scripts.
**Sending email currently work only with sendGrid**

Download and install
--------------------

First of all make sure you have install python in your machine and the version is higher than `3.6`. If not please process as follow to install it.
.. code-block:: bash
>> brew install python@3.9

**Installation using pip**

The easiest way to install is to use  [Python Package Index](https://pypi.org/project/GhTrack/),
so, a pip install should be enough.
.. code-block:: bash
>> pip3 install GhTrack


**Installation by cloning the source code**
If you have done the installation using pip, you can ignore this part.
To use it please clone the [github-track](https://github.com/zinaLacina/github-track) repository.
.. code-block:: bash
>> git clone https://github.com/zinaLacina/github-track

Once it clone please cd into the directory
.. code-block:: bash
>> cd  github-track

Once inside the direction check that you have the latest up to date of the setuptools.
.. code-block:: bash
 python3 -m pip install --upgrade setuptools

 And lastly install the *module*
.. code-block:: bash
 python3 setup.py install

 And you are all set for to run the application.

Short tutorial
---------------------
Let's test the base features of the module, that consist to pull the last
7 days pull requests of a public repo.
By default the module has default value in the settings located in the data folder.
The default repo is ``kubernetes``.
So to get the list of the last 7 days pull requests of the ``kubernetes`` repo.

Open a terminal, and in the console please type >>``python3``
After that, import the ``GhTrack`` module
.. code-block:: python
 >> from GhTrack import GhTrack
 # create GhTrack object without any params(first of all the default params)
 >> g = GhTrack()
 #That will print on the console the html of the last 7 days pull requests
 >> g.sendEmailOrPrintConsole(emailNotConsole=False)

You can also get the json format of the last 7 days pull requests
.. code-block:: python
   >>  from GhTrack import GhTrack
   >> g = GhTrack()
   >> pulls = g.getPulls()
   #json format
   >> pulls
Then play with your Github objects::

    for pull in pulls:
        print(pull["title"])




Licensing
---------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
