"""Provides entry point main()."""

import sys
import os
import json
import shutil
from .dependency import Dependency
from .project import Project
from .bcolors import bcolors

def main():
	print_adm_header()

	if len(sys.argv) < 2 or sys.argv[1] != 'install':
		print bcolors.FAIL + "Please enter a valid argument to install your dependencies (i.e. 'adm install')." + bcolors.ENDC
		print str(sys.argv)
		return

	project = load_project(os.getcwd())
	if not project.main_dir:
		print bcolors.FAIL + "No build.gradle file found for the main application. Aborting dependency installation." + bcolors.ENC
		return

	try:
		json_data = open('adm_file')
	except IOError:
		print bcolors.FAIL + "No adm_file provided. Aborting." + bcolors.ENDC
		return

	data = json.load(json_data)
	data = data['dependencies']
	json_data.close()

	remove_old_dependencies(project)

	success_count = 0
	for d in data:
		dep = Dependency(d['name'], d['url'])

		if 'branch' in d:
			dep.branch = d['branch']
		if 'tag' in d:
			dep.tag = d['tag']
		if 'commit' in d:
			dep.commit

		if add_dependency(dep, project):
			success_count += 1

	if success_count < len(data):
		color = bcolors.WARNING
	else:
		color = bcolors.OKGREEN
	print color + "\n-----------------------"
	print "adm finished:"
	print success_count, " of ", len(data), " dependencies added successfully."
	print bcolors.ENDC


def remove_old_dependencies(project):
	print "Removing old dependencies..."

	# Remove /deps directory
	if os.path.exists(os.path.join(project.root, 'deps')):
		shutil.rmtree(os.path.join(project.root, 'deps'))

	os.mkdir('deps')

	# Remove instances from app/build.gradle
	os.chdir(os.path.join(project.root, project.main_dir))
	with open('build.gradle', 'r') as f:
		data = f.readlines()

	for line in data[:]:
		if ':deps' in line:
			print bcolors.WARNING + "Removing " + line + bcolors.ENDC
			data.remove(line)

	with open('build.gradle', 'w') as f:
		f.writelines(data)

	# Remove instances from settings.gradle
	os.chdir(project.root)
	with open('settings.gradle', 'r') as f:
		data = f.readlines()

	for line in data[:]:
		if ':deps' in line:
			print bcolors.WARNING + "Removing " + line + bcolors.ENDC
			data.remove(line)

	with open('settings.gradle', 'w') as f:
		f.writelines(data)

def add_dependency(dep, project):
	print "\nAdding dependency " + dep.name + "\n-----------------------"
	
	clone_repo(dep, project)
	move_library(dep, project)

	lib_dir = locate_library(project)

	if lib_dir:
		print "Moving " + dep.name + " to /deps..."
		os.system('mv ' + lib_dir + ' ' + os.path.join(project.root, 'deps', dep.name))
	else:
		print "Canceling this dependency..."
		return

	delete_repo(project)
	insert_into_build_gradle(dep, project)
	insert_into_settings_gradle(dep, project)

	if not update_dependency_for_project(dep, project):
		return

	print bcolors.OKBLUE + dep.name + " was added successfully!" + bcolors.ENDC
	print "-----------------------"
	return True

def clone_repo(dep, project):
	os.chdir(project.root)
	if not os.path.exists(os.path.join(project.root, 'clonedRepos')):
		try:
			os.mkdir('clonedRepos')
		except OSError:
			print bcolors.FAIL + "Error creating 'clonedRepos' directory" + bcolors.ENDC
	os.chdir('clonedRepos')

	print "Cloning " + dep.name + "..."
	os.system('git clone ' + dep.url)

def move_library(dep, project):
	os.chdir(project.root)

	if os.path.exists(os.path.join(project.root, 'deps', dep.name)):
		print dep.name + " already exists. Removing the existing copy before moving in the new one."
		shutil.rmtree(os.path.join(project.root, 'deps', dep.name))	

def delete_repo(project):
	print "Deleting the cloned repo..."
	os.chdir(project.root)
	os.system('rm -rf clonedRepos')

def insert_into_build_gradle(dep, project):
	print "Inserting " + dep.name + " into the build.gradle file..."
	os.chdir(os.path.join(project.root, project.main_dir))

	with open('build.gradle', 'r') as f:
		data = f.readlines()

	lib_str = "':deps:" + dep.name + "'"
	for line in data:
		if lib_str in line:
			print dep.name + " is already included in build.gradle. Skipping this step."
			return

	# We need to be certain that the 'dependencies' portion of the build.gradle file is at the top-level
	# and not contained within another, such as buildscript {..}		
	count = 0
	for line in data:
		if count == 0 and line.lstrip().startswith('dependencies') and line.rstrip().endswith('{'):
			print "Inserting '" + dep.name + "' at index: ", data.index(line) + 1
			data.insert(data.index(line) + 1, "\tcompile project(':deps:" + dep.name + "')\n")
		if '{' in line:
			count += 1
		if '}' in line:
			count -= 1

	with open('build.gradle', 'w') as f:
		f.writelines(data)

