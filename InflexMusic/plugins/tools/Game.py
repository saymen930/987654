
from telebot import TeleBot, types
import random
import threading
import time
import os
import datetime
import json
from InflexMusic import app

# Bot start vaxtı
bot_start_time = datetime.datetime.now()
start_message_count = 0

        'group_only': "🛡️ Sahibim bu komandayı yalnız qruplar üçün təyin edib\n✓ Məni qrupa əlavə edib komandanı yoxla",
        'games_stopped': "🔚 Bütün oyunlar dayandırıldı, yeni oyun üçün /game yaz",
        'language_changed': "✅ Dil Azərbaycan dilinə dəyişdirildi",
        'language_menu': "🌍 Dil seçin:",
        'support': "📤 Support",
        'add_group': "➕ Məni Qrupuna Əlavə Et ➕",
        'commands': "📚 Əmrlər",
        'owner': "👤 Sahibim",
        'chat_group': "🌐 Söhbət Qrupumuz",
        'developer': "🧑‍💻 Developer",
        'main_menu': "Ana Menyu 🏡",
        'explain_game': "🗣 İzah Oyunu",
        'word_game': "🔤 Söz Oyunu",
        'guess_game': "🎯 Təxmin Oyunu",
        'riddle_game': "❓ Tapmaca Oyunu",
        'number_game': "🔢 Rəqəm Oyunu",
        'group_bests': "👑 Qrupun Enləri",
        'mole_game': "🦫 Köstəbək Game",
        'truth_dare': "🔥 Doğruluq / Cəsarət",
        'blank_game': "🧩 Boş Xana"
    }
 }
  

# =============== OYUNLARIN VERİLƏRİ ===============

# Söz bazaları
izah_sozleri = ["Telefon", "Qarpız", "Kitab", "Kompyuter", "yumurta", "baki", "oyuncaq", "qapı", "işıq", "Lənkaran", "limon", "çay", "qənd", "şəkər", "ölmək", "morq", "Versiya", "salam", "var", "oyunçu", "oyun", "forma", "əsgər", "saat", "muncuq", "razval", "yağış", "günəş", "samir", "ət", "sümük", "kondisoner", "Mercedes", "bmw", "lada", "YMZ", "ortaq", "bot", "telegram", "whatsapp", "səssiz", "Kəlbəcər", "globus", "Qız", "oğlan", "abort", "həkim", "usta", "xəstəxana", "kitabxana", "məktəb", "şagird", "elcan", "Rahim", "raxa", "Ruhin", "dünya", "global", "combot", "robot", "mexikox", "ürək", "ciyər", "oyuncaq", "televizor", "şkaf", "aybaşı", "regl", "mədəniyyəsiz", "şüvən", "cırnamaq", "fifa", "korna", "Türkiyə", "top", "Instagram", "memoza", "çobansalat", "Tağıyev", "Nağıyev", "xəlilov", "abbasov", "mal", "inək", "qoyun", "daraq", "traktor", "aviator", "əmsal", "sumka", "pul", "aliqarx", "dayday", "ata", "ana", "nənə", "bibi", "kamera", "ətir", "gül", "əsgər", "dost", "qardaş", "dünən", "düşmən", "radio", "qəzet", "mahnı", "küknar", "kobud", "sarımtıl", "poçt"]
soz_oyunu_sozler = ["Telefon", "Qarpız", "Kitab", "Kompyuter", "yumurta", "baki", "oyuncaq", "qapı", "işıq", "Lənkaran", "limon", "çay", "qənd", "şəkər", "ölmək", "morq", "Versiya", "salam", "var", "oyunçu", "oyun", "forma", "əsgər", "saat", "muncuq", "razval", "yağış", "günəş", "samir", "ət", "sümük", "kondisoner", "Mercedes", "bmw", "lada", "YMZ", "ortaq", "bot", "telegram", "whatsapp", "səssiz", "Kəlbəcər", "globus", "Qız", "oğlan", "abort", "həkim", "usta", "xəstəxana", "kitabxana", "məktəb", "şagird", "elcan", "Rahim", "raxa", "Ruhin", "dünya", "global", "combot", "robot", "mexikox", "ürək", "ciyər", "oyuncaq", "televizor", "şkaf", "aybaşı", "regl", "mədəniyyəsiz", "şüvən", "cırnamaq", "fifa", "korna", "Türkiyə", "top", "Instagram", "memoza", "çobansalat", "Tağıyev", "Nağıyev", "xəlilov", "abbasov", "mal", "inək", "qoyun", "daraq", "traktor", "aviator", "əmsal", "sumka", "pul", "aliqarx", "dayday", "ata", "ana", "nənə", "bibi", "kamera", "ətir", "gül", "əsgər", "dost", "qardaş", "dünən", "düşmən", "radio", "qəzet", "mahnı", "küknar", "kobud", "sarımtıl", "poçt",]
tapmacalar = [
    ("Mən ağlayıram, sən islanırsan. Nəəm?", "yağış"),
    ("Suda batmaz, odda yanmaz. Bu nədir?", "buz"),
    ("Üstü qırmızı, içi ağ, şirəsi şirin. Nədir?", "alma"),
    ("Hər yerdə varam, amma tutmaq olmur. Nəəm?", "hava"),
    ("Dörd ayağı var, amma qaçmır. Nədir?", "stol"),
    ("Gecə görünür, amma əllə tutulmaz. Nədir?", "ulduz"),
    ("Hər səhər gəlir, amma bir dəfə də geri dönmür. Nədir?", "günəş"),
    ("Bədənim kiçik, amma səsim böyükdür. Nədir?", "zəng"),
    ("İki qolu var, amma heç nə götürmür. Nədir?", "qapı"),
    ("Qara bədən, ağ baş, çox uçur, amma heç insan deyil. Nədir?", "quş"),
    ("Ağacdan asılır, şirin dadı var. Nədir?", "bal"),
    ("Qışda gəlir, hər şeyi örtür. Nədir?", "qar"),
    ("İçim su, amma içmirəm. Nədir?", "balıq"),
    ("Gündüz açıqdır, gecə isə qapalı. Nədir?", "göz"),
    ("Qara rəngdədir, amma ağda yazı var. Nədir?", "taxta"),
    ("Yumurta kimi yuvarlaq, içi sarı. Nədir?", "yumurta"),
    ("Yol gedir, amma heç ayağı yoxdur. Nədir?", "maşın"),
    ("Yol kəsir, amma heç hərəkət etmir. Nədir?", "qapı"),
    ("Külək əsir, amma heç bir şey görmürsən. Nədir?", "külək"),
    ("Suda yaşayar, amma nəfəs almaz. Nədir?", "balıq"),
    ("Ağdır, soyuqdur, yazda ərimir. Nədir?", "qar"),
    ("Çox qaçar, amma ayağı yoxdur. Nədir?", "su"),
    ("Gözə görünməz, amma hər yerdə var. Nədir?", "hava"),
    ("Bir otaq var, içində heç nə yoxdur. Nədir?", "qab"),
    ("Qaçır, amma heç yerə getmir. Nədir?", "saat"),
    ("Kəsəndə ağrımır, amma qanaxar. Nədir?", "soğan"),
    ("Dəmir yox, amma kilidi var. Nədir?", "açar"),
    ("Ayaq yoxdur, amma qaçar. Nədir?", "vaqon"),
    ("Beynim yoxdur, amma fikirlərimi deyirəm. Nədir?", "kitab"),
    ("Yumşaqdır, amma daş kimi sərtdir. Nədir?", "buz"),
    ("Qışda gəlir, yazda gedir. Nədir?", "qar"),
    ("Dörd dənə ayaq, amma heç qaçmır. Nədir?", "stol"),
    ("Yolda gedir, amma heç ayağı yoxdur. Nədir?", "avtomobil"),
    ("Səni izləyir, amma heç yerə getmir. Nədir?", "gölge"),
    ("İki qanadı var, amma uçmur. Nədir?", "qapı"),
    ("Bədənim kiçik, amma səsim böyükdür. Nədir?", "zəng"),
    ("Hər yerdə oluram, amma heç bir şeyi tutmuram. Nəəm?", "hava"),
    ("Qaçır, amma heç ayağı yoxdur. Nədir?", "su"),
    ("Qışda ağ olur, yayda isə yox. Nədir?", "qar"),
    ("Qaçır, amma heç hərəkət etmir. Nədir?", "saat"),
    ("Gözə görünməz, amma hər yerdədir. Nədir?", "hava"),
    ("Ayaq yoxdur, amma gedir. Nədir?", "vaqon"),
    ("Qara, ağ və qırmızı rəngdədir. Nədir?", "kitab"),
    ("Səssizdir, amma hər şeyi eşidir. Nədir?", "göz"),
    ("Üzərində çoxlu dişləri var, amma yemir. Nədir?", "saat"),
    ("Hər şeyi yandırır, amma özü yanmaz. Nədir?", "günəş"),
    ("Yumşaqdır, amma kəsir. Nədir?", "bıçaq"),
    ("İki qanadı var, amma uçmur. Nədir?", "qapı"),
    ("İçində su var, amma içmir. Nədir?", "balıq"),
    ("Bədənim ağ, amma soyuq deyil. Nədir?", "kağız"),
    ("Hər yerdə oluram, amma tutmaq olmur. Nəəm?", "hava"),
    ("Bədənim yumşaqdır, amma içim sərtdir. Nədir?", "yumurta"),
    ("Hər səhər gəlir, amma heç vaxt geri dönmür. Nədir?", "günəş"),
    ("Dörd dənə ayaq, amma heç qaçmır. Nədir?", "stol"),
    ("Qara bədən, ağ baş, çox uçur. Nədir?", "quş"),
    ("Suda yaşayar, amma nəfəs almaz. Nədir?", "balıq"),
    ("Qışda ağ, yayda yox. Nədir?", "qar"),
    ("Yol gedir, amma ayağı yoxdur. Nədir?", "maşın"),
    ("Ayaq yoxdur, amma qaçar. Nədir?", "vaqon"),
    ("Səssizdir, amma hər şeyi eşidir. Nədir?", "göz"),
    ("Qara rəngdədir, amma ağda yazı var. Nədir?", "taxta"),
    ("İçim su, amma içmirəm. Nədir?", "balıq"),
    ("Kəsəndə ağrımır, amma qanaxar. Nədir?", "soğan"),
    ("Beynim yoxdur, amma fikirlərimi deyirəm. Nədir?", "kitab"),
    ("Qışda gəlir, yazda gedir. Nədir?", "qar"),
    ("Dörd ayağı var, amma qaçmır. Nədir?", "stol"),
    ("Yol gedir, amma ayağı yoxdur. Nədir?", "avtomobil"),
    ("Səni izləyir, amma heç yerə getmir. Nədir?", "gölge"),
    ("Ayaq yoxdur, amma gedir. Nədir?", "vaqon"),
    ("Qara, ağ və qırmızı rəngdədir. Nədir?", "kitab"),
    ("Yumşaqdır, amma kəsir. Nədir?", "bıçaq"),
    ("İki qanadı var, amma uçmur. Nədir?", "qapı"),
    ("Hər şeyi yandırır, amma özü yanmaz. Nədir?", "günəş"),
    ("İçində su var, amma içmir. Nədir?", "balıq"),
    ("Bədənim ağ, amma soyuq deyil. Nədir?", "kağız"),
    ("Hər yerdə oluram, amma tutmaq olmur. Nəəm?", "hava"),
    ("Bədənim yumşaqdır, amma içim sərtdir. Nədir?", "yumurta"),
    ("Hər səhər gəlir, amma heç vaxt geri dönmür. Nədir?", "günəş"),
    ("Dörd ayağı var, amma qaçmır. Nədir?", "stol"),
    ("Qara bədən, ağ baş, çox uçur. Nədir?", "quş"),
    ("Suda yaşayar, amma nəfəs almaz. Nədir?", "balıq"),
    ("Qışda ağ, yayda yox. Nədir?", "qar"),
    ("Yol gedir, amma ayağı yoxdur. Nədir?", "maşın"),
    ("Ayaq yoxdur, amma qaçar. Nədir?", "vaqon"),
    ("Səssizdir, amma hər şeyi eşidir. Nədir?", "göz"),
    ("Qara rəngdədir, amma ağda yazı var. Nədir?", "taxta"),
    ("İçim su, amma içmirəm. Nədir?", "balıq"),
    ("Kəsəndə ağrımır, amma qanaxar. Nədir?", "soğan"),
    ("Beynim yoxdur, amma fikirlərimi deyirəm. Nədir?", "kitab"),
    ("Qışda gəlir, yazda gedir. Nədir?", "qar"),
    ("Dörd ayağı var, amma qaçmır. Nədir?", "stol")
]
texmin_shekiller = [
    ("https://imgur.com/a/2O80dBD", 23),
    ("https://imgur.com/a/EY05QMN", 22),
    ("https://imgur.com/a/U9Nywaz", 21),
    ("https://imgur.com/a/yap6uIm", 24),
    ("https://imgur.com/a/irQaTIN", 25),
    ("https://imgur.com/a/JoWs3pk", 20),
    ("https://imgur.com/a/7ziotBK", 26),
    ("https://imgur.com/a/Vl9LTiX", 29),
    ("https://imgur.com/a/WGLbUbi", 19),
    ("https://imgur.com/a/D3cGOz9", 27),
]
dogruluq_suallar = [
    "Ən utandığın hadisə nə olub?",
    "Kimdən xoşun gəlir?",
    "Ən son kimə yalan demisən?"
]

