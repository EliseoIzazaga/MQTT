#Eliseo Izazaga
# to test subprocess calls correctly in the RPI system

import subprocess

x = subprocess.run(['/home/ubuntu/connectedhomeip/out/standalone/chip-tool onoff on'], shell=True)
print(x)
print(x.args)
print(x.returncode)
print(x.stdout)
print(x.stderr)