def insert_into_settings_gradle(dep, project):
	print "Inserting " + dep.name + " into the settings.gradle file..."
	os.chdir(project.root)

	with open('settings.gradle', 'r') as f:
		data = f.readlines()

	for line in data:
		if dep.name in line:
			print "Project " + dep.name + " has already been added to settings.gradle"
			return

	data.insert(len(data), "\ninclude ':deps:" + dep.name + "'")
	with open('settings.gradle', 'w') as f:
		f.writelines(data)

def locate_library(project):
	print "Locating the library..."

	os.chdir(os.path.join(project.root, 'clonedRepos'))

	for dirname, dirnames, filenames in os.walk('.'):
	    for filename in filenames:
	    	if filename == 'build.gradle':
	        	if is_library_plugin(os.path.join(dirname, filename)):
	        		return dirname

	    if '.git' in dirnames:
	        dirnames.remove('.git')

	print "Library not found."

def locate_main_app(root):
	os.chdir(root)
	for dirname, dirnames, filenames in os.walk('.'):
		if '.git' in dirnames:
			dirnames.remove('.git')

		if 'gradle' in dirnames:
			dirnames.remove('gradle')

		if '.gradle' in dirnames:
			dirnames.remove('.gradle')	

		if '.idea' in dirnames:
			dirnames.remove('.idea')

		if 'build' in dirnames:
			dirnames.remove('build')

		for filename in filenames:
			if filename == 'build.gradle':
				if is_main_app(os.path.join(dirname, filename)):
					# print os.path.join(dirname, filename) + " is the main app"
					return dirname.lstrip('./')

	print "Main app not found."

def is_library_plugin(filepath):
	for line in open(filepath, 'r'):
		if 'android-library' in line.rstrip():
			return True

	return False

def is_main_app(filepath):
	for line in open(filepath, 'r'):
		if "'android'" in line.rstrip():
			return True

	return False

def load_project(root):
	project = Project()
	project.main_dir = locate_main_app(root)

	for line in open(os.path.join(root, project.main_dir, 'build.gradle'), 'r'):
		if 'com.android.tools.build:gradle:' in line:
			project.gradle_version = line

		if 'compileSdkVersion' in line:
			project.compile_sdk_version = line

		if 'buildToolsVersion' in line:
			project.build_tools_version = line

		if 'minSdkVersion' in line:
			project.min_sdk_version = line

		if 'targetSdkVersion' in line:
			project.target_sdk_version = line

	return project

def update_dependency_for_project(dep, project):
	print "Updating " + dep.name + " build.gradle to match the project build.gradle..."

	os.chdir(os.path.join(project.root, 'deps', dep.name))

	with open('build.gradle', 'r') as f:
		data = f.readlines()

	for line in data:
		if 'com.android.tools.build:gradle:' in line and project.gradle_version is not None:
			data[data.index(line)] = project.gradle_version

		if 'compileSdkVersion' in line and project.compile_sdk_version is not None:
			data[data.index(line)] = project.compile_sdk_version

		if 'buildToolsVersion' in line and project.build_tools_version is not None:
			data[data.index(line)] = project.build_tools_version

		if 'targetSdkVersion' in line and project.target_sdk_version is not None:
			data[data.index(line)] = project.target_sdk_version

		if 'minSdkVersion' in line and project.min_sdk_version is not None:
			libv = line.rstrip()[-2:]
			projv = project.min_sdk_version.rstrip()[-2:]

			if libv > projv:
				print bcolors.WARNING + "This library requires a minSdkVersion of ", libv, ". Please update your project to match, or remove this library from 'adm_file'." + bcolors.ENDC
				# TODO: offer to do this for them
				return


	with open('build.gradle', 'w') as f:
		f.writelines(data)

	return True

def print_adm_header():
	print bcolors.HEADER
	print "            __                 "
	print "           /\ \                "
	print "    __     \_\ \    ___ ___    "
	print "  /'__`\   /'_` \ /' __` __`\  "
	print " /\ \L\.\_/\ \L\ \/\ \/\ \/\ \ "
	print " \ \__/.\_\ \___,_\ \_\ \_\ \_\ "
	print "  \/__/\/_/\/__,_ /\/_/\/_/\/_/\n"
	print "   Android Dependency Manager\n"
	print "-------------------------------\n"
	print bcolors.ENDC







