GhTrack Class
==========

This is the main class of the github-track module.

Configuration file
---------------
You can instantiate the class *GhTrack* by passing your own configuration file. Otherwise it will load with the default
configuration file. That default file looks something below.
In case if you are providing a file, it has to be the absolute path of the file.

*auth.twilioapi* can be ignored.
*github.token* is your development token that you can create through github portal.
If you are planning to pull `pull requests` more than 60 times. it is recommended to set this value to a valid token.
An invalid token, will not allow you to query `pull requests` .
*email.to* the address email to send the email.
*email.from* a valid address email verified by sendGrid in order to be able to send emails.
*email.subject* the subject of your email.
*email.sendGridApi* Your sendGrid Api key. That is used to authenticate and send email.
if you provide and invalid `api key` the application will not be able to send any email.
The *repo* section is the owner and the name of the repo you want to pull the requests. By default it is "kubernetes/kubernetes"

.. code-block:: yaml

    settings:
      auth:
        twilioapi: ""
      github:
        token: ""
      email:
        to: zinalacina@gmail.com
        from: zlacina@monbili.com
        subject: "Subject of the pull request"
        sendGridApi: ""
      repo:
        user: kubernetes
        name: kubernetes


Setup the class GhTrack
----------------
To begin with you need to create an instance of the class GhTrack.
Like stated above, you can profile a file as configuration values or
providing the necessary params during the class object creation or
you can create without any params and keep the default values the application is providing.

.. code-block:: python

    >>> g = GhTrack()
    >>> g = GhTrack(file_name="/absolute/path/to/the/config/file")
    >>> g = GhTrack(token="github token", email="email to received email", user="repo owner", repo="public repo")

Set the age of the pulls request
------------------------
By default pulls requests are not older than 7 days.
.. code-block:: python

    >>> g.setAge(0)
    # That means the pulls requests will return only today created pulls

Get repo full information
----------------

.. code-block:: python

    >>> repo = g.getRepo()
    >>> repo["name"]
    'kubernetes'
    >> repo["full_name"]
    'kubernetes/kubernetes'


Get the pull requests of the repo
----------------------

.. code-block:: python

    >>> pulls = g.getPulls()
    # if there are pulls the len will return the number of pulls
    >>> len(pulls)
    30

Get pulls request by status open or closed
------------------------

.. code-block:: python

    >>> pulls = g.getPullsByStatus(status="open")
    # if there are pulls the len will return the number of pulls
    >>> pulls[0]["state"]
    'open'

Send Email Or Print on the Console
-------------------------------
Here you can decide to print the html summary of the pulls request or to send to your configurable email.
If the send grid api key is not set, you will not be able to send emails.
If the send grid api key is invalid, you will see an exception on the screen.

.. code-block:: python

    >>> summary = g.sendEmailOrPrintConsole(emailNotConsole=False)
    >>> summary
    # output the html format of the summary.

