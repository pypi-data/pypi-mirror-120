<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [BILL - Bert's Interactive Lesson Loader](#bill---berts-interactive-lesson-loader)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Building the development instance](#building-the-development-instance)
- [Configuration File](#configuration-file)
- [WebTerminal](#webterminal)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

BILL - Bert's Interactive Lesson Loader
===================

<a name="top"></a>
<a name="overview"></a>
# Overview

Think [Katacoda](https://www.katacoda.com/), but instead of a website with learning examples, 
you have a desktop app that creates hands-on lessons from markdown-formatted documents, 
complete with a web terminal.

I used the boilerplate from this repo 
[r0x0r/pywebview-react-boilerplate](https://github.com/r0x0r/pywebview-react-boilerplate) 
to create the basis for the app.

As such, the UI is written in [ReactJS](https://reactjs.org/), with 
the [pywebview](https://github.com/r0x0r/pywebview) python package 
rendering the HTML as a GUI.

This is a similar approach to what 
[Electron](https://www.electronjs.org/) accomplishes, 
but with a much smaller resulting file.

<a name="features"></a>
# Features

* Define your lessons catalog in a YAML-formatted configuration file, e.g. [bill.config.yaml.example](bill.config.yaml.example)
* [Lessons](#Lessons) are Markdown-formatted files
  1. First rendered as [jinja](https://jinja.palletsprojects.com/en/3.0.x/) templates
  1. Then rendered as HTML<br />
* Web-based terminals via [xtermjs](https://github.com/xtermjs/xterm.js/) component<br />
  See section on [WebTerminal](#WebTerminal)

# Installation
  
* From pypi.org: `pip install bertdotbill`
* From locally-cloned repo: `pip install bertdotbill`
* From locally-cloned repo, in development mode: `pip install -e .`
* From git `pip install git+http://www.github.com/berttejeda/bert.bill.git`

<a name="building-the-app"></a>
# Building the app

* Install and configure prerequisites:
  * Python 3.7+
  * Nodejs (tested with version 16.5.0)
* Install yarn: `npm install yarn`
* Install modules: `yarn install`
* Install python prerequisites: `pip install -r requirements.txt`
* Build: `yarn build`
* Launch the desktop app: `yarn start:gui:dev`<br />
  Under the hood, this recompiles the HTML and launches [bertdotbill/app.py](bertdotbill/app.py)

Notes for users on Windows 10 x64:
  * If you want to be able to open the Developer Console from the Desktop App, you'll need to install<br />
    [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
  * Ensure you configure Nodejs as per https://github.com/nodejs/node-gyp#on-windows:
      * Install the current version of Python from the Microsoft Store package.
      * Install tools and configuration manually:
      * Install Visual C++ Build Environment: Visual Studio Build Tools (using "Visual C++ build tools" workload) or Visual Studio Community (using the "Desktop development with C++" workload)
      * Launch cmd, npm config set msvs_version 2017
      * If the above steps didn't work for you, please visit Microsoft's Node.js Guidelines for Windows for additional tips.  

<a name="building-the-installer"></a>
# Building the installer

You can run `yarn build:installer` to generate the installer.

Under the hood, the above command calls the [setup.sh](setup.sh) script to do the heavy lifting.

Once the process completes, the installer file should be located in the *dist* folder.

Platform-specific notes:

- Windows: The above script calls [InnoSetup](https://jrsoftware.org/isinfo.php) against the InnoSetup script [setup.iss](setup.iss)<br />
  As such, you'll need to install [InnoSetup](https://jrsoftware.org/isinfo.php) for this to work,<br />
  Important: The [setup.sh](setup.sh) script is written in bash, so it'll only 
  work if you're on a posix emulation environment, e.g. [Cygwin](https://www.cygwin.com/), 
  [git-bash](https://git-scm.com/downloads), etc
- Linux: Not yet implemented
- OSX: Not yet implemented

[Back to Top](#top)
<a name="developing-the-app"></a>
# Developing the app

If you want to make changes to the UI, you'll need to launch the 
web instance with `yarn start:web:dev`.

Your changes to UI components will re-render the HTML on-the-fly.

<a name="configuration-file"></a>
# Configuration File

The configuration file is read by the **desktop** app , and is a YAML-formatted file.

As mentioned above, a sample configuration file is provided: [bill.config.yaml.example](bill.config.yaml.example)

The desktop app will attempt to find the config file in the following locations:
- Under ~/bill.config.yaml
- Adjacent to the app, i.e. in the same folder as the app's script
- Under ~/.bill/bill.config.yaml
- Under /etc/bill.config.yaml

Do review the comments in the sample file, as these explain how the sections
are interpreted/handled by the UI.

## Storing credentials - OS Keyring

The config file allows you to specify credentials in the following jinja format: 

```yaml
auth:
  global:
    username: "{{ session.get_credential('mycredential').username }}"
    password: "{{ session.get_credential('mycredential').password }}"
```

Under the hood, we are calling a function (get_credential) from the session object.

This function utilizes the python [keyring](https://pypi.org/project/keyring/) library to retrieve
credentials stored in the OS keyring.

### Windows

In the case of Windows, the function interacts with the 
[Windows Credential Manager](https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0)
to retrieve the referenced _Generic_ Credentials

As such, the example above will expect a Generic Windows Credential named 'mycredential',
with a value filled in for username and password.

<a name="Lessons"></a>
# Lessons

As mentioned above, lessons are Markdown-formatted files interpreted as [jinja](https://jinja.palletsprojects.com/en/3.0.x/) templates.

You can define a lesson catalog in the [configuration file](bill.config.yaml.example#L33-L57).

If these files are stored in a password-protected web location, 
you'll need to specify credentials in the auth.global section of the config file.

Per-lesson credentials are not yet implemented, but will be in a future version.

## Jinja Templating

To add to the templating goodies provided by the Jinja library,
I've exposed the OS Environment via the _environment_ key of the _sessions_ object.

This means you should be able to reference any OS-level environment variable in your
lesson content, e.g. 

```markdown
# Overview

Hello {{ session['environment']['USERNAME'] }}, welcome to Lesson 1
```

<a name="WebTerminal"></a>
# WebTerminal

Every lesson rendered through the app includes a web-based terminal emulator component
that allows for practicing the lesson material.

These web terminals are embedded in the user interface, 
available at its footer and as a slide-in from the right (click Utils to reveal).

As mentioned before, the underlying technology for these web terminals is [xterm.js](https://github.com/xtermjs/xterm.js/).

As such, the xterm.js component requires a websocket to a bash process.

By [default](bertdotbill/defaults.py), the bert.bill desktop app will attempt to connect to a local instance of the websocket via _http://127.0.0.1:5000/_.

To get this running locally, you can invoke the docker image I've prepared via: `docker run --rm -it --name aiohttp -p 5000:5000 berttejeda/aiohttp-websocket-bash:1.0.0`

The command above will automatically start the websocket 
and bash process on the container and expose the websocket on your host port 5000.

Feel free to adjust the docker run command to your need, e.g. change the port mapping, but 
be aware that the desktop app's [configuration file](bill.config.yaml.example) must be adjusted to reflect any changes to the way
the websocket is accessed.