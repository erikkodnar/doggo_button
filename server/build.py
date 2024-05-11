import subprocess

def build_executable():
  # Execute the PyInstaller command
  result = subprocess.run("pyinstaller --onefile --name doggo_server doggo_server.py", shell=True)
  if result.returncode == 0:
      print("Executable has been created successfully!")
  else:
      print("Failed to create the executable.")

if __name__ == "__main__":
    build_executable()
