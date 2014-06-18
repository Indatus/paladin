"""Provides entry point main()."""

import sys
import os
import json
import shutil
from .dependency import Dependency
from .project import Project
from .bcolors import bcolors
from .action import Action

# Verbosity levels
v_lvl = 1
v_quiet = -1
v_normal = 0
v_verbose = 1

def main():
    if validate_arguments() == Action.INSTALL:
        print_paladin_header()
        project = load_project(os.getcwd())
        data = load_orders()

        remove_old_dependencies(project)
        add_dependencies(project, data)
        pass
    elif validate_arguments() == Action.REMOVEALL:
        print_paladin_header()
        remove_all_dependencies()
    elif validate_arguments() == Action.VERSION:
        print bcolors.HEADER + "Paladin - v0.6.0\n" + bcolors.ENDC
        sys.exit()
    else:
        print_paladin_header()
        print validate_arguments()
        sys.exit("Aborting...")


#  __  __       _         __  __      _   _               _
# |  \/  | __ _(_)_ __   |  \/  | ___| |_| |__   ___   __| |___
# | |\/| |/ _` | | '_ \  | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|
# | |  | | (_| | | | | | | |  | |  __/ |_| | | | (_) | (_| \__ \
# |_|  |_|\__,_|_|_| |_| |_|  |_|\___|\__|_| |_|\___/ \__,_|___/

def print_paladin_header():
    print bcolors.HEADER
    print "    Paladin fells your dependencies like a boss."
    print "-----------------------------------------------------\n"
    print bcolors.ENDC


def validate_arguments():
    global v_lvl
    action = bcolors.FAIL + "Please enter a valid argument." + bcolors.ENDC

    if len(sys.argv) == 2 and ('-V' in sys.argv or '--version' in sys.argv):
        return Action.VERSION

    for arg in sys.argv:
        if 'paladin' in arg:
            pass
        elif arg == '-q' or arg == '--quiet':
            v_lvl = v_quiet
        elif arg == '-v' or arg == '--verbose':
            v_lvl = v_verbose
        elif arg == 'install':
            action = Action.INSTALL
        elif arg == 'removeall':
            action = Action.REMOVEALL
        else:
            return bcolors.WARNING + "Unknown argument: " + arg + bcolors.ENDC

    return action


def load_project(root):
    project = Project()
    project.main_dir = locate_main_app(root)

    for line in open(os.path.join(root, project.main_dir, 'build.gradle'), 'r'):
        if 'com.android.tools.build:gradle:' in line:
            project.gradle_version = line

        if 'compileSdkVersion' in line:
            project.compile_sdk_version = line

        if 'buildToolsVersion' in line:
            project.built_tools_version = line

        if 'minSdkVersion' in line:
            project.min_sdk_version = line

        if 'targetSdkVersion' in line:
            project.target_sdk_version = line

    return project


def load_orders():
    try:
        json_data = open('orders')
    except IOError:
        print bcolors.FAIL + "No orders provided.  Aborting..." + bcolors.ENDC
        sys.exit('No orders provided. Aborting...')

    data = json.load(json_data)
    json_data.close()
    return data['dependencies']


def remove_old_dependencies(project):
    if not v_lvl == v_quiet:
        print "Removing old dependencies..."

    # Remove /armory directory
    if os.path.exists(os.path.join(project.root, 'armory')):
        shutil.rmtree(os.path.join(project.root, 'armory'))

    os.mkdir('armory')

    # Remove instances from app/build.gradle
    os.chdir(os.path.join(project.root, project.main_dir))
    with open('build.gradle', 'r') as f:
        data = f.readlines()

    for line in data[:]:
        if ':armory' in line:
            if not v_lvl == v_quiet:
                print bcolors.WARNING + "Removing " + line + bcolors.ENDC

            data.remove(line)

    with open('build.gradle', 'w') as f:
        f.writelines(data)

    # Remove instances from settings.gradle
    os.chdir(project.root)
    with open('settings.gradle', 'r') as f:
        data = f.readlines()

    for line in data[:]:
        if ':armory' in line:
            if not v_lvl == v_quiet:
                print bcolors.WARNING + "Removing " + line + bcolors.ENDC

            data.remove(line)

    with open('settings.gradle', 'w') as f:
        f.writelines(data)


def add_dependencies(project, data):
    success_count = 0
    for d in data:
        if d['url']:
            if 'name' in d:
                name = d['name']
            else:
                name = dependency_name(d['url'])

            dep = Dependency(name, d['url'])

            if 'branch' in d:
                dep.branch = d['branch']
            if 'tag' in d:
                dep.tag = d['tag']
            if 'commit' in d:
                dep.commit = d['commit']

            if add_dependency(project, dep):
                success_count += 1
        else:
            print bcolors.FAIL
            print "You must specify a url for each dependency in the orders."
            print bcolors.ENDC

    if success_count < len(data):
        color = bcolors.WARNING
    else:
        color = bcolors.OKGREEN
    print color + "\n------------------------"
    print "Paladin finished: "
    print success_count, " of ", len(data), " dependencies added successfully."
    print bcolors.ENDC


