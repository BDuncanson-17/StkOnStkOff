import platform

def get_system_info():
    info = {
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "node": platform.node(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "system": platform.system(),
        "release": platform.release(),
    }
    return info

# Usage:
info = get_system_info()
for key, value in info.items():
    print(f"{key}: {value}")