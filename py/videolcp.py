from playwright.sync_api import sync_playwright


def find_m3u8_with_browser(page_url):
  found_links = set()

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # DÜZELTME: referer parametresi extra_http_headers içine taşındı
    context = browser.new_context(
        user_agent=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
            ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ),
        extra_http_headers={'Referer': 'https://www.stream4free.tv/'},
    )

    page = context.new_page()

    def handle_request(request):
      if '.m3u8' in request.url:
        found_links.add(request.url)

    page.on('request', handle_request)

    try:
      page.goto(page_url, timeout=60000, wait_until='networkidle')
      page.wait_for_timeout(5000)
    except Exception as e:
      print(f'Yüklenme sırasında hata oluştu ama devam ediliyor: {e}')

    browser.close()

  return list(found_links)


target_url = 'https://www.stream4free.tv/public-senat'
links = find_m3u8_with_browser(target_url)

if links:
  print('#EXTM3U')
  print('#EXT-X-VERSION:3')
  print('#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720')
  for link in links:
    print(link)
else:
  print('Kaynak kodunda m3u8 bulunamadı.')
