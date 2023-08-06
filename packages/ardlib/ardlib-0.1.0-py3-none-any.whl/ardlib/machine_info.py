import platform

def get_machine_info() -> dict:
    machine = platform.machine()
    node = platform.node()
    system = platform.system()
    processor = platform.processor()
    arch = platform.architecture()
    return {
        "machine": machine,
        "node": node,
        "system": system,
        "processor": processor,
        "arch": arch
    }