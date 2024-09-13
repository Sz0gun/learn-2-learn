import platform
import psutil
import subprocess  # Dodajemy ten import


def get_system_info():
    # Informacje o systemie operacyjnym
    system_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'Python Version': platform.python_version(),
    }

    # Informacje o pamięci
    memory_info = psutil.virtual_memory()
    system_info['Total Memory (GB)'] = round(memory_info.total / (1024 ** 3), 2)
    system_info['Available Memory (GB)'] = round(memory_info.available / (1024 ** 3), 2)

    # Informacje o dyskach
    disk_info = psutil.disk_partitions()
    system_info['Disk Info'] = []
    for partition in disk_info:
        usage = psutil.disk_usage(partition.mountpoint)
        system_info['Disk Info'].append({
            'Device': partition.device,
            'Mountpoint': partition.mountpoint,
            'Total Space (GB)': round(usage.total / (1024 ** 3), 2),
            'Used Space (GB)': round(usage.used / (1024 ** 3), 2),
            'Free Space (GB)': round(usage.free / (1024 ** 3), 2),
            'Filesystem Type': partition.fstype,
        })

    # Informacje o procesorze
    system_info['CPU Cores'] = psutil.cpu_count(logical=False)  # Fizyczne rdzenie
    system_info['Logical CPUs'] = psutil.cpu_count(logical=True)  # Logiczne procesory
    system_info['CPU Frequency (MHz)'] = psutil.cpu_freq().current

    # Informacje o sieci
    network_info = psutil.net_if_addrs()
    system_info['Network Interfaces'] = []
    for interface, addrs in network_info.items():
        for addr in addrs:
            if addr.family == 2:  # Adresy IPv4
                system_info['Network Interfaces'].append({
                    'Interface': interface,
                    'IP Address': addr.address,
                    'Netmask': addr.netmask,
                    'Broadcast IP': addr.broadcast
                })

    # Informacje o karcie graficznej
    try:
        gpu_info = subprocess.check_output("lspci | grep -i 'vga\|3d\|2d'", shell=True).decode('utf-8').strip()
        system_info['GPU Info'] = gpu_info
    except subprocess.CalledProcessError:
        system_info['GPU Info'] = 'Unable to retrieve GPU information.'

    return system_info

if __name__ == "__main__":
    info = get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")
