"""
# Retards Creative Server Updates

## Server

```bash
cd $MODSOURCE
git add -A
git commit -m $COMMITMSG
git push
java -jar $FASTPACK --baseURL $REMOTE --path . --mc $MCVER --out $XML
# Upload XML to release

cd /home/malasaur/Desktop/RetardsCreative
git add -A
git commit -m $COMMITMSG
git push
java -jar /usr/bin/fastpack.jar 
    --baseURL https://github.com/Malasaur/RetardsCreativeMods/raw/refs/heads/master 
    --path . --mc 1.20.1 --out /home/malasaur/Desktop/serverPack.xml
# Create release with XML
```

## Client

```bash
java -jar $MCUCLI --pack $REMOTEXML --path $MINECRAFT --server $SERVER

java -jar /usr/bin/mcupdater.jar 
    --pack https://github.com/Malasaur/RetardsCreativeMods/releases/latest/download/serverMods.xml
    --path $MINECRAFT 
    --server "Retards Creative"
```
"""

"""
mcUpdater = "/usr/bin/mcupdater.jar"
repo = "https://github.com/Malasaur/RetardsCreativeMods"
xml = "serverMods.xml"
mcPath = "/home/malasaur/.local/share/PrismLauncher/instances/Forge 1.20.1/minecraft"
server = "Retards Creative"

remoteXml = repo+"/releases/latest/download/"+xml

def updateMods():
    ...
"""

from subprocess import run, PIPE, CalledProcessError
from platform import system

def javaInstalled():
    try:
        subprocess.run(["java", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except CalledProcessError: return False

def installJava():
    system = system().lower()

    match system:
        case "linux":
            print("Installing Java...")
        case "windows":
            print("Installing Java...")
        case _:
            print("ERROR: OS not supported")


"""
https://github.com/AdoptOpenJDK/openjdk16-binaries/releases/latest/download/OpenJDK16U-jdk_x64_windows_openj9_16.0.1_9_openj9-0.26.0.msi
import os
import platform

def install_java():
    system = platform.system().lower()
    
    if system == 'linux':
        # Try using yay or apt (you could extend this for other package managers like pacman, dnf)
        print("Java not found. Attempting to install...")
        if os.system("yay -S jdk11-openjdk") != 0:  # Change the package name as per your requirements
            print("Java installation failed. Try installing it manually.")
    elif system == 'darwin':  # macOS
        print("Java not found. Attempting to install with brew...")
        if os.system("brew install openjdk@11") != 0:
            print("Java installation failed. Try installing it manually.")
    elif system == 'windows':
        print("Java not found. Please install Java from the official website: https://adoptopenjdk.net/ or Oracle's JDK.")
    else:
        print("Unsupported OS detected. Please install Java manually.")

import subprocess
import sys

def check_java_installed():
    try:
        # Check for Java version
        subprocess.run(["java", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
"""