enleri_cumleler = [
    "Qrupun ən gözəli kimdir?",
    "Qrupun ən ağıllısı kimdir?",
    "Qrupun ən əylənçəlisi kimdir?",
    "Qrupun ən yaramazı kimdir?",
    "Qrupun ən səssizcəsi kimdir?",
    "Qrupun ən danışanı kimdir?",
    "Qrupun ən şirinləşəni kimdir?",
    "Qrupun ən qocalanı kimdir?",
    "Qrupun ən balacası kimdir?",
    "Qrupun ən mehriban olanı kimdir?",
    "Qrupun ən ciddi olanı kimdir?",
    "Qrupun ən gülməlisi kimdir?",
    "Qrupun ən xəyalçısı kimdir?",
    "Qrupun ən təmizləşəni kimdir?",
    "Qrupun ən səbirsizi kimdir?",
    "Qrupun ən sakit olanı kimdir?",
    "Qrupun ən enerjili olanı kimdir?",
    "Qrupun ən romantik olanı kimdir?",
    "Qrupun ən şən olanı kimdir?",
    "Qrupun ən qəribə olanı kimdir?",
    "Qrupun ən mərhəmətlisi kimdir?",
    "Qrupun ən kibirli olanı kimdir?",
    "Qrupun ən sadiq olanı kimdir?",
    "Qrupun ən xəyanətkar olanı kimdir?",
    "Qrupun ən utancaq olanı kimdir?",
    "Qrupun ən cəsur olanı kimdir?",
    "Qrupun ən qorxaq olanı kimdir?",
    "Qrupun ən dost canlısı kimdir?",
    "Qrupun ən tənha olanı kimdir?",
    "Qrupun ən optimist olanı kimdir?"
]

# Boş Xana oyunu üçün sözlər
bos_xana_sozler = [
    "telefon", "kompyuter", "kitab", "qarpiz", "yumurta", "baki", "oyuncaq",
    "qapu", "isiq", "lenkeran", "limon", "cay", "qend", "seker", "morq",
    "versiya", "salam", "oyuncu", "oyun", "forma", "esger", "saat", "muncuq",
    "yagis", "gunes", "samir", "et", "sumuk", "kondisoner", "mercedes", "bmw",
    "lada", "ortaq", "telegram", "whatsapp", "sessiz", "kelbecer", "globus",
    "qiz", "oglan", "hekim", "usta", "xestexana", "kitabxana", "mekteb",
    "sagird", "elcan", "rahim", "raxa", "ruhin", "dunya", "global", "combot",
    "robot", "mexikox", "urek", "ciyer", "televizor", "skaf", "aybaşi",
    "medeniyet", "suven", "cirnamaq", "fifa", "korna", "turkiye", "top",
    "instagram", "memoza", "coban", "tagiyev", "nagiyev", "xelilov", "abbasov",
    "mal", "inek", "qoyun", "daraq", "traktor", "aviator", "emsal", "sumka",
    "pul", "aliqarx", "dayday", "ata", "ana", "nene", "bibi", "kamera", "etir",
    "gul", "dost", "qardas", "dunen", "dusmen", "radio", "qezet", "mahni",
    "kuknar", "kobud", "sarimtil", "poct"
]

