# Mudarris Akademiyasi — Telegram Bot

`/start` bosilganda foydalanuvchiga salomlashuv xabari va Mini App'ni ochuvchi tugma yuboradi. Production'da **webhook** rejimida, Render.com Web Service sifatida ishlaydi.

## Loyiha strukturasi

```
bot/
├── bot.py             # kirish nuqtasi (webhook/polling)
├── config.py          # environment variable'larni o'qish
├── handlers.py        # /start + global xatolik ushlagichi + ro'yxatdan o'tkazish
├── keyboards.py        # inline klaviatura (Mini App tugmasi)
├── logger.py          # logging sozlamalari
├── requirements.txt
├── runtime.txt
├── render.yaml
└── .env.example
```

Barcha fayllar bitta papkada, papkasiz (flat) — GitHub veb-saytidan "Add file → Upload files" orqali hammasini bir vaqtda tanlab yuklash mumkin, papka sudrashning hojati yo'q.

## Polling vs Webhook — nima uchun webhook tanlandi

- **Polling** (`run_polling`) — botning o'zi Telegram serveridan doimiy so'rab turadi. Sodda, lekin doim tirik jarayon talab qiladi va HTTP port tinglamaydi. Render'ning **Web Service** turi esa `$PORT`da HTTP so'rovlarni kutishni talab qiladi — polling buni bajarmagani uchun Render uni "port band emas" deb hisoblab, xizmatni nosog'lom deb belgilaydi va qayta-qayta restart qilishi mumkin edi (aynan shu ilgari kelgan xatolarning sababi).
- **Webhook** (`run_webhook`) — Telegram yangiliklarni to'g'ridan-to'g'ri bizning HTTP endpoint'imizga yuboradi, bot esa `$PORT`da tinglaydi. Bu Render Web Service modeliga to'liq mos keladi.
- Bu loyihada: agar `WEBHOOK_URL` (yoki Render avtomatik beradigan `RENDER_EXTERNAL_URL`) mavjud bo'lsa — **webhook**, aks holda (masalan sizning kompyuteringizda lokal test qilsangiz) — **polling**'ga avtomatik o'tadi. Alohida kod yozish shart emas, `bot.py` shuni o'zi hal qiladi.

## Render.com'ga deploy qilish — bosqichma-bosqich

1. **Repo tayyorlash.** Bu `bot/` papkani (yoki butun loyihani) GitHub'ga push qiling.
2. Render Dashboard > **New +** > **Web Service** > repo'ni tanlang.
3. Agar `bot/` boshqa fayllar (frontend, admin panel) bilan bitta repoda bo'lsa, **Root Directory** maydoniga `bot` deb yozing — Render shu papka ichidan `requirements.txt`/`bot.py`ni qidiradi.
4. **Environment**: `Python 3` tanlang (yoki `render.yaml` orqali avtomatik aniqlanadi — pastga qarang).
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python bot.py`
7. **Environment Variables** (Render Dashboard > Environment):
   | Kalit | Qiymat |
   |---|---|
   | `BOT_TOKEN` | @BotFather'dan olingan haqiqiy token |
   | `SITE_URL` | `https://mudarris-akadmeiyasi.netlify.app/` (ixtiyoriy, default shu) |
   | `WEBHOOK_SECRET` | ixtiyoriy, tasodifiy uzun matn (masalan `openssl rand -hex 32`) — qo'shimcha xavfsizlik |

   `PORT` va `RENDER_EXTERNAL_URL`'ni **qo'shmang** — Render buni avtomatik o'zi beradi.
8. **Deploy** tugmasini bosing. Loglarda `"Webhook rejimida ishga tushmoqda: https://...onrender.com/<BOT_TOKEN>"` degan qatorni ko'rsangiz — bot ishga tushgan.
9. Telegram'da botga `/start` yuboring — javob kelishi kerak.

### `render.yaml` orqali (tavsiya etiladi)

Agar Render Dashboard'da "Blueprint" (Infrastructure as Code) usulini tanlasangiz, ushbu papkadagi `render.yaml` fayl orqali servis avtomatik sozlanadi — faqat `BOT_TOKEN` va (ixtiyoriy) `WEBHOOK_SECRET` qiymatlarini birinchi deploy paytida qo'lda kiritishingiz kerak bo'ladi (`sync: false` bo'lgani uchun Render sizdan so'raydi).

## Xavfsizlik eslatmalari

- `BOT_TOKEN` endi hech qanday faylda saqlanmaydi — faqat Environment Variable orqali beriladi. Eski `token.txt` olib tashlandi.
- `.env.example`ni nusxalab `.env` qilib, unga haqiqiy qiymatlarni yozsangiz ham, `.env` faylni Git'ga qo'shmang.
- `WEBHOOK_SECRET` o'rnatilsa, Telegram yuborgan har bir so'rov `X-Telegram-Bot-Api-Secret-Token` header orqali tekshiriladi — soxta so'rovlarning oldini oladi.
