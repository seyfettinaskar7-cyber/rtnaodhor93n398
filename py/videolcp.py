import re
import requests


def find_m3u8_in_source(page_url):
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like'
          ' Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
      ),
      'Referer': page_url,
  }

  try:
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    # .m3u8 uzantılı linkleri yakalamak için Regex kalıbı
    pattern = r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*'
    matches = re.findall(pattern, html_content)

    if matches:
      # Tekrarlanan linkleri temizle
      return list(set(matches))
  except Exception as e:
    print(f'Bağlantı hatası: {e}')

  return []


target_url = 'https://www.stream4free.tv/public-senat'
links = find_m3u8_in_source(target_url)

if links:
  print('#EXTM3U')
  print('#EXT-X-VERSION:3')
  print('#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720')
  for link in links:
    print(link)
else:
  print('Kaynak kodunda m3u8 bulunamadı (Oynatıcı JS ile dinamik yükleniyor olabilir).')