# Köstebek oyunu üçün söz cütləri
kostebek_sozler = [
    ("alma", "armud"),      # 3 nəfər alma, 1 nəfər armud
    ("it", "pişik"),       # 3 nəfər it, 1 nəfər pişik
    ("maşın", "avtobus"),  # 3 nəfər maşın, 1 nəfər avtobus
    ("kitab", "qəzet"),    # 3 nəfər kitab, 1 nəfər qəzet
    ("telefon", "kompyuter"), # 3 nəfər telefon, 1 nəfər kompyuter
    ("çay", "qəhvə"),      # 3 nəfər çay, 1 nəfər qəhvə
    ("futbol", "basketbol"), # 3 nəfər futbol, 1 nəfər basketbol
    ("yaz", "qış"),        # 3 nəfər yaz, 1 nəfər qış
    ("dəniz", "göl"),      # 3 nəfər dəniz, 1 nəfər göl
    ("güneş", "ay"),       # 3 nəfər güneş, 1 nəfər ay
    ("qırmızı", "mavi"),   # 3 nəfər qırmızı, 1 nəfər mavi
    ("məktəb", "universitet"), # 3 nəfər məktəb, 1 nəfər universitet
    ("şəhər", "kənd"),     # 3 nəfər şəhər, 1 nəfər kənd
    ("pizza", "burger"),   # 3 nəfər pizza, 1 nəfər burger
    ("musiqi", "film"),    # 3 nəfər musiqi, 1 nəfər film
    ("yumurta", "pendir"), # 3 nəfər yumurta, 1 nəfər pendir
    ("doktor", "həkim"),   # 3 nəfər doktor, 1 nəfər həkim
    ("qapı", "pəncərə"),   # 3 nəfər qapı, 1 nəfər pəncərə
    ("masa", "stul"),      # 3 nəfər masa, 1 nəfər stul
    ("su", "çay"),         # 3 nəfər su, 1 nəfər çay
    ("ağac", "çiçək"),     # 3 nəfər ağac, 1 nəfər çiçək
    ("ev", "mənzil"),      # 3 nəfər ev, 1 nəfər mənzil
    ("saat", "tarix"),     # 3 nəfər saat, 1 nəfər tarix
    ("çörək", "düyü"),     # 3 nəfər çörək, 1 nəfər düyü
    ("çanta", "baqaj"),    # 3 nəfər çanta, 1 nəfər baqaj
    ("ayaq", "əl"),        # 3 nəfər ayaq, 1 nəfər əl
    ("göz", "qulaq"),      # 3 nəfər göz, 1 nəfər qulaq
    ("burun", "ağız"),     # 3 nəfər burun, 1 nəfər ağız
    ("başmaq", "çarıq"),   # 3 nəfər başmaq, 1 nəfər çarıq
    ("paltar", "kostyum"), # 3 nəfər paltar, 1 nəfər kostyum
    ("şapka", "kasket"),   # 3 nəfər şapka, 1 nəfər kasket
    ("qələm", "karandaş"), # 3 nəfər qələm, 1 nəfər karandaş
    ("dəftər", "bloknot"), # 3 nəfər dəftər, 1 nəfər bloknot
    ("şagird", "tələbə"),  # 3 nəfər şagird, 1 nəfər tələbə
    ("müəllim", "professor"), # 3 nəfər müəllim, 1 nəfər professor
    ("avtobus", "tramvay"), # 3 nəfər avtobus, 1 nəfər tramvay
    ("qatar", "təyyarə"),  # 3 nəfər qatar, 1 nəfər təyyarə
    ("gəmi", "qayıq"),     # 3 nəfər gəmi, 1 nəfər qayıq
    ("velosiped", "motosikl"), # 3 nəfər velosiped, 1 nəfər motosikl
    ("yol", "küçə"),       # 3 nəfər yol, 1 nəfər küçə
    ("bazar", "mağaza"),   # 3 nəfər bazar, 1 nəfər mağaza
    ("restoran", "kafe"),  # 3 nəfər restoran, 1 nəfər kafe
    ("bank", "poçt"),      # 3 nəfər bank, 1 nəfər poçt
    ("xəstəxana", "klinika"), # 3 nəfər xəstəxana, 1 nəfər klinika
    ("dərman", "vitamin"), # 3 nəfər dərman, 1 nəfər vitamin
    ("şəkər", "bal"),      # 3 nəfər şəkər, 1 nəfər bal
    ("duz", "limon"),      # 3 nəfər duz, 1 nəfər limon
    ("ət", "balıq"),       # 3 nəfər ət, 1 nəfər balıq
    ("toyuq", "qazmaq"),   # 3 nəfər toyuq, 1 nəfər qazmaq
    ("inək", "qoyun"),     # 3 nəfər inək, 1 nəfər qoyun
    ("at", "eşşək"),       # 3 nəfər at, 1 nəfər eşşək
    ("qartal", "göyərçin"), # 3 nəfər qartal, 1 nəfər göyərçin
    ("gül", "qızılgül"),   # 3 nəfər gül, 1 nəfər qızılgül
    ("ağac", "kol"),       # 3 nəfər ağac, 1 nəfər kol
    ("meyvə", "tərəvəz"),  # 3 nəfər meyvə, 1 nəfər tərəvəz
    ("banan", "portağal"), # 3 nəfər banan, 1 nəfər portağal
    ("üzüm", "albalı"),    # 3 nəfər üzüm, 1 nəfər albalı
    ("pomidor", "xiyar"),  # 3 nəfər pomidor, 1 nəfər xiyar
    ("kələm", "yerkökü"),  # 3 nəfər kələm, 1 nəfər yerkökü
    ("soğan", "sarımsaq"), # 3 nəfər soğan, 1 nəfər sarımsaq
    ("kartof", "çuğundur"), # 3 nəfər kartof, 1 nəfər çuğundur
    ("yağ", "süd"),        # 3 nəfər yağ, 1 nəfər süd
    ("kərə", "qaymaq"),    # 3 nəfər kərə, 1 nəfər qaymaq
    ("şərab", "araq"),     # 3 nəfər şərab, 1 nəfər araq
    ("bira", "konyak"),    # 3 nəfər bira, 1 nəfər konyak
    ("siqaret", "qəlyun"), # 3 nəfər siqaret, 1 nəfər qəlyun
    ("oyun", "iş"),        # 3 nəfər oyun, 1 nəfər iş
    ("işçi", "patron"),    # 3 nəfər işçi, 1 nəfər patron
    ("maaş", "mükafat"),   # 3 nəfər maaş, 1 nəfər mükafat
    ("pul", "qızıl"),      # 3 nəfər pul, 1 nəfər qızıl
    ("gümüş", "almaz"),    # 3 nəfər gümüş, 1 nəfər almaz
    ("üzük", "boyunbağı"), # 3 nəfər üzük, 1 nəfər boyunbağı
    ("saat", "üzük"),      # 3 nəfər saat, 1 nəfər üzük
    ("gözlük", "linza"),   # 3 nəfər gözlük, 1 nəfər linza
    ("saç", "saqqal"),     # 3 nəfər saç, 1 nəfər saqqal
    ("əl", "barmaq"),      # 3 nəfər əl, 1 nəfər barmaq
    ("diş", "dil"),        # 3 nəfər diş, 1 nəfər dil
    ("baş", "boyun"),      # 3 nəfər baş, 1 nəfər boyun
    ("çiyin", "arxa"),     # 3 nəfər çiyin, 1 nəfər arxa
    ("qarın", "döş"),      # 3 nəfər qarın, 1 nəfər döş
    ("diz", "dirsək"),     # 3 nəfər diz, 1 nəfər dirsək
    ("sümük", "əzələ"),    # 3 nəfər sümük, 1 nəfər əzələ
    ("qan", "ürək"),       # 3 nəfər qan, 1 nəfər ürək
    ("beyin", "ciyər"),    # 3 nəfər beyin, 1 nəfər ciyər
    ("rəqs", "musiqi"),    # 3 nəfər rəqs, 1 nəfər musiqi
    ("oxumaq", "yazmaq"),  # 3 nəfər oxumaq, 1 nəfər yazmaq
    ("şeir", "hekayə"),    # 3 nəfər şeir, 1 nəfər hekayə
    ("roman", "povest"),   # 3 nəfər roman, 1 nəfər povest
    ("teatr", "kino"),     # 3 nəfər teatr, 1 nəfər kino
    ("aktyör", "rejissor"), # 3 nəfər aktyör, 1 nəfər rejissor
    ("rəssam", "heykəltaraş"), # 3 nəfər rəssam, 1 nəfər heykəltaraş
    ("şəkil", "foto"),     # 3 nəfər şəkil, 1 nəfər foto
    ("radio", "televizor"), # 3 nəfər radio, 1 nəfər televizor
    ("xəbər", "proqram"),  # 3 nəfər xəbər, 1 nəfər proqram
    ("qəzet", "jurnal"),   # 3 nəfər qəzet, 1 nəfər jurnal
    ("internet", "wifi"),  # 3 nəfər internet, 1 nəfər wifi
    ("email", "sms"),      # 3 nəfər email, 1 nəfər sms
    ("mektub", "kart"),    # 3 nəfər mektub, 1 nəfər kart
    ("hediyyə", "sürpriz"), # 3 nəfər hediyyə, 1 nəfər sürpriz
    ("ad günü", "toy"),    # 3 nəfər ad günü, 1 nəfər toy
    ("sevgi", "məhəbbət"), # 3 nəfər sevgi, 1 nəfər məhəbbət
    ("dost", "düşmən"),    # 3 nəfər dost, 1 nəfər düşmən
    ("ailəm", "qohum"),    # 3 nəfər ailəm, 1 nəfər qohum
    ("ata", "ana"),        # 3 nəfər ata, 1 nəfər ana
    ("qardaş", "bacı"),    # 3 nəfər qardaş, 1 nəfər bacı
    ("oğul", "qız"),       # 3 nəfər oğul, 1 nəfər qız
    ("əmi", "xala"),       # 3 nəfər əmi, 1 nəfər xala
    ("dayı", "bibi"),      # 3 nəfər dayı, 1 nəfər bibi
    ("nənə", "baba"),      # 3 nəfər nənə, 1 nəfər baba
    ("qonaq", "ev sahibi"), # 3 nəfər qonaq, 1 nəfər ev sahibi
    ("yolçu", "sürücü"),   # 3 nəfər yolçu, 1 nəfər sürücü
    ("alıcı", "satıcı"),   # 3 nəfər alıcı, 1 nəfər satıcı
    ("ustad", "şagird"),   # 3 nəfər ustad, 1 nəfər şagird
    ("hakim", "müdafiəçi"), # 3 nəfər hakim, 1 nəfər müdafiəçi
    ("polis", "yanğınsöndürən"), # 3 nəfər polis, 1 nəfər yanğınsöndürən
    ("həkim", "tibb bacısı"), # 3 nəfər həkim, 1 nəfər tibb bacısı
    ("pilot", "stüardesa"), # 3 nəfər pilot, 1 nəfər stüardesa
    ("aşbaz", "garson"),   # 3 nəfər aşbaz, 1 nəfər garson
    ("berber", "gözəllik ustası"), # 3 nəfər berber, 1 nəfər gözəllik ustası
    ("çiftçi", "bağban"),  # 3 nəfər çiftçi, 1 nəfər bağban
    ("builder", "arxitektor"), # 3 nəfər builder, 1 nəfər arxitektor
    ("mühəndis", "proqramçı"), # 3 nəfər mühəndis, 1 nəfər proqramçı
    ("jurnalist", "tərcüməçi"), # 3 nəfər jurnalist, 1 nəfər tərcüməçi
    ("hüquqşünas", "notarius"), # 3 nəfər hüquqşünas, 1 nəfər notarius
    ("bankir", "mühasib"),  # 3 nəfər bankir, 1 nəfər mühasib
    ("satış", "alış"),     # 3 nəfər satış, 1 nəfər alış
    ("ixrac", "idxal"),    # 3 nəfər ixrac, 1 nəfər idxal
    ("fabrik", "zavod"),   # 3 nəfər fabrik, 1 nəfər zavod
    ("ofis", "anbar"),     # 3 nəfər ofis, 1 nəfər anbar
    ("toplantı", "konfrans"), # 3 nəfər toplantı, 1 nəfər konfrans
    ("layihə", "plan"),    # 3 nəfər layihə, 1 nəfər plan
    ("nəticə", "proses"),  # 3 nəfər nəticə, 1 nəfər proses
    ("başlanğıc", "son"),  # 3 nəfər başlanğıc, 1 nəfər son
    ("problem", "həll"),   # 3 nəfər problem, 1 nəfər həll
    ("sual", "cavab"),     # 3 nəfər sual, 1 nəfər cavab
    ("xəta", "düzəliş"),  # 3 nəfər xəta, 1 nəfər düzəliş
    ("irəli", "geri"),     # 3 nəfər irəli, 1 nəfər geri
    ("yuxarı", "aşağı"),   # 3 nəfər yuxarı, 1 nəfər aşağı
    ("sağ", "sol"),        # 3 nəfər sağ, 1 nəfər sol
    ("böyük", "kiçik"),    # 3 nəfər böyük, 1 nəfər kiçik
    ("uzun", "qısa"),      # 3 nəfər uzun, 1 nəfər qısa
    ("geniş", "dar"),      # 3 nəfər geniş, 1 nəfər dar
    ("dərin", "dayaz"),    # 3 nəfər dərin, 1 nəfər dayaz
    ("yüksək", "alçaq"),   # 3 nəfər yüksək, 1 nəfər alçaq
]

