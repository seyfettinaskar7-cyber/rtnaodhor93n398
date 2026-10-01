import re
import requests


def find_m3u8_in_source(page_url):
  # Daha güncel ve gerçekçi bir masaüstü tarayıcı başlığı
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
          ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
      ),
      'Referer': 'https://www.stream4free.tv/',
      'Accept': (
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
      ),
      'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
  }

  try:
    response = requests.get(page_url, headers=headers, timeout=10)
    response.raise_for_status()
    html_content = response.text

    # .m3u8 uzantılı linkleri yakalamak için Regex kalıbı
    pattern = r'https?://[^\s\'"]+?\.m3u8[^\s\'"]*'
    matches = re.findall(pattern, html_content)

    if matches:
      return list(set(matches))

  except requests.exceptions.HTTPError as err:
    print(f'HTTP Hatası: {err} (Site bot koruması uyguluyor olabilir)')
  except Exception as e:
    print(f'Bağlantı hatası: {e}')

  return []


target_url = 'https://www.stream4free.tv/public-senat'
links = find_m3u8_in_source(target_url)

if links:
  print('#EXTM3U')
  print('#EXT-X-VERSION:3')
  for link in links:
    print(link)
else:
  print('Kaynak kodunda m3u8 bulunamadı.')
