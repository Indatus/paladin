import os


class Project:

    'Model for containing data about an Android Project'

    def __init__(self):
        self.main_dir = None
        # classpath 'com.android.tools.build:gradle:0.9.+'
        self.gradle_version = None
        self.compile_sdk_version = None  # compileSdkVersion 19
        self.build_tools_version = None  # buildToolsVersion '19.0.1'
        self.min_sdk_version = None		# minSdkVersion 14
        self.target_sdk_version = None  # targetSdkVerion 19
        self.root = os.getcwd()

    def __repr__(self):
        return '{ main_dir: %s, gradle_version: %s, compile_sdk_version: %s, build_tools_version: %s, min_sdk_version: %s, target_sdk_version: %s, root: %s }' % (self.main_dir, self.gradle_version, self. compile_sdk_version, self.build_tools_version, self.min_sdk_version, self.target_sdk_version, self.root)