def remove_all_dependencies():
    if not v_lvl == v_quiet:
        print "Removing all dependencies..."

    project = load_project(os.getcwd())

    if os.path.exists(os.path.join(project.root, 'armory')):
        shutil.rmtree(os.path.join(project.root, 'armory'))

    os.remove(os.path.join(project.root, 'orders'))

    # Remove instances from app/build.gradle
    os.chdir(os.path.join(project.root, project.main_dir))
    with open('build.gradle', 'r') as f:
        data = f.readlines()

    for line in data[:]:
        if ':armory' in line:
            if not v_lvl == v_quiet:
                print bcolors.WARNING + "Removing " + line + bcolors.ENDC

            data.remove(line)

    with open('build.gradle', 'w') as f:
        f.writelines(data)

    # Remove instances from settings.gradle
    os.chdir(project.root)
    with open('settings.gradle', 'r') as f:
        data = f.readlines()

    for line in data[:]:
        if ':armory' in line:
            if not v_lvl == v_quiet:
                print bcolors.WARNING + "Removing " + line + bcolors.ENDC

            data.remove(line)

    with open('settings.gradle', 'w') as f:
        f.writelines(data)


#     _       _     _   ____                            _
#    / \   __| | __| | |  _ \  ___ _ __   ___ _ __   __| | ___ _ __   ___ _   _
#   / _ \ / _` |/ _` | | | | |/ _ \ '_ \ / _ \ '_ \ / _` |/ _ \ '_ \ / __| | | |
#  / ___ \ (_| | (_| | | |_| |  __/ |_) |  __/ | | | (_| |  __/ | | | (__| |_| |
# /_/   \_\__,_|\__,_| |____/ \___| .__/ \___|_| |_|\__,_|\___|_| |_|\___|\__, |
#                                 |_|                                     |___/

def add_dependency(project, dep):
    if not v_lvl == v_quiet:
        print "\nAdding " + dep.name + " to project..."
        print "--------------------------------"

    clone_repo(project, dep)
    top_dir = locate_top_build_dir(project, dep)
    check_for_existing_dep(project, dep)

    if not v_lvl == v_quiet:
        print "Moving " + dep.name + " to /armory..."

    mv_cmd = 'mv ' + top_dir + ' ' + escaped_path(os.path.join(project.root, 'armory', dep.name))
    if v_lvl == v_verbose:
        print "Executing: " + mv_cmd

    os.system(mv_cmd)

    delete_repo(project)

    if not is_library_plugin(os.path.join(project.root, 'armory', dep.name, 'build.gradle')):
        dep = convert_to_library(project, dep)

    insert_into_build_gradle(project, dep)
    insert_into_settings_gradle(project, dep)

    if not update_dep_for_project(project, dep):
        return

    if not v_lvl == v_quiet:
        print bcolors.OKBLUE + dep.name + " was added successfully!" + bcolors.ENDC
        print "-------------------------"

    return True


def clone_repo(project, dep):
    os.chdir(project.root)
    if not os.path.exists(os.path.join(project.root, 'clonedRepos')):
        try:
            os.mkdir('clonedRepos')
        except OSError:
            print bcolors.FAIL + "Error creating 'clonedRepos' directory." + bcolors.ENDC
    os.chdir('clonedRepos')

    if not v_lvl == v_quiet:
        print "Cloning " + dep.name + "..."

    if not v_lvl == v_verbose:
        os.system('git clone -q ' + dep.url)
    else:
        os.system('git clone ' + dep.url)


def locate_top_build_dir(project, dep):
    for dirname, dirnames, filenames in os.walk(os.path.join(project.root, 'clonedRepos')):
        for filename in filenames:
            if filename == 'build.gradle':
                with open(os.path.join(dirname, 'build.gradle'), 'r') as f:
                    data = f.readlines()

                if len(data) > 1:
                    return escaped_path(dirname)

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

    print bcolors.FAIL + "No build.gradle file found for library " + dep.name + bcolors.ENDC
    sys.exit("No build.gradle file found for library " + dep.name)


def check_for_existing_dep(project, dep):
    if os.path.exists(os.path.join(project.root, 'armory', dep.name)):
        if not v_lvl == v_quiet:
            print dep.name + " already exists. Removing the existing version before moving in the new one."

        shutil.rmtree(os.path.join(project.root, 'armory', dep.name))


def delete_repo(project):
    if not v_lvl == v_quiet:
        print "Deleting the cloned repo..."

    shutil.rmtree(os.path.join(project.root, 'clonedRepos'))


def is_library_plugin(filepath):
    for line in open(filepath, 'r'):
        if 'android-library' in line:
            return True

    return False


