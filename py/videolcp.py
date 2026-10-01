import re
import requests


def find_m3u8_in_source(page_url):
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
          ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
      ),
      'Referer': 'https://www.stream4free.tv/',
  }

  try:
    # timeout eklemek, sitenin yanıt vermediği durumlarda kodun sonsuza kadar donmasını engeller
    response = requests.get(page_url, headers=headers, timeout=10)

    # DİKKAT: raise_for_status() kaldırıldı.
    # Böylece 403 gelse bile kod hata fırlatıp durmaz, içeriği okumaya çalışır.

    html_content = response.text

    # .m3u8 uzantılı linkleri yakalamak için Regex kalıbı
    pattern = r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*'
    matches = re.findall(pattern, html_content)

    if matches:
      return list(set(matches))

  except requests.exceptions.RequestException as e:
    # Ağ tabanlı tüm hataları burada yakalayıp sessizce geçebilir veya yazdırabilirsiniz
    print(f'Uyarı: İstek sırasında bir sorun oluştu ama devam ediliyor: {e}')

  return []


target_url = 'https://www.stream4free.tv/public-senat'
links = find_m3u8_in_source(target_url)

if links:
  print('#EXTM3U')
  print('#EXT-X-VERSION:3')
  for link in links:
    print(link)
else:
  print('Kaynak kodunda m3u8 bulunamadı veya erişilemedi.')
