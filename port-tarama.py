import threading
from queue import Queue
import time

# Hedef bilgilerini al
target = input("Taramak istediğiniz IP veya Domain: ")
print(f"\n{target} taranıyor... Bu işlem seçilen port sayısına göre vakit alabilir.")

# Thread güvenliği için kilit ve port kuyruğu
print_lock = threading.Lock()
queue = Queue()

def portscan(port):
    """Port tarama işlemini gerçekleştiren fonksiyon"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1) # 1 saniye bekleme süresi (İnternet taramaları için ideal)
    try:
        con = s.connect_ex((target, port))
        with print_lock:
            if con == 0:
                print(f"[+] Port {port:5} : AÇIK")
        s.close()
    except:
        pass

def threader():
    """Kuyruktaki işleri işçilere (thread) dağıtan fonksiyon"""
    while True:
        worker = queue.get()
        portscan(worker)
        queue.task_done()

# Kaç adet eş zamanlı çalışan (thread) olacağını belirle
# 100-200 arası idealdir, çok yüksek yapmak hedef sistem tarafından engellenmenize sebep olabilir.
for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True # Ana program kapandığında threadleri de kapat
    t.start()

start_time = time.time()

# Hangi port aralığını tarayacağımızı seçelim (Örn: 1-1000 arası)
for port in range(1, 1001):
    queue.put(port)

# Tüm işlerin bitmesini bekle
queue.join()

end_time = time.time()
print(f"\nTarama tamamlandı. Geçen süre: {round(end_time - start_time, 2)} saniye.")
