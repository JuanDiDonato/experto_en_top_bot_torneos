import threading
import time
def daemon():
    print("Lanzado")
    time.sleep(2)
    print('Deteniendo')
d = threading.Thread(target=daemon, name='Daemon')
d.daemon = True
d.start()