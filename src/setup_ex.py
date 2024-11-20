'''from subprocess import run, PIPE, CalledProcessError
from os import environ, makedirs
from os.path import join, isdir
from platform import system

import requests

class UnsupportedSystem: ...
class MinecraftFolderNotFound: ...

def tryCmd(*cmd):
    """
        Runs a CLI command, and returns True if it exited without errors
    """

    try:
        run(cmd, check=True, stdout=PIPE, stderr=PIPE)
        return True
    except CalledProcessError: return False

def getJava_Linux():
    """
        Downloads and installs Java on Linux
    """

    if tryCmd("pacman", "--version"): # Arch
        print("`pacman` found. Arch-based distro detected. Installing Java...")
        run("sudo", "pacman", "-S", "jdk-openjdk")
    else:
        print("`pacman` not found.")
        if tryCmd("apt", "--version"): # Debian
            print("`apt` found. Debian-based distro detected. Installing Java...")
            run("sudo", "apt", "install", "default-jdk")
        else: # Other
            print("`apt` not found.")
            raise UnsupportedSystem("Linux distro not compatible")

def getJava_Windows():
    """
        Downloads and installs Java on Windows
    """

    print("Installing Java...")
    
    url = "https://github.com/AdoptOpenJDK/openjdk16-binaries/releases/latest/download/OpenJDK16U-jdk_x64_windows_openj9_16.0.1_9_openj9-0.26.0.msi"
    filename = "OpenJDKInstaller.jar"

    msi = join(environ["USERPROFILE"], filename)
    
    response = requests.get(url)

    if response.status_code == 200:
        with open(msi, 'wb') as f:
            f.write(response.content)
        print("Fetched Java installer. Follow the program's instructions to install Java.")
        run(msi)
    else:
        raise ConnectionError("Unable to download JDK installer")

def javaSetup():
    """
        Downloads and installs Java if not installed
    """

    if not tryCmd("java", "-version"):
        print("Java not installed.")

    while not tryCmd("java", "-version"):
        match system().lower():
            case "linux": # Linux
                print("Linux detected.")
                getJava_Linux()
            case "windows": # Windows
                print("Windows detected.")
                getJava_Windows()
            case _: # Other
                raise UnsupportedSystem("Operating System not compatible")

    print("Java installed.")

def mcuSetup():
    """
        Downloads and installs MCUpdater, then returns the jar's location
    """

    print("Downloading mcupdater.jar...")

    url = "https://files.mcupdater.com/MCU-CLI-latest.jar"
    filename = "mcupdater.jar"

    path = (
        join(environ["HOME"], ".local", "bin") if system().lower()=="linux"
        else join(environ["USERPROFILE"], "bin")
    )

    if not isdir(path):
        print("Created bin folder.")
        makedirs(path)

    jar = join(path, filename)

    response = requests.get(url)

    if response.status_code == 200:
        with open(jar, 'wb') as f:
            f.write(response.content)
        print("mcupdater.jar installed.")
        return jar
    else:
        raise ConnectionError("Unable to download MCUpdater CLI")

def findMC():
    """
        Finds and returns the Minecraft folder path
    """

    paths = (
        [
            join(environ["HOME"], ".minecraft"),
            join(environ["HOME"], ".local", "share", "PrismLauncher", "instances", "Forge 1.20.1", "minecraft"),
        ]
        if system().lower()=="linux" else
        [
            join(enviton["APPDATA"], ".minecraft"),
        ]
    )

    for path in paths:
        if isdir(path):
            print("Minecraft fodler found.")
            return path

    raise MinecraftFolderNotFound("Minecraft folder was not found.") # TODO: ask folder from user


def makeRCU(jar, mcPath):
    """
        Sets up the `rcu` command
    """

    rcuFolder = (
        join("/", "usr", "local", "bin") if system().lower()=="linux"
        else join(environ["USERPROFILE"], "AppData", "Local", "Microsoft", "WindowsApps")
    )

    rcu = join("rcu" if system().lower()=="linux" else "rcu.bat")

    rcuCmd = f"java -jar '{jar}' --pack https://github.com/Malasaur/RetardsCreative/releases/latest/download/serverPack.xml --path '{mcPath}' --server \"Retards Creative\""
    if system().lower()=="linux":
        rcuCmd = "#!/bin/bash\n"+rcuCmd

    open(rcu, 'w').write(rcuCmd)

    if system().lower()=="linux":
        run(["sudo", "mv", "rcu", rcuFolder])
        run(["sudo", "chmod", "+x", join(rcuFolder, rcu)])

    print("Created RCU command at %s." % rcuFolder)

def setup():
    javaSetup()
    jar = mcuSetup()
    mcPath = findMC()

    makeRCU(jar, mcPath)

__name__ == "__main__" and setup()
'''