# =============== GLOBAL DƏYİŞƏNLƏR ===============

# Chat-ə görə oyun state-ləri
games_state = {}

# Timer thread-ləri saxlamaq üçün
game_timers = {}

# İstifadəçi və qrup məlumatlarını saxlamaq üçün
user_chats = set()
group_chats = set()

def get_game_state(chat_id):
    if chat_id not in games_state:
        games_state[chat_id] = {
            'aparici_id': None,
            'izah_sozu': None,
            'soz_oyunu_cavab': None,
            'tapmaca_cavab': None,
            'texmin_yas': None,
            'texmin_aktiv': False,
            'qosulan_oyunçular': [],
            'dogruluk_aktiv': False,
            'active_game': None,
            'texmin_cavablar': {},  # user_id: cavab
            'reqem_oyunu': None,
            'reqem_cehd_sayi': 0,
            'enleri_cumle': None,
            'kostebek_aktiv': False,
            'kostebek_oyuncular': {},  # user_id: {'username': str, 'soz': str}
            'kostebek_kosturan': None,  # köstəbək olan oyunçu
            'kostebek_ses_verenler': {},  # user_id: voted_user_id
            'kostebek_tur': 0,
            'kostebek_izah_sirasi': [],
            'kostebek_hazirki_sira': 0,
            'bos_xana_soz': None,
            'bos_xana_gosterilen': None,
            'last_activity': datetime.datetime.now()
        }
    return games_state[chat_id]

# Oyun fəaliyyətini yenilə
def update_game_activity(chat_id):
    game_state = get_game_state(chat_id)
    game_state['last_activity'] = datetime.datetime.now()

# 5 dəqiqəlik inactivity timer
def start_inactivity_timer(chat_id):
    # Əvvəlki timer varsa, ləğv et
    if chat_id in game_timers:
        game_timers[chat_id].cancel()

    # Yeni timer başlat
    timer = threading.Timer(300.0, inactivity_timeout, args=(chat_id,))  # 300 saniyə = 5 dəqiqə
    timer.start()
    game_timers[chat_id] = timer

def inactivity_timeout(chat_id):
    game_state = get_game_state(chat_id)
    if game_state['active_game']:
        # Oyunu bitir
        reset_game_state(chat_id)
        bot.send_message(chat_id, "🌟 Görürəm mənim oynamırsınız, Məndə oyunu qapatıram  🌟")

    # Timer-i sil
    if chat_id in game_timers:
        del game_timers[chat_id]

