R2-D2 — v0.3.7
====================================

Android Dependency Manager for libraries that aren't packaged as .jar or .aar.

If you have any feedback, don't hesitate to reach out to me on Twitter [@jonathonstaff](https://twitter.com/jonathonstaff).  I'm still actively developing this, and I understand there are some limitations - this is still in alpha.

![r2d2 running in Terminal](r2d2_screenshot.png)


Overview
========

R2-D2 is designed to assist Android developers who use dependencies in their projects which aren't packaged as .jar or .aar on [Maven Central](http://search.maven.org/).  This is strictly for developers using Android Studio and Gradle.  Before adding a library using R2-D2, I highly recommend searching the Maven Central repositories (check out [Gradle, please](http://gradleplease.appspot.com/)), since this will often provide the best means of incorporating an external library.

That being said, uploading a library to Maven Central is no walk in the park, so developers frequently forgo the process altogether and simply host a public repo with their source code.  The [Facebook SDK for Android](https://github.com/facebook/facebook-android-sdk) for example, (shame on you Facebook, you're more than capable!) isn't available on Maven Central, which forces developers to clone down and manually import the library.

R2-D2 works to do this for you, quite similar to [CocoaPods](http://cocoapods.org/) for Objective-C development.  A `/toolbox` folder is created in the root directory of your project and all R2-D2 libraries are stored there.


Installation
============

Run:

	$ pip install r2d2

or download the source and run:

	$ python setup.py install


Usage
=====

Currently `r2d2 install` is the only command that works.  Others will be added in time.


Create a `schematic`
-----------------

Create a json file at the root of your project titled `schematic` with the following format:

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

- `"url"`

Future attributes:

- `"commit"`
- `"tag"`
- `"branch"`

If you do not specifiy `"name"` in the schematic, R2-D2 will do so for you.


Installing Dependencies
-----------------------

	$ r2d2 install


You should see the progess displayed in your shell window.  Once this has completed, open Android Studio and **sync** your Gradle project.


Removing Libraries
------------------

You can remove libraries by simply removing that dependency from the `schematic` and re-running:

	$ r2d2 install


Developed By
============

[Jonathon Staff](http://jonathonstaff.com)


License
=======

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
