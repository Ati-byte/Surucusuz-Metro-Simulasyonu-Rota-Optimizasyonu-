# Sürücüsüz Metro Simülasyonu Üzerine Yapay Zeka Projesi 🚇


Bu proje, metro istasyonları arasında **en kısa süreli** ve **en az aktarmalı** rotaları bulan bir simülasyon uygulamasıdır. Graf veri yapısı ve optimizasyon algoritmaları kullanılarak yazılmıştır.

---

## Kullanılan Python Kütüphaneleri


- **`collections`** (defaultdict, deque):  
  - Graf yapısını oluşturmak için `defaultdict` ve kuyruk işlemleri için `deque` kullanıldı.
- **`heapq`**:  
  - A* algoritmasında öncelik kuyruğu (priority queue) yönetimi için kullanıldı.
- **`typing`**:  
  -  Kod okunabilirliği artırmak için kullanıldı.

---

## Algoritmaların Çalışma Mantığı

### **BFS (Breadth-First Search) ile En Az Aktarma**  
  
 - Başlangıç istasyonundan başlayarak, tüm komşu istasyonları katman katman dolaşır. Her adımda hat değişimi sayısını en aza indirir.  
  ```python
  kuyruk = deque([(baslangic, [baslangic], 0)])  # (current, path, aktarma_sayisi)
  while kuyruk:
      current, path, aktarma = kuyruk.popleft()
      if hedefe_ulasti: return path
      for komsu in current.komsular:
          yeni_aktarma = aktarma + (1 if hat_degisti else 0)
          kuyruk.append((komsu, path + [komsu], yeni_aktarma))
```
**Neden BFS?**
- En az aktarmayı kesin olarak bulur.
- Karmaşık hesaplamalar gerektirmez.

##  A* Algoritması ile En Hızlı Rota  
- **A***, hedefe en kısa sürede ulaşmak için graf arama algoritmasıdır. Bu projede, her bir istasyonun hedefle aynı hat üzerinde olup olmamasına göre hesaplanan **heuristik fonksiyonu** ile optimizasyon sağlanır. öncelikli olarak hedefe yakın yönlere odaklanır.
  
  ```python
  heap = [(0 + heuristic(baslangic), id(baslangic), 0, baslangic, [baslangic])]
  while heap:
    _, current_cost, current, path = heapq.heappop(heap)
    if current == hedef:
        return (path, current_cost)
    for komsu, sure in current.komsular:
        new_cost = current_cost + sure
        if new_cost < cost_so_far.get(komsu.idx, float('inf')):
            heapq.heappush(heap, (new_cost + heuristic(komsu), new_cost, komsu, path + [komsu]))
   ```
**Neden A***?
- Daha az düğüm dolaşır yani hızlı ve verimlidir.
- Heuristik özelliği sayesinde ilk önce hedefe yakın yönlere bakar.

---
## Örnek Kullanım ve Test Sonuçları
- Proje, şehir içi ulaşım ağlarının modellemesi için bir temel oluşturur. Büyük şehirlerin ulaşım sistemlerine adapte edilebilir ve maksimum verimlilik için geliştirilir.

- Ankarada olan metro istasyonlarıyla örnek

  <img src="https://github.com/Ati-byte/Surucusuz-Metro-Simulasyonu-Rota-Optimizasyonu-/blob/main/Test_sonucu.png">

## Projeyi Geliştirme Fikirleri

1. Gerçek Zamanlı Veri Entegrasyonu

- Şehirlerin gerçek metro verilerini ekleme(şehirlerin açık veri API'larından canlı veri çekme).
- Örnek: `requests` kütüphanesi ile İstanbul Metro verilerini almak.
2. GUI Eklenmesi

- Tkinter veya PyQt ile kullanıcı dostu arayüz tasarımı.
- Kullanıcıların harita üzerinden istasyon seçebilmesi.

3. Mobil Uygulama Entegrasyonu

- Backend oluşturup mobil uygulamaya bağlama.

4. Sesli Asistan Entegrasyonu

 - Google Assistant veya Alexa ekleme.

5. Çoklu Taşıma Modu Desteği

- Otobüs, tramvay gibi diğer ulaşım araçlarını dahil etme.

6. Optimizasyon İyileştirmeleri

- Gerçek zamanlı trafik yoğunluğu faktörünü ekleme(Google haritalardan API ile çekilebilir).
- Trafik yoğunluğu veya kaza durumlarını ekleme (örnek: İstanbul Ulaşım hizmetleri web sitesinde mevcut)

7. Çok Kriterli Optimizasyon

- Maliyet, süre ve konforu dengeli optimize eden Pareto analizi.(En kısa olmasına karşın trafik yopunluğunun konforu azaltacağı durumları göz önünde bulundurma veya en ucuz rotalar.)
  




  
