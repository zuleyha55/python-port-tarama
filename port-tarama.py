import socket
import threading
import subprocess

target_net = input("Ağ adresini girin (Örn: 192.168.1): ")
common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389]
print_lock = threading.Lock()

def scan_ports(ip):
    # Port tarama öncesi host aktif mi diye bak (Ping)
    check = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if check.returncode == 0:
        with print_lock:
            print(f"\n[+] HOST AKTİF: {ip}")
        
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                with print_lock:
                    print(f"    [>] Port {port}: AÇIK")
            sock.close()

threads = []
print(f"\n[*] {target_net}.0/24 ağı taranıyor...")

for i in range(1, 255):
    ip_to_scan = f"{target_net}.{i}"
    t = threading.Thread(target=scan_ports, args=(ip_to_scan,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n[!] Tarama tamamlandı.")