def reset_game_state(chat_id):
    game_state = get_game_state(chat_id)
    game_state['aparici_id'] = None
    game_state['izah_sozu'] = None
    game_state['soz_oyunu_cavab'] = None
    game_state['tapmaca_cavab'] = None
    game_state['texmin_yas'] = None
    game_state['texmin_aktiv'] = False
    game_state['qosulan_oyunçular'] = []
    game_state['dogruluk_aktiv'] = False
    game_state['active_game'] = None
    game_state['texmin_cavablar'] = {}
    game_state['reqem_oyunu'] = None
    game_state['reqem_cehd_sayi'] = 0
    game_state['enleri_cumle'] = None
    game_state['kostebek_aktiv'] = False
    game_state['kostebek_oyuncular'] = {}
    game_state['kostebek_kosturan'] = None
    game_state['kostebek_ses_verenler'] = {}
    game_state['kostebek_tur'] = 0
    game_state['kostebek_izah_sirasi'] = []
    game_state['kostebek_hazirki_sira'] = 0
    game_state['bos_xana_soz'] = None
    game_state['bos_xana_gosterilen'] = None

# =============== BAŞLANĞIC MENYU ===============

def main_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(get_text(message.from_user.id, 'explain_game'), callback_data="oyun_izah"),
        types.InlineKeyboardButton(get_text(message.from_user.id, 'word_game'), callback_data="oyun_soz")
    )
    markup.row(
        types.InlineKeyboardButton(get_text(message.from_user.id, 'guess_game'), callback_data="oyun_texmin"),
        types.InlineKeyboardButton(get_text(message.from_user.id, 'riddle_game'), callback_data="oyun_tapmaca")
    )
    markup.row(
        types.InlineKeyboardButton(get_text(message.from_user.id, 'number_game'), callback_data="oyun_reqem"),
        types.InlineKeyboardButton(get_text(message.from_user.id, 'group_bests'), callback_data="oyun_enleri")
    )
    markup.row(
        types.InlineKeyboardButton(get_text(message.from_user.id, 'mole_game'), callback_data="oyun_kostebek"),
        types.InlineKeyboardButton(get_text(message.from_user.id, 'truth_dare'), callback_data="oyun_dogruluq")
    )
    markup.row(
        types.InlineKeyboardButton(get_text(message.from_user.id, 'blank_game'), callback_data="oyun_bos_xana")
    )
    bot.send_message(message.chat.id, get_text(message.from_user.id, 'game_menu'), reply_markup=markup)

@bot.message_handler(commands=['game'])
def start_game(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    # Qrup mesajlarını saxla
    group_chats.add(message.chat.id)
    main_menu(message)
    
# =============== İZAH OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_izah")
def izah_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'izah'
    game_state['aparici_id'] = None
    game_state['izah_sozu'] = random.choice(izah_sozleri)
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton("🎤 Aparıcı olmaq istəyirəm", callback_data="aparici_ol"))
    bot.send_message(call.message.chat.id, "İzah oyunu başladı! Aparıcı seçin.", reply_markup=btn)

@bot.callback_query_handler(func=lambda call: call.data == "aparici_ol")
def aparici_sec(call):
    game_state = get_game_state(call.message.chat.id)
    if game_state['aparici_id']:
        bot.answer_callback_query(call.id, "Aparıcı artıq seçilib!")
        return

    game_state['aparici_id'] = call.from_user.id
    # Buttonları alt alta düzmək üçün row_width=1
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(
        types.InlineKeyboardButton("🔍 Sözə baxmaq", callback_data="soz_goster"),
        types.InlineKeyboardButton("❌ Fikrimi Dəyişdim", callback_data="imtina"),
        types.InlineKeyboardButton(" 🔃 Sözü dəyişmək", callback_data="soz_deyis")
    )
    username = call.from_user.first_name
    bot.send_message(call.message.chat.id, f"Aparıcı seçildi: sözü izah edir, {username} ", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: call.data == "soz_goster")
