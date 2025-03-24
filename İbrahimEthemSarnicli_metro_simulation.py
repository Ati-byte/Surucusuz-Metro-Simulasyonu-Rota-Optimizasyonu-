# -*- coding: utf-8 -*-
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int): # (istasyon, süre) tuple'ları
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        kuyruk = deque([(baslangic, [baslangic], 0)])  # (current, path, aktarma_sayisi)
        ziyaret_edildi = {baslangic.idx: 0}
        
        while kuyruk:
            current, path, aktarma = kuyruk.popleft()
            
            if current.idx == hedef.idx:
                return path
            
            for komsu, _ in current.komsular:
                yeni_aktarma = aktarma + (1 if current.hat != komsu.hat else 0)
                
                if komsu.idx not in ziyaret_edildi or yeni_aktarma < ziyaret_edildi.get(komsu.idx, float('inf')):
                    ziyaret_edildi[komsu.idx] = yeni_aktarma
                    kuyruk.append((komsu, path + [komsu], yeni_aktarma))
        
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
    
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
    
        
        def heuristic(current: Istasyon) -> int: # Heuristic: Hedef istasyona olan minimum tahmini süre (örneğin hat değişimi durumu)
            return 0                             # Mesafe bilgileri girilip mesafeye göre sıralama yapmasını da sağlayabiliriz.
    
        heap = []
        heapq.heappush(heap, (0 + heuristic(baslangic), id(baslangic), 0, baslangic, [baslangic]))
    
        cost_so_far = {baslangic.idx: 0}
    
        while heap:
            _, _, current_cost, current, path = heapq.heappop(heap)
        
            if current.idx == hedef.idx:
                return (path, current_cost)
        
            for komsu, sure in current.komsular:
                new_cost = current_cost + sure  
            
                if komsu.idx not in cost_so_far or new_cost < cost_so_far.get(komsu.idx, float('inf')):
                    cost_so_far[komsu.idx] = new_cost
                    priority = new_cost + heuristic(komsu)
                    heapq.heappush(heap, (priority, id(komsu), new_cost, komsu, path + [komsu]))
    
        return None

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")        # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")         # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Yeşil Hat
    metro.istasyon_ekle("Y1", "Çayyolu", "Yeşil Hat")  #Ek test için yeni istasyon
    metro.istasyon_ekle("Y2", "Bahçelievler", "Yeşil Hat") #Ek test için yeni istasyon
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4) # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6) # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8) # Demetevler -> OSB
    
    #Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5) # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3) # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4) # Sıhhiye -> Gar
    
    #Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7) # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9) # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5) # Gar -> Keçiören
    
    #Yeşil Hat bağlantıları
    metro.baglanti_ekle("Y1", "Y2", 5) #Ek test için yeni bağlantı
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Bağlantısız İstasyon (TEST İÇİN)
    metro.istasyon_ekle("X1", "Bağlantısız İstasyon", "Test Hat")
    
    # Testler
    print("\n=== Test Sonuçları ===")
    
    # Senaryo 1: AŞTİ -> OSB
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    print("En az aktarma:", " -> ".join([i.ad for i in rota]))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı ({sure} dk):", " -> ".join([i.ad for i in rota]))
    
    # Senaryo 2: Batıkent -> Keçiören
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    print("En az aktarma:", " -> ".join([i.ad for i in rota]))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı ({sure} dk):", " -> ".join([i.ad for i in rota]))
    
    # Senaryo 3: Keçiören -> AŞTİ
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    print("En az aktarma:", " -> ".join([i.ad for i in rota]))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı ({sure} dk):", " -> ".join([i.ad for i in rota]))
        
    # Senaryo 4: Aynı İstasyondan Aynı İstasyona (AŞTİ -> AŞTİ)
    print("\n4. AŞTİ'den AŞTİ'ye':")
    rota = metro.en_az_aktarma_bul("M1", "M1")
    print(f"En az aktarma: {' -> '.join([i.ad for i in rota]) if rota else 'Bulunamadı'}")
    sonuc = metro.en_hizli_rota_bul("M1", "M1")
    if sonuc:
        print(f"En hızlı ({sonuc[1]} dk): {' -> '.join([i.ad for i in sonuc[0]])}")
        
    # Senaryo 5: Doğrudan Bağlantı (Kızılay -> Ulus)
    print("\n5. Kızılay'dan Ulus'a :")
    rota = metro.en_az_aktarma_bul("K1", "K2")
    print(f"En az aktarma: {' -> '.join([i.ad for i in rota])}")
    sonuc = metro.en_hizli_rota_bul("K1", "K2")
    if sonuc:
        print(f"En hızlı ({sonuc[1]} dk): {' -> '.join([i.ad for i in sonuc[0]])}")

    # Senaryo 6: Çoklu Aktarma (Batıkent -> Gar)
    #Birden fazla aktarma seçeneği olduğunda en hızlıyı seçtiğinden emin olmak.
    print("\n6. Batıkent^den Gar'a :") 
    rota = metro.en_az_aktarma_bul("T1", "T3")
    print(f"En az aktarma: {' -> '.join([i.ad for i in rota])}")
    sonuc = metro.en_hizli_rota_bul("T1", "T3")
    if sonuc:
        print(f"En hızlı ({sonuc[1]} dk): {' -> '.join([i.ad for i in sonuc[0]])}")
        
    # Senaryo 7: Farklı Hatlarda En Hızlı Rota (Çayyolu -> Sıhhiye)
    print("\n7. Çayyolun'dan Sıhhiye'ye:")
    metro.baglanti_ekle("Y2", "M3", 4)  # Bahçelievler -> Sıhhiye
    rota = metro.en_az_aktarma_bul("Y1", "M3")
    print(f"En az aktarma: {' -> '.join([i.ad for i in rota])}")
    sonuc = metro.en_hizli_rota_bul("Y1", "M3")
    if sonuc:
        print(f"En hızlı ({sonuc[1]} dk): {' -> '.join([i.ad for i in sonuc[0]])}")
        
    # Senaryo 8: Büyük Metro Ağı Testi (OSB -> Keçiören)
    # karmaşık ağlarda algoritmanın performansını ölçmek.
    print("\n8. OSB'den Keçiören'e:") 
    rota = metro.en_az_aktarma_bul("K4", "T4")
    print(f"En az aktarma: {' -> '.join([i.ad for i in rota])}")
    sonuc = metro.en_hizli_rota_bul("K4", "T4")
    if sonuc:
        print(f"En hızlı ({sonuc[1]} dk): {' -> '.join([i.ad for i in sonuc[0]])}")    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
