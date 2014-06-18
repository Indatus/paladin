Paladin — v0.6.0
================

Android Dependency Manager for libraries that aren't packaged as .jar or
.aar — Paladin fells your dependencies like boss.

If you have any feedback, don't hesitate to reach out to me on Twitter
[@jonathonstaff](https://twitter.com/jonathonstaff). I'm still actively
developing this, and I understand there are some limitations.

Overview
========

Paladin is designed to assist Android developers who use dependencies in
their projects which aren't packaged as .jar or .aar on `Maven
Central <http://search.maven.org/>`__. This is strictly for developers
using Android Studio and Gradle. Before adding a library using Paladin,
I highly recommend searching the Maven Central repositories (check out
`Gradle, please <http://gradleplease.appspot.com/>`__), since this will
often provide the best means of incorporating an external library.

That being said, uploading a library to Maven Central is no walk in the
park, so developers frequently forgo the process altogether and simply
host a public repo with their source code. The `Facebook SDK for
Android <https://github.com/facebook/facebook-android-sdk>`__ for
example, (shame on you Facebook, you're more than capable!) isn't
available on Maven Central, which forces developers to clone down and
manually import the library.

Paladin works to do this for you, quite similar to
`CocoaPods <http://cocoapods.org/>`__ for Objective-C development. An
``/armory`` folder is created in the root directory of your project and
all Paladin libraries are stored there.

Installation
============

Run:

::

    $ pip install paladin

or download the source and run:

::

    $ python setup.py install

Usage
=====

Paladin needs orders before he can carry them out. Commands can be run
with either a ``-v, --verbose`` flag or ``-q, --quiet`` flag to change
the level of output printed in the command line.

Create ``orders``
-----------------

Create a json file at the root of your project titled ``orders``

::

    $ vim orders

with the following format:

::

    {
      "dependencies": [
        {
          "name": "Android-SmoothSeekBar",
          "url": "https://github.com/Indatus/Android-SmoothSeekBar.git"
        },
        {
          "name": "Android-SwipeControl",
          "url": "https://github.com/Indatus/Android-SwipeControl.git"
        }
      ]
    }

Required attributes:

-  ``"url"`` (The url to a git repo containing the dependency)

Future attributes:

-  ``"commit"``
-  ``"tag"``
-  ``"branch"``

If you do not specifiy ``"name"`` in the orders, Paladin will do so for
you.

Installing Dependencies
-----------------------

::

    $ paladin install

You should see the progess displayed in your shell window. Once this has
completed, open Android Studio and **sync** your Gradle project.

Removing Libraries
------------------

You can remove libraries by simply removing that dependency from the
``orders`` and re-running:

::

    $ paladin install

If you wish to remove all dependencies installed by Paladin, run:

::

    $ paladin removeall

Developed By
============

`Jonathon Staff <http://jonathonstaff.com>`__

License
=======

::

      Copyright 2014 Jonathon Staff

      Licensed under the Apache License, Version 2.0 (the "License");
      you may not use this file except in compliance with the License.
      You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
      See the License for the specific language governing permissions and
      limitations under the License.

