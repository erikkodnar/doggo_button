# doggo_button

## Setup scripts

### Bash
- Make setup.sh executable
  - `chmod +x setup.sh`
- `./setup.sh`

### PowerShell

- **UNSUPPORTED** (TODO)
- Make sure that the execution policy allows running scripts. This can be adjusted by running Set-ExecutionPolicy RemoteSigned or a similar command in an elevated (administrator) PowerShell session.
- `./setup.ps1`

## install
- `cd server`
- `python3 -m venv venv`
- `pip install -r requirements.txt`

## Run server
- `python doggo_server.py`

## Build
- `python build.py`

## Run test client
- `python main.py`


## Server

- Uses a TTS module to speak a given socket message (temporary, socket will send in IDs, the server will map the IDs to the correct string)
