Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import socket
... import sys
... 
... # Kullanıcıdan girdi al
... target = input("Taramak istediğiniz IP veya Domain: ")
... 
... print(f"\nTarama başlatıldı: {target}")
... print("-" * 30)
... 
... try:
...     for port in range(1, 65536):
...     
...         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
...         sock.settimeout(0.01) # Çok hızlı geçmesi için süreyi iyice kısalttık
...         
...         result = sock.connect_ex((target, port))
...         
...         if result == 0:
...             # Açık port bulunduğunda satırı temizle ve kalıcı olarak yaz
...             sys.stdout.write(f"\r[+] Port {port}: AÇIK\n")
...             sys.stdout.flush()
...             
...         sock.close()
... 
... except Exception as e:
...     print(f"\nHata oluştu: {e}")
... 
... print("\n" + "-" * 30)
