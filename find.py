import subprocess

program_name = "keylogger.py"
result = subprocess.run(
    ["where", program_name],
    capture_output=True,
    text=True
)
path=result.stdout.strip()
print(path)
