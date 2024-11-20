import os, platform, subprocess, requests, traceback

from pathlib import Path

class UnsupportedSystem(Exception): ...

def runCmd(*cmd):
    """
    Runs a shell command and returns True if successful, False otherwise.
    """

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def installJava_Linux():
    """
    Installs Java on Linux using the system's package manager.
    """

    if runCmd("pacman", "--version"):
        print("Arch-based distro detected. Installing Java with pacman...")
        subprocess.run(["sudo", "pacman", "-S", "jdk-openjdk", "--noconfirm"])
    elif runCmd("apt", "--version"):
        print("Debian-based distro detected. Installing Java with apt...")
        subprocess.run(["sudo", "apt", "install", "default-jdk", "-y"])
    else:
        raise UnsupportedSystem("Unsupported Linux distribution. Install Java manually.")

def installJava_Windows():
    """
    Downloads and installs Java on Windows.
    """

    print("Downloading and installing Java for Windows...")

    url = "https://github.com/AdoptOpenJDK/openjdk16-binaries/releases/latest/download/OpenJDK16U-jdk_x64_windows_openj9_16.0.1_9_openj9-0.26.0.msi"
    installer_path = Path(os.environ["USERPROFILE"], "Downloads", "OpenJDKInstaller.msi")

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(installer_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Running Java installer. Follow the installation steps.")
        subprocess.run(["msiexec", "/i", str(installer_path)])
    else:
        raise ConnectionError("Failed to download Java installer.")


def installJava():
    """
    Ensures Java is installed. Installs it if not present.
    """

    if runCmd("java", "-version"):
        print("Java is already installed.")
        return

    os_name = platform.system().lower()
    if os_name == "linux":
        installJava_Linux()
    elif os_name == "windows":
        installJava_Windows()
    else:
        raise UnsupportedSystem(f"{os_name.capitalize()} is not supported.")

    if not runCmd("java", "-version"):
        raise RuntimeError("Java installation failed. Please install it manually.")

def downloadMcu():
    """
    Downloads the MCUpdater JAR file and saves it to a shared bin directory.
    """
    
    print("Downloading MCUpdater CLI...")

    url = "https://files.mcupdater.com/MCU-CLI-latest.jar"
    bin_dir = Path.home() / (".local/bin" if platform.system().lower() == "linux" else "bin")
    bin_dir.mkdir(parents=True, exist_ok=True)
    jar_path = bin_dir / "mcupdater.jar"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('Content-Length', 0))
        chunk_size = 1024

        with open(jar_path, "wb") as file:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    progress = (downloaded_size / total_size) * 100 if total_size else 0
                    print(f"\rDownloading: {progress:.2f}% ({downloaded_size}/{total_size} bytes)", end="")
        print()

        print(f"MCUpdater downloaded to {jar_path}.")
        return jar_path
    else:
        raise ConnectionError("Failed to download MCUpdater CLI.")


def findMC():
    """
    Locates the Minecraft installation folder.
    """

    os_name = platform.system().lower()
    paths = [
        Path.home() / ".minecraft",
        Path.home() / ".local/share/PrismLauncher/instances/Forge 1.20.1/minecraft",
    ] if os_name == "linux" else [
        Path(os.environ.get("APPDATA", ""), ".minecraft"),
    ]

    for path in paths:
        if path.is_dir():
            print(f"Minecraft folder found at {path}.")
            return path

    path = ""
    while not path or not os.path.isdir(path):
        print("Minecraft folder not found.")
        path = input("Please manually enter your Minecraft path: ")
    
    return path

def createRCU(jar_path, mc_folder):
    """
    Creates the `rcu` or `rcu.bat` command for launching MCUpdater.
    """
    
    os_name = platform.system().lower()
    bin_dir = Path("/usr/local/bin") if os_name == "linux" else Path(os.environ["USERPROFILE"], "AppData/Local/Microsoft/WindowsApps")
    bin_dir.mkdir(parents=True, exist_ok=True)
    rcu_path = bin_dir / ("rcu" if os_name == "linux" else "rcu.bat")

    command = (
        f"java -jar \"{jar_path}\" --pack https://github.com/Malasaur/RetardsCreative/releases/latest/download/serverPack.xml "
        f"--path \"{mc_folder}\" --server \"Retards Creative\""
    )
    if os_name == "linux":
        command = f"#!/bin/bash\n{command}"

    with open(rcu_path, "w") as file:
        file.write(command)

    if os_name == "linux":
        subprocess.run(["sudo", "chmod", "+x", str(rcu_path)])

    print(f"RCU command created at {rcu_path}. Add it to your PATH if needed.")


def main():
    """
    Main setup function.
    """
    installJava()
    jar_path = downloadMcu()
    mc_folder = findMC()
    createRCU(jar_path, mc_folder)

if __name__ == "__main__":

    try:
        main()
    except:
        print(traceback.format_exc())
        print("Please copy the above error and send it to the developer before closing the program.")
    
    input("Press Enter to exit")
