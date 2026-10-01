from playwright.sync_api import sync_playwright


def find_m3u8_with_browser(page_url):
  found_links = set()

  with sync_playwright() as p:
    # Tarayıcırı başlatıyoruz (headless=False yaparsanız tarayıcının ekranda açıldığını görürsünüz)
    browser = p.chromium.launch(headless=True)

    # Gerçek bir kullanıcı gibi görünmek için context ve user-agent ayarlıyoruz
    context = browser.new_context(
        user_agent=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
            ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ),
        referer='https://www.stream4free.tv/',
    )

    page = context.new_page()

    # Ağ trafiğini (Network requests) dinle: Sayfa yüklenirken geçen her isteği yakala
    def handle_request(request):
      if '.m3u8' in request.url:
        found_links.add(request.url)

    page.on('request', handle_request)

    try:
      print(
          'Siteye bağlanılıyor, 403 engeli aşılıyor ve ekranın gelmesi'
          ' bekleniyor...'
      )
      # Sayfaya git ve ağ trafiğinin oturması için oynatıcının yüklenmesini bekle
      page.goto(page_url, timeout=60000, wait_until='networkidle')

      # Oynatıcı biraz geç tetikleniyorsa ekstra birkaç saniye (örn: 5 saniye) bekleyebiliriz
      page.wait_for_timeout(5000)

    except Exception as e:
      print(f'Yüklenme sırasında hata oluştu ama devam ediliyor: {e}')

    browser.close()

  return list(found_links)


target_url = 'https://www.stream4free.tv/public-senat'
links = find_m3u8_with_browser(target_url)

if links:
  print('\nBulunan M3U8 Bağlantıları:')
  print('#EXTM3U')
  print('#EXT-X-VERSION:3')
  for link in links:
    print(link)
else:
  print(
      'Yine de m3u8 bulunamadı. Site çok katı bir Cloudflare korumasına sahip'
      ' olabilir.'
  )
