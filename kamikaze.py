#Encoding UTF-8

"""
Sartek SİHA
Enes Kılıçaslan
"""
#Kamikaze Algoritması

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Örnek bağlantı dizesi ile SİHA'ya bağlanıldı
siha = connect('127.0.0.1:14550', wait_ready=True)


def takeoff(hedef_irtifa):
    # Kalkış algoritması

    siha.mode = VehicleMode("GUIDED")
    siha.armed = True

    while not siha.armed:
        print("SİHA'nın hazır olması bekleniyor...")
        time.sleep(1)

    siha.simple_takeoff(hedef_irtifa)
    while True:
        print("Anlık İrtifa: ", siha.location.global_relative_frame.alt)
        if siha.location.global_relative_frame.alt >= hedef_irtifa * 0.95:
            print("Hedef irtifaya ulaşıldı.")
            time.sleep(1)


def diving(qr_konum, hedef_irtifa, minimum_irtifa):

    # Dalış Algoritması

    print("Hedeflenen konuma doğru dalışa geçiliyor")
    point = LocationGlobalRelative(qr_konum['lat'],
                                   qr_konum['lon'],
                                   hedef_irtifa)
    siha.simple_goto(point)

    while True:
        anlık_irtifa = siha.location.global_relative_frame.alt
        print("Dalış yapılıyor... Anlık irtifa: ", anlık_irtifa)

        if anlık_irtifa <= minimum_irtifa:
            print("minimum irtifanın altına inildi dalış iptal")
            return False

        time.sleep(1)

def pas_gecme(hedef_irtifa):

    #Pas geçme algoritması

    print(f"{hedef_irtifa}m irtifaya  yükseleniyor")
    point = LocationGlobalRelative(siha.location.global_frame.lat,
                                   siha.location.global_frame.lon,
                                   hedef_irtifa)
    siha.simple_goto(point)

    while siha.location.global_relative_frame.alt < hedef_irtifa * 0.95:
        print("Yükseliyor... anlık irtifa: ", siha.location.global_relative_frame.alt)
        time.sleep(1)

    print("Pas geçme irtifasına ulaşıldı")

# SİHA kalkışa geçiyor
takeoff(100) # 100 metre yüksekliğe çıkış

# Dalış ve pas geçme işlemleri
qr_konum = {'lat': 39.75083, 'lon': 30.48456}  # Örnek konum (Esogü kütüphane)
hedef_irtifa = 100  # Hedef irtifa (100 metre)
minimum_irtifa = 35  # Minimum izin verilen irtifa (35 metre)
tekrar_deneme = 3  # Tekrar deneme sayısı

for attempt in range(tekrar_deneme):
    print(f"Attempt {attempt + 1}")
    if diving(qr_konum, hedef_irtifa, minimum_irtifa):
        break
    pas_gecme(100) # Pas geçip tekrar 100 merteye çıkış

# İniş
print("İniş yapılıyor...")
siha.mode = VehicleMode("LAND")

# Aracla bağlantıyı bırakma
siha.close()