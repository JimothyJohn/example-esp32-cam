# Install PlatformIO

I use the <a href="https://platformio.org/platformio-ide">PlatformIO extension in VS Code</a>, but it's actually quicker to use the command line:

```bash 
# Install PlatformIO
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py)"
```

OPTIONAL (Linux) - I also like to create the alias "platformio" to quickly activate the PlatformIO virtual environment on the command line:

```bash 
# Create alias
echo "alias platformio=\". ~/.platformio/penv/bin/activate\"" >> ~/.bashrc && . ~/.bashrc
# Try it out!
platformio
echo "You should now see: (penv) user@host:~$"
```