def convert_to_library(project, dep):
    if not v_lvl == v_quiet:
        print "Converting " + dep.name + " to a proper library..."

    with open(os.path.join(project.root, 'armory', dep.name, 'build.gradle'), 'r') as f:
        original = f.readlines()

    lib_dir = locate_library_dir(
            project, os.path.join(project.root, 'armory', dep.name))
    if not lib_dir:
        if not v_lvl == v_quiet:
            print bcolors.FAIL + "Skipping installation of " + dep.name + "..." + bcolors.ENDC

        return

    with open(os.path.join(lib_dir, 'build.gradle'), 'r') as f:
        data = f.readlines()

    for line in original[::-1]:
        if '// Top-level' not in line:
            data.insert(0, line)

    with open(os.path.join(lib_dir, 'build.gradle'), 'w') as f:
        f.writelines(data)

    # Delete top-level build.gradle and settings.gradle
    os.system('rm ' + os.path.join(
        project.root, 'armory', dep.name, 'build.gradle'))
    if os.path.exists(os.path.join(project.root, 'armory', dep.name, 'settings.gradle')):
        os.system('rm ' + os.path.join(
            project.root, 'armory', dep.name, 'settings.gradle'))

        dep.path = lib_dir.replace('/build.gradle', '')
    dep.extended_name = dep.path.replace(os.path.join(project.root, 'armory'), '')
    dep.extended_name = dep.extended_name.lstrip('/')

    if v_lvl == v_verbose:
        print "dep.extended_name: " + dep.extended_name

    return dep


def locate_library_dir(project, top_dir):
    for dirname, dirnames, filenames in os.walk(top_dir):
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
                if is_library_plugin(os.path.join(dirname, filename)):
                    return escaped_path(dirname)

    if not v_lvl == v_quiet:
        print bcolors.FAIL + "No library found." + bcolors.ENDC


def insert_into_build_gradle(project, dep):
    if not v_lvl == v_quiet:
        print "Inserting " + dep.name + " into build.gradle..."

    with open(os.path.join(project.root, project.main_dir, 'build.gradle'), 'r') as f:
        data = f.readlines()

    lib_str = "':armory:" + dep.extended_name + "'"
    for line in data:
        if lib_str in line:
            if not v_lvl == v_quiet:
                print dep.name + " has already been added to build.gradle. Skipping this step..."

    # We need to be certain that the 'dependencies' portion of build.gradle is as the top level
    # and not contained within another, such as buildscript {..}
    count = 0
    for line in data:
        if count == 0 and line.lstrip().startswith('dependencies') and line.rstrip().endswith('{'):
            data.insert(data.index(line) + 1,
                    "\tcompile project(':armory:" + dep.extended_name + "')\n")
            if '{' in line:
                count += 1
        if '}' in line:
            count -= 1

    with open(os.path.join(project.root, project.main_dir, 'build.gradle'), 'w') as f:
        f.writelines(data)


def insert_into_settings_gradle(project, dep):
    if not v_lvl == v_quiet:
        print "Inserting " + dep.name + " into settings.gradle..."

    with open(os.path.join(project.root, 'settings.gradle'), 'r') as f:
        data = f.readlines()

    for line in data:
        if dep.extended_name in line:
            if not v_lvl == v_quiet:
                print dep.name + " has already been added to settings.gradle. Skipping this step..."

            return

    data.insert(len(data), "\ninclude ':armory:" + dep.extended_name + "'")
    with open(os.path.join(project.root, 'settings.gradle'), 'w') as f:
        f.writelines(data)


def update_dep_for_project(project, dep):
    if not v_lvl == v_quiet:
        print "Updating " + dep.name + " build.gradle to match the project build.gradle..."

    with open(os.path.join(project.root, 'armory', dep.extended_name, 'build.gradle')) as f:
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
                print bcolors.WARNING + "This library requires a minSdkVersion of ", libv, ". Please update your project to match, or remove this library from 'orders'." + bcolors.ENDC
                # TODO: offer to do this for them
                return

    with open(os.path.join(project.root, 'armory', dep.extended_name, 'build.gradle'), 'w') as f:
        f.writelines(data)

    return True

#  _   _      _                   __  __      _   _               _
# | | | | ___| |_ __   ___ _ __  |  \/  | ___| |_| |__   ___   __| |___
# | |_| |/ _ \ | '_ \ / _ \ '__| | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|
# |  _  |  __/ | |_) |  __/ |    | |  | |  __/ |_| | | | (_) | (_| \__ \
# |_| |_|\___|_| .__/ \___|_|    |_|  |_|\___|\__|_| |_|\___/ \__,_|___/
#              |_|


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
                    if v_lvl == v_verbose:
                        print os.path.join(dirname, filename) + " is the main app"

                    return escaped_path(dirname.lstrip('./'))

    print bcolors.FAIL + "Main app not found." + bcolors.ENDC
    sys.exit('No build.gradle file found for the main application.')


def is_main_app(filepath):
    for line in open(filepath, 'r'):
        if "'android'" in line.rstrip():
            return True

    return False


def dependency_name(url):
    name = url.rstrip('.git')
    name = name[::-1]
    name = name[0: name.find('/')]
    return name[::-1]

def escaped_path(path):
    return path.replace(' ', '\ ')
