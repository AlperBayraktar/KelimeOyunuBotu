
## The Domates - Pomodoro Botu

Bu bot Kodluyoruz JR. Discord Botu Yapma Hackathon'u için yapılmıştır.




## Yapımcılar

- [Alper Bayraktar](https://www.github.com/AlperBayraktar)
- [Eren Ege](https://www.github.com/CipioMi)
## Proje İçin Kullanılan Teknolojiler


## Python ve Modülleri
- Discord  - Bot Komutları yaratıldı
- OS       - klasör ismi alındı
- asyncio  - async sleep() işlemi için kullanıldı
- requests - json-server'a istem yapılmak için kullanıldı
- json     - json-server'a yapılan istemin body'si için kullanıldı
- datetime - tarih ve saat alındı.
- PIL      - görsel işlemler için kullanıldı
- io       - buffer yaratmak için kullanıldı

## React ve json-server
- react - dinamik arayüz için kullanıldı
- json-server - aşırı büyük veriler olmadığı için veritabanı yerine fake api kullanıldı

## Botun Kullanımı

- Bot dosyasının olduğu dizine gelin
- TOKEN.txt dosyasına bot token'nını girin
- Not: PomodoroBot no-admin.py'ı tek başına çalıştırabilirsiniz. Fakat admin paneli ile çalıştırmak istiyorsanız json-server'ı çalıştırdıktan sonra PomodoroBot-admin.py'ı çalıştırmalısınız.
- Not 2: Bot dosyasını terminal üzerinden çalıştırmak daha iyi olacaktır.

## Admin Panelinin Kullanımı

- admin-panel dizinine gelin

- ardından json-server'i çalıştırın

```bash
npm run server
```

- Daha sonra react uygulamasını çalıştırın, panel açılacaktır
- Not: react ve json-server'i indirmiş olmanız gerekmektedir