def soz_goster(call):
    game_state = get_game_state(call.message.chat.id)
    if call.from_user.id != game_state['aparici_id']:
        bot.answer_callback_query(call.id, "Sənin sıran deyil!!!!")
        return
    bot.answer_callback_query(call.id, text=f"Söz: {game_state['izah_sozu']}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "imtina")
def aparici_imtina(call):
    game_state = get_game_state(call.message.chat.id)
    if call.from_user.id != game_state['aparici_id']:
        bot.answer_callback_query(call.id, "Sənin sıran deyil!!!!")
        return

    game_state['aparici_id'] = None
    username = call.from_user.first_name
    bot.send_message(call.message.chat.id, f"{username} Aparıcı imtina etdi,")
    izah_oyunu_basla(call)

@bot.callback_query_handler(func=lambda call: call.data == "soz_deyis")
def soz_deyis(call):
    game_state = get_game_state(call.message.chat.id)
    if call.from_user.id != game_state['aparici_id']:
        bot.answer_callback_query(call.id, "Sənin sıran deyil!!!!")
        return

    game_state['izah_sozu'] = random.choice(izah_sozleri)
    bot.answer_callback_query(call.id, "Yeni söz seçildi ✅")

# =============== SÖZ OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_soz")
def soz_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'soz'
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    yeni_soz(call.message)

def yeni_soz(message):
    game_state = get_game_state(message.chat.id)
    game_state['soz_oyunu_cavab'] = random.choice(soz_oyunu_sozler)
    herfler = list(game_state['soz_oyunu_cavab'])
    random.shuffle(herfler)
    bot.send_message(message.chat.id, f"🌟 {''.join(herfler)} 🌟\nDüzgün sözü tapmağa çalış ✨\n\nSözü keçmək üçün /kec yaz ✨")

@bot.message_handler(commands=['kec'])
def soz_kec(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    game_state = get_game_state(message.chat.id)
    if game_state['active_game'] == 'soz':
        bot.send_message(message.chat.id, "Köhnə söz keçildi 🎯")
        yeni_soz(message)

# =============== TAPMACA OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_tapmaca")
def tapmaca_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'tapmaca'
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    yeni_tapmaca(call.message)

def yeni_tapmaca(message):
    game_state = get_game_state(message.chat.id)
    sual, cavab = random.choice(tapmacalar)
    game_state['tapmaca_cavab'] = cavab
    bot.send_message(message.chat.id, f"🎯 {sual}")

# =============== TƏXMİN OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_texmin")
def texmin_oyunu(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'texmin'
    sekil, yas = random.choice(texmin_shekiller)
    game_state['texmin_yas'] = yas
    game_state['texmin_aktiv'] = True
    game_state['texmin_cavablar'] = {}
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    bot.send_photo(call.message.chat.id, sekil, caption="Bu insanın yaşını təxmin et! 20 saniyən var.")

    # Timer thread başlat
    threading.Thread(target=texmin_timer_fun, args=(call.message.chat.id,)).start()

def texmin_timer_fun(chat_id):
    time.sleep(20)
    game_state = get_game_state(chat_id)
    if game_state['texmin_aktiv']:
        game_state['texmin_aktiv'] = False

        # Ən yaxın cavabı tap
        if game_state['texmin_cavablar']:
            min_ferq = float('inf')
            qazanan = None
            qazanan_cavab = None

            for user_id, cavab in game_state['texmin_cavablar'].items():
                ferq = abs(cavab - game_state['texmin_yas'])
                if ferq < min_ferq:
                    min_ferq = ferq
                    qazanan = user_id
                    qazanan_cavab = cavab

            if qazanan:
                try:
                    user_info = bot.get_chat_member(chat_id, qazanan)
                    username = user_info.user.first_name
                    bot.send_message(chat_id, f"⏰ Vaxt bitdi!\n🎯 Ən yaxın cavab: {username} ({qazanan_cavab} yaş)\nDoğru cavab: {game_state['texmin_yas']} yaş")
                except:
                    bot.send_message(chat_id, f"⏰ Vaxt bitdi!\nDoğru cavab: {game_state['texmin_yas']} yaş")
            else:
                bot.send_message(chat_id, f"⏰ Vaxt bitdi! Doğru cavab: {game_state['texmin_yas']} yaş")
        else:
            bot.send_message(chat_id, f"⏰ Vaxt bitdi! Doğru cavab: {game_state['texmin_yas']} yaş")

# =============== RƏQƏM OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_reqem")
def reqem_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'reqem'
    game_state['reqem_oyunu'] = random.randint(1, 100)
    game_state['reqem_cehd_sayi'] = 0
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    bot.send_message(call.message.chat.id, "🔢 Rəqəm Oyunu başladı!\n\nMən 1-dən 100-ə qədər bir rəqəm seçdim.\nBu rəqəmi tapmağa çalış! 🎯")

# =============== QRUPUN ENLƏRİ ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_enleri")
def enleri_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'enleri'
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    yeni_enleri_cumle(call.message)

def yeni_enleri_cumle(message):
    game_state = get_game_state(message.chat.id)
    game_state['enleri_cumle'] = random.choice(enleri_cumleler)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Yeni Tur 🎲", callback_data="enleri_yeni_tur"))

    bot.send_message(
        message.chat.id,
        f"👑 {game_state['enleri_cumle']}\n\n💭 Cavabınızı yazın və müzakirə edin!",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "enleri_yeni_tur")
def enleri_yeni_tur(call):
    game_state = get_game_state(call.message.chat.id)
    if game_state['active_game'] == 'enleri':
        yeni_enleri_cumle(call.message)

# =============== KÖSTEBEK GAME ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_kostebek")
def kostebek_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'kostebek'
    game_state['kostebek_aktiv'] = True
    game_state['kostebek_oyuncular'] = {}
    game_state['kostebek_tur'] = 0
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🎮 Oyuna Qoşul", callback_data="kostebek_qosul"))

    bot.send_message(
        call.message.chat.id,
        "🦫 Köstəbək Game başladı!\n\n🎯 Minimum 4 oyunçu lazımdır\n🔍 3 oyunçuya eyni söz, 1 köstəbəyə fərqli söz veriləcək\n\n👥 Qoşulmaq üçün buttona basın:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "kostebek_qosul")
def kostebek_qosul(call):
    game_state = get_game_state(call.message.chat.id)
    if not game_state['kostebek_aktiv'] or game_state['active_game'] != 'kostebek':
        bot.answer_callback_query(call.id, "Köstəbək oyunu aktiv deyil!")
        return

    user_id = call.from_user.id
    username = call.from_user.first_name

    if user_id not in game_state['kostebek_oyuncular']:
        game_state['kostebek_oyuncular'][user_id] = {'username': username, 'soz': ''}

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("🎮 Oyuna Qoşul", callback_data="kostebek_qosul"))
        if len(game_state['kostebek_oyuncular']) >= 2:
            keyboard.add(types.InlineKeyboardButton("🚀 Oyunu Başlat", callback_data="kostebek_basla"))

        oyuncu_list = '\n'.join([f"👤 {data['username']}" for data in game_state['kostebek_oyuncular'].values()])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🦫 Köstəbək Game\n\n👥 Qoşulan oyunçular ({len(game_state['kostebek_oyuncular'])}):\n{oyuncu_list}\n\n{'🚀 Oyunu başlatmaq üçün düyməni basın!' if len(game_state['kostebek_oyuncular']) >= 2 else '⏳ Minimum 2 oyunçu lazımdır...'}",
            reply_markup=keyboard
        )
        bot.answer_callback_query(call.id, f"✅ {username} oyuna qoşuldu!")
    else:
        bot.answer_callback_query(call.id, "⚠️ Artıq oyundasan!")

@bot.callback_query_handler(func=lambda call: call.data == "kostebek_basla")
def kostebek_oyunu_basla(call):
    game_state = get_game_state(call.message.chat.id)
    if len(game_state['kostebek_oyuncular']) < 2:
        bot.answer_callback_query(call.id, "❌ Minimum 2 oyunçu lazımdır!")
        return

    # Sözləri təyin et
    normal_soz, kostebek_sozu = random.choice(kostebek_sozler)
    oyuncu_list = list(game_state['kostebek_oyuncular'].keys())

    # Köstəbəyi seç
    kostebek_id = random.choice(oyuncu_list)
    game_state['kostebek_kosturan'] = kostebek_id

    # Sözləri təyin et
    for user_id in game_state['kostebek_oyuncular']:
        if user_id == kostebek_id:
            game_state['kostebek_oyuncular'][user_id]['soz'] = kostebek_sozu
        else:
            game_state['kostebek_oyuncular'][user_id]['soz'] = normal_soz

    # İzah sırasını təyin et
    game_state['kostebek_izah_sirasi'] = oyuncu_list.copy()
    random.shuffle(game_state['kostebek_izah_sirasi'])
    game_state['kostebek_hazirki_sira'] = 0
    game_state['kostebek_tur'] += 1

    # Qrupda hər oyunçu üçün söz buttonları yaradın
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for user_id, data in game_state['kostebek_oyuncular'].items():
        keyboard.add(types.InlineKeyboardButton(f"📝 {data['username']}", callback_data=f"kostebek_soz_{user_id}"))

    # İlk oyunçu və növbətiyə keçmək buttonunu əlavə et
    ilk_oyuncu = game_state['kostebek_oyuncular'][game_state['kostebek_izah_sirasi'][0]]['username']
    keyboard.add(types.InlineKeyboardButton("➡️ Növbətiyə Keç", callback_data="kostebek_novbeti"))

    bot.send_message(
        call.message.chat.id,
        f"🦫 Köstəbək Game Tur {game_state['kostebek_tur']} başladı!\n\n🎯 Hər oyunçu öz sözünə baxmaq üçün öz buttonuna bassın\n📝 İzah sırası: {ilk_oyuncu}\n\n💡 Hər oyunçu öz sözünü izah etsin, köstəbəyi tapaq!",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("kostebek_soz_"))
def kostebek_soz_goster(call):
    user_id = int(call.data.split("_")[2])

    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "❌ Bu sənin buttonun deyil!!")
        return

    game_state = get_game_state(call.message.chat.id)
    if user_id in game_state['kostebek_oyuncular']:
        soz = game_state['kostebek_oyuncular'][user_id]['soz']
        bot.answer_callback_query(call.id, f"📝 Sənin sözün: {soz}", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ Oyunda deyilsən!")

@bot.callback_query_handler(func=lambda call: call.data == "kostebek_novbeti")
def kostebek_novbeti_callback(call):
    game_state = get_game_state(call.message.chat.id)
    if game_state['active_game'] != 'kostebek' or not game_state['kostebek_aktiv']:
        bot.answer_callback_query(call.id, "❌ Köstəbək oyunu aktiv deyil!")
        return

    if game_state['kostebek_hazirki_sira'] < len(game_state['kostebek_izah_sirasi']) - 1:
        game_state['kostebek_hazirki_sira'] += 1
        novbeti_oyuncu = game_state['kostebek_oyuncular'][game_state['kostebek_izah_sirasi'][game_state['kostebek_hazirki_sira']]]['username']

        # Keyboard yenilə - izah menyusu
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for user_id, data in game_state['kostebek_oyuncular'].items():
            keyboard.add(types.InlineKeyboardButton(f"📝 {data['username']}", callback_data=f"kostebek_soz_{user_id}"))

        keyboard.add(types.InlineKeyboardButton("➡️ Növbətiyə Keç", callback_data="kostebek_novbeti"))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🦫 Köstəbək Game Tur {game_state['kostebek_tur']}\n\n🎯 Hər oyunçu öz sözünə baxmaq üçün öz buttonuna bassın\n📝 İzah sırası: {novbeti_oyuncu}\n\n💡 Hər oyunçu öz sözünü izah etsin, köstəbəyi tapaq!",
            reply_markup=keyboard
        )
        bot.answer_callback_query(call.id, f"✅ Növbəti oyunçu: {novbeti_oyuncu}")
    else:
        # Bütün oyunçular izah etdi, səs vermə başlasın
        bot.answer_callback_query(call.id, "✅ Bütün oyunçular izah etdi, indi səs vermə vaxtı!")
        kostebek_ses_verme_basla(call.message.chat.id)

@bot.message_handler(commands=['novbe'])
def kostebek_novbe(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    game_state = get_game_state(message.chat.id)
    if game_state['active_game'] != 'kostebek' or not game_state['kostebek_aktiv']:
        return

    if game_state['kostebek_hazirki_sira'] < len(game_state['kostebek_izah_sirasi']) - 1:
        game_state['kostebek_hazirki_sira'] += 1
        novbeti_oyuncu = game_state['kostebek_oyuncular'][game_state['kostebek_izah_sirasi'][game_state['kostebek_hazirki_sira']]]['username']
        bot.send_message(message.chat.id, f"📝 Növbəti oyunçu: {novbeti_oyuncu}")
    else:
        # Bütün oyunçular izah etdi, səs vermə başlasın
        kostebek_ses_verme_basla(message.chat.id)

def kostebek_ses_verme_basla(chat_id):
    game_state = get_game_state(chat_id)
    game_state['kostebek_ses_verenler'] = {}

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for user_id, data in game_state['kostebek_oyuncular'].items():
        buttons.append(types.InlineKeyboardButton(f"🗳 {data['username']}", callback_data=f"kostebek_ses_{user_id}"))

    # Buttonları 2-2 sıra ilə əlavə et
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            keyboard.row(buttons[i], buttons[i + 1])
        else:
            keyboard.row(buttons[i])

    bot.send_message(
        chat_id,
        f"🗳️ Səs vermə vaxtı!\n\n❓ Kimdən şübhələnirsiniz? Kimə səs verəcəksiniz?\n\n👥 Hər oyunçu 1 səs verə bilər:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("kostebek_ses_"))
def kostebek_ses_ver(call):
    game_state = get_game_state(call.message.chat.id)
    if game_state['active_game'] != 'kostebek' or not game_state['kostebek_aktiv']:
        bot.answer_callback_query(call.id, "Köstəbək oyunu aktiv deyil!")
        return

    voter_id = call.from_user.id
    voted_id = int(call.data.split("_")[2])

    # Oyunçu oyunda olmalıdır
    if voter_id not in game_state['kostebek_oyuncular']:
        bot.answer_callback_query(call.id, "❌ Oyunda deyilsən!")
        return

    # Özünə səs verə bilməz
    if voter_id == voted_id:
        bot.answer_callback_query(call.id, "❌ Özünə səs verə bilməzsən!")
        return

    # Səsini qeyd et
    game_state['kostebek_ses_verenler'][voter_id] = voted_id

    voted_username = game_state['kostebek_oyuncular'][voted_id]['username']
    bot.answer_callback_query(call.id, f"✅ {voted_username} üçün səs verdin!")

    # Hamı səs verdirilsə nəticəni göstər
    if len(game_state['kostebek_ses_verenler']) == len(game_state['kostebek_oyuncular']):
        kostebek_ses_verme_netice(call.message.chat.id)

def kostebek_ses_verme_netice(chat_id):
    game_state = get_game_state(chat_id)

    # Səsləri hesabla
    ses_sayilari = {}
    for voted_id in game_state['kostebek_ses_verenler'].values():
        ses_sayilari[voted_id] = ses_sayilari.get(voted_id, 0) + 1

    # Ən çox səs alan(lar)ı tap
    max_ses = max(ses_sayilari.values())
    kenarlashacaq = [user_id for user_id, ses_sayi in ses_sayilari.items() if ses_sayi == max_ses]

    # Nəticəni göstər
    netice_metni = "🗳️ Səs vermə nəticəsi:\n\n"
    for user_id, ses_sayi in sorted(ses_sayilari.items(), key=lambda x: x[1], reverse=True):
        username = game_state['kostebek_oyuncular'][user_id]['username']
        netice_metni += f"👤 {username}: {ses_sayi} səs\n"

    # Köstəbəyin həqiqi kimliyini açıqla
    kostebek_username = game_state['kostebek_oyuncular'][game_state['kostebek_kosturan']]['username']

    if game_state['kostebek_kosturan'] in kenarlashacaq:
        netice_metni += f"\n🎉 Təbriklər! Köstəbək tapıldı!\n🦫 Köstəbək: {kostebek_username}"
        # Oyunu yenidən başlat
        kostebek_yeni_tur_basla(chat_id)
    else:
        kenarashdigi = game_state['kostebek_oyuncular'][kenarlashacaq[0]]['username'] if len(kenarlashacaq) == 1 else "Bərabərlik"
        netice_metni += f"\n😞 Səhv! Köstəbək qaçdı!\n🦫 Həqiqi köstəbək: {kostebek_username}\n❌ Kənara aşdı: {kenarashdigi}"

        # Kənara aşanı oyundan çıxart
        if len(kenarlashacaq) == 1:
            del game_state['kostebek_oyuncular'][kenarlashacaq[0]]

        # Oyunçu sayı yetərdirsə yeni tur
        if len(game_state['kostebek_oyuncular']) >= 4:
            kostebek_yeni_tur_basla(chat_id)
        else:
            netice_metni += "\n\n❌ Kifayət qədər oyunçu qalmadı, oyun bitdi!"
            game_state['kostebek_aktiv'] = False

    bot.send_message(chat_id, netice_metni)

def kostebek_yeni_tur_basla(chat_id):
    game_state = get_game_state(chat_id)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🎮 Yeni Tur Başlat", callback_data="kostebek_yeni_tur"))

    bot.send_message(
        chat_id,
        f"🦫 Yeni tur üçün hazırsınız!\n\n👥 Qalan oyunçular: {len(game_state['kostebek_oyuncular'])} nəfər",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "kostebek_yeni_tur")
def kostebek_yeni_tur(call):
    game_state = get_game_state(call.message.chat.id)
    if len(game_state['kostebek_oyuncular']) < 4:
        bot.answer_callback_query(call.id, "❌ Minimum 4 oyunçu lazımdır!")
        return

    kostebek_oyunu_basla(call)

# =============== BOŞ XANA OYUNU ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_bos_xana")
def bos_xana_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'bos_xana'
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    yeni_bos_xana_tur(call.message)

def yeni_bos_xana_tur(message):
    game_state = get_game_state(message.chat.id)
    # Təsadüfi söz seç
    game_state['bos_xana_soz'] = random.choice(bos_xana_sozler)

    # Sözün bəzi hərflərini gizlə (təxminən yarısını)
    soz = game_state['bos_xana_soz']
    soz_length = len(soz)
    gizlenecek_sayi = max(1, soz_length // 2)  # Ən azı 1 hərf gizlənsin

    # Hansı mövqelərin gizlənəcəyini təyin et
    gizli_mövqeler = random.sample(range(soz_length), gizlenecek_sayi)

    # Göstəriləcək sözü yarat
    gosterilen_soz = ""
    for i, herf in enumerate(soz):
        if i in gizli_mövqeler:
            gosterilen_soz += "_"
        else:
            gosterilen_soz += herf

    game_state['bos_xana_gosterilen'] = gosterilen_soz

    bot.send_message(
        message.chat.id,
        f"🚀 Yeni Tur Başlandı 🚀\n\n🧩 {gosterilen_soz} 🌟\n\nBoş olan xanaları doldurmağa çalış 🎲\nStrategiya Karyeranı artır 🪄\n\n💡 Sözü keçmək üçün /burax yaz"
    )

@bot.message_handler(commands=['burax'])
def bos_xana_burax(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    game_state = get_game_state(message.chat.id)
    if game_state['active_game'] == 'bos_xana':
        bot.send_message(message.chat.id, f"⏭️ Söz keçildi! Doğru cavab: **{game_state['bos_xana_soz']}** idi")
        yeni_bos_xana_tur(message)

# =============== DOĞRULUQ / CƏSARƏT ===============

@bot.callback_query_handler(func=lambda call: call.data == "oyun_dogruluq")
def dogruluq_basla(call):
    game_state = get_game_state(call.message.chat.id)
    game_state['active_game'] = 'dogruluq'
    game_state['qosulan_oyunçular'] = []
    game_state['dogruluk_aktiv'] = True
    update_game_activity(call.message.chat.id)
    start_inactivity_timer(call.message.chat.id)
    bot.send_message(call.message.chat.id, "🔥 Doğruluq / Cəsarət oyunu!\n\n📝 Qoşulmaq üçün: /qosul\n🎮 Başlatmaq üçün: /basla")

@bot.message_handler(commands=['qosul'])
def qosul(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    game_state = get_game_state(message.chat.id)
    if not game_state['dogruluk_aktiv'] or game_state['active_game'] != 'dogruluq':
        return

    if message.from_user.id not in game_state['qosulan_oyunçular']:
        game_state['qosulan_oyunçular'].append(message.from_user.id)
        username = message.from_user.first_name
        bot.send_message(message.chat.id, f"✅ {username} oyuna qoşuldu!\n\n👥 Qoşulan oyunçular: {len(game_state['qosulan_oyunçular'])}")
    else:
        username = message.from_user.first_name
        bot.send_message(message.chat.id, f"⚠️ {username} artıq oyundasan!")

@bot.message_handler(commands=['basla'])
def dogruluk_oyunu_basla(message):
    # Yalnız qruplarda işləsin
    if message.chat.type not in ['group', 'supergroup']:
        bot.send_message(message.chat.id, get_text(message.from_user.id, 'group_only'))
        return

    game_state = get_game_state(message.chat.id)
    if game_state['active_game'] != 'dogruluq' or not game_state['dogruluk_aktiv']:
        return

    if len(game_state['qosulan_oyunçular']) < 2:
        bot.send_message(message.chat.id, "❌ Ən azı 2 oyunçu lazımdır!")
        return

    dogruluk_yeni_tur_basla(message.chat.id)

def dogruluk_yeni_tur_basla(chat_id):
    game_state = get_game_state(chat_id)
    if len(game_state['qosulan_oyunçular']) >= 2:
        verici_id = random.choice(game_state['qosulan_oyunçular'])
        cavab_verici_id = random.choice([x for x in game_state['qosulan_oyunçular'] if x != verici_id])

        try:
            verici_info = bot.get_chat_member(chat_id, verici_id)
            cavab_verici_info = bot.get_chat_member(chat_id, cavab_verici_id)

            verici_username = verici_info.user.first_name
            cavab_verici_username = cavab_verici_info.user.first_name
        except:
            verici_username = "oyunçu"
            cavab_verici_username = "oyunçu"

        bot.send_message(chat_id, f"🎲 Doğruluq turu başlayır...\n\n{verici_username} → {cavab_verici_username}\n\n💬 {verici_username}, sualını ver!")

        btn = types.InlineKeyboardMarkup()
        btn.add(types.InlineKeyboardButton("Yeni tur 🎲", callback_data="dogruluk_yeni_tur"))
        bot.send_message(chat_id, "Cavabı verdikdən sonra yeni tur üçün aşağıdakı düyməni basın", reply_markup=btn)

@bot.callback_query_handler(func=lambda call: call.data == "dogruluk_yeni_tur")
def dogruluk_yeni_tur(call):
    dogruluk_yeni_tur_basla(call.message.chat.id)

# =============== MESSAGE HANDLER-LƏR ===============

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Qrup mesajlarını saxla
    if message.chat.type in ['group', 'supergroup']:
        group_chats.add(message.chat.id)

    game_state = get_game_state(message.chat.id)

    # Oyun aktivsə və mesaj oyunla əlaqəlidirsə fəaliyyəti yenilə
    if game_state['active_game']:
        update_game_activity(message.chat.id)
        start_inactivity_timer(message.chat.id)

    # İzah oyunu cavab yoxlanması
    if (game_state['active_game'] == 'izah' and
        game_state['aparici_id'] and
        game_state['izah_sozu'] and
        message.from_user.id != game_state['aparici_id']):

        if message.text and message.text.lower() == game_state['izah_sozu'].lower():
            # Yeni aparıcı təyin et
            old_word = game_state['izah_sozu']
            game_state['aparici_id'] = message.from_user.id
            game_state['izah_sozu'] = random.choice(izah_sozleri)

            username = message.from_user.first_name
            bot.send_message(message.chat.id, f"🎉 {username} - düzgün sözü tapdı,  yeni sözü izah edir🥳")

            # Buttonları alt alta
            menu = types.InlineKeyboardMarkup(row_width=1)
            menu.add(
                types.InlineKeyboardButton("🔍 Sözə baxmaq", callback_data="soz_goster"),
                types.InlineKeyboardButton("❌ Fikrimi dəyişdim", callback_data="imtina"),
                types.InlineKeyboardButton("🔃 Sözü dəyişmək", callback_data="soz_deyis")
            )
            bot.send_message(message.chat.id, f"Aparıcı: {username}", reply_markup=menu)
            return

    # Söz oyunu cavab yoxlanması
    if (game_state['active_game'] == 'soz' and
        game_state['soz_oyunu_cavab'] and
        message.text):

        if message.text.lower() == game_state['soz_oyunu_cavab'].lower():
            old_word = game_state['soz_oyunu_cavab']
            game_state['soz_oyunu_cavab'] = random.choice(soz_oyunu_sozler)
            herfler = list(game_state['soz_oyunu_cavab'])
            random.shuffle(herfler)

            username = message.from_user.first_name
            bot.send_message(message.chat.id, f"🎉 {username} sözü tapdın! {old_word}\n\nYeni söz: 🌟{''.join(herfler)}🌟\nSözü keçmək üçün /kec yaz ✨")
            return

    # Tapmaca cavab yoxlanması
    if (game_state['active_game'] == 'tapmaca' and
        game_state['tapmaca_cavab'] and
        message.text):

        if message.text.lower() == game_state['tapmaca_cavab'].lower():
            username = message.from_user.first_name
            bot.send_message(message.chat.id, f"🌟 Bəli! Düzgün tapdın, {username}!")
            yeni_tapmaca(message)
            return

    # Təxmin oyunu cavab yoxlanması
    if (game_state['active_game'] == 'texmin' and
        game_state['texmin_aktiv'] and
        game_state['texmin_yas'] and
        message.text):

        try:
            yas = int(message.text)
            # Cavabı yaddaşa sal
            game_state['texmin_cavablar'][message.from_user.id] = yas

            if abs(yas - game_state['texmin_yas']) <= 1:
                game_state['texmin_aktiv'] = False
                username = message.from_user.first_name
                bot.send_message(message.chat.id, f"🎯 Əla təxmin {username}! Doğru cavab: {game_state['texmin_yas']} yaş")
                # Yeni tur başlat
                time.sleep(2)
                sekil, yas = random.choice(texmin_shekiller)
                game_state['texmin_yas'] = yas
                game_state['texmin_aktiv'] = True
                game_state['texmin_cavablar'] = {}
                bot.send_photo(message.chat.id, sekil, caption="🎯 Yeni tur! Bu insanın yaşını təxmin et! 20 saniyən var.")
                threading.Thread(target=texmin_timer_fun, args=(message.chat.id,)).start()
                return
        except ValueError:
            pass

    # Rəqəm oyunu cavab yoxlanması
    if (game_state['active_game'] == 'reqem' and
        game_state['reqem_oyunu'] and
        message.text):

        try:
            reqem = int(message.text)
            game_state['reqem_cehd_sayi'] += 1

            if reqem == game_state['reqem_oyunu']:
                bot.send_message(message.chat.id, f"🎉 Təbriklər {message.from_user.first_name}\n🔢 Düzgün Rəqəm {game_state['reqem_oyunu']}\n🔃 Edilən Cəhd Sayı {game_state['reqem_cehd_sayi']}")
                # Yeni oyun başlat
                game_state['reqem_oyunu'] = random.randint(1, 100)
                game_state['reqem_cehd_sayi'] = 0
                bot.send_message(message.chat.id, "🔢 Yeni rəqəm seçildi! 1-dən 100-ə qədər yeni rəqəmi tap! 🎯")
                return
            elif reqem > game_state['reqem_oyunu']:
                bot.send_message(message.chat.id, "Dostum! Çox böyük dedin aşağı en🎯")
                return
            elif reqem < game_state['reqem_oyunu']:
                bot.send_message(message.chat.id, "Dostum! Çox az dedin biraz yüksəlt")
                return
        except ValueError:
            pass

    # Boş Xana oyunu cavab yoxlanması
    if (game_state['active_game'] == 'bos_xana' and
        game_state['bos_xana_soz'] and
        message.text):

        if message.text.lower().strip() == game_state['bos_xana_soz'].lower():
            username = message.from_user.first_name
            bot.send_message(message.chat.id, f"🎉 Əla! {username} sözü tapdı! 🌟")
            yeni_bos_xana_tur(message)
            return
