# CoinRadar Bot

CoinRadar Bot, 100’den fazla kripto para biriminin teknik göstergelerini ve makine öğrenimi tabanlı analizini kullanarak **en yüksek potansiyel getiriye sahip coinleri** otomatik olarak tespit eder ve Telegram üzerinden öneri olarak sunar.

## Özellikler

- 🔍 Otomatik coin listesi ve tarihsel veri çekme
- 📊 Gelişmiş teknik analiz ve göstergeler (RSI, MACD, Bollinger Bands, vb.)
- 🤖 Makine öğrenimi ile kazanç olasılığı hesaplama (XGBoost modeli)
- 📈 Günlük kâr, başarı oranı ve performans raporları
- 📩 Telegram bot entegrasyonu ile anlık yatırım önerileri

## Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

2. `bot.py` dosyasında, aşağıdaki satıra **kendi Telegram Bot Token'ınızı** girin:
    ```python
    TOKEN = "KENDİ_TELEGRAM_BOT_TOKENINIZ"
    ```
    > Güvenlik nedeniyle GitHub’a token eklenmemiştir!

3. İlk veri setini oluşturmak için sırasıyla:
    ```bash
    python src/data_loader.py      # Coin listesini ve fiyat verilerini indirir
    python src/feature_builder.py  # Teknik göstergelerden ML veri seti üretir
    python src/trainer.py          # Makine öğrenimi modelini eğitir
    python src/main.py             # Analiz ve öneri üretir
    python bot.py                  # Telegram botunu başlatır
    ```

## Notlar

- **Token, .env gibi gizli dosyalar ve büyük veri dosyaları repoya dahil edilmemiştir.**
- Proje dosyası içeriği örnek amaçlıdır, finansal yatırım tavsiyesi değildir.
- Geri bildirim ve katkılarınız için pull request gönderebilirsiniz.

## Lisans

MIT License

---

> 📬 **İletişim:** [GitHub](https://github.com/Ahmetmelihdenizz) üzerinden ulaşabilirsin.





# coinradar_bot
