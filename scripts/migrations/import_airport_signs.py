import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import database as db

AIRPORT_SIGNS = [
    {
        "type": "vocab",
        "front": "arrivals",
        "back": "зона прилёта / прилёт (рейсов)",
        "transcription": "/əˈraɪ.vəlz/",
        "explanation": "Ударение на второй слог: ar·RI·vals. Зона аэропорта, куда выходят прилетевшие пассажиры.",
        "example": "I will meet you at the arrivals hall right outside the exit.",
        "pronunciation_text": "arrivals",
        "raw_original": "arrivals [ударение: ar·RI·vals]"
    },
    {
        "type": "vocab",
        "front": "bag drop",
        "back": "стойка сдачи багажа (baggage drop-off)",
        "transcription": "/ˈbæɡ drɒp/",
        "explanation": "Стойка, где вы просто отдаете чемодан, если уже зарегистрировались на рейс онлайн.",
        "example": "Since we checked in online, we only need to leave our suitcases at the bag drop desk.",
        "pronunciation_text": "bag drop",
        "raw_original": "bag drop"
    },
    {
        "type": "vocab",
        "front": "baggage reclaim",
        "back": "выдача багажа / зона получения багажа",
        "transcription": "/ˈbæɡ.ɪdʒ rɪˌkleɪm/",
        "explanation": "Ударение на RE: baggage re·CLAIM (US: baggage claim). Зона с багажными лентами.",
        "example": "Go straight to baggage reclaim carousel 4 to collect your luggage.",
        "pronunciation_text": "baggage reclaim",
        "raw_original": "baggage reclaim [ударение: re·CLAIM]"
    },
    {
        "type": "vocab",
        "front": "check-in",
        "back": "стойка регистрации / регистрация на рейс",
        "transcription": "/ˈtʃek.ɪn/",
        "explanation": "Ударение на первый слог CHECK-in. Место, где проверяют билет, паспорт и выдают посадочный талон (boarding pass).",
        "example": "Please have your passport and booking reference ready at the check-in desk.",
        "pronunciation_text": "check-in",
        "raw_original": "check-in [ударение: CHECK-in]"
    },
    {
        "type": "vocab",
        "front": "customs",
        "back": "таможня / таможенный контроль",
        "transcription": "/ˈkʌs.təmz/",
        "explanation": "Ударение: CUS·toms. Проверка декларируемых товаров, валюты и запрещенных к ввозу вещей (не путать с паспортным контролем!).",
        "example": "Do you have anything to declare before going through customs?",
        "pronunciation_text": "customs",
        "raw_original": "customs [ударение: CUS-toms]"
    },
    {
        "type": "vocab",
        "front": "departures",
        "back": "зона вылета / вылет (рейсов)",
        "transcription": "/dɪˈpɑː.tʃəz/",
        "explanation": "Ударение на второй слог: de·PAR·tures. Секция аэропорта для вылетающих пассажиров.",
        "example": "The departures board shows that our flight to London is on time.",
        "pronunciation_text": "departures",
        "raw_original": "departures [ударение: de-PAR-tures]"
    },
    {
        "type": "vocab",
        "front": "gates",
        "back": "выходы на посадку (гейты)",
        "transcription": "/ɡeɪts/",
        "explanation": "Выходы, ведущие непосредственно в телетрап (рукав) или автобус к самолету.",
        "example": "Flight BA245 is now boarding at gate 12.",
        "pronunciation_text": "gates",
        "raw_original": "gates"
    },
    {
        "type": "vocab",
        "front": "lifts",
        "back": "лифты (британский вариант; в US: elevators)",
        "transcription": "/lɪfts/",
        "explanation": "UK: lifts / US: elevators. Лифты в здании аэропорта для перемещения между этажами с багажом.",
        "example": "Take the lifts to the second floor for international departures.",
        "pronunciation_text": "lifts",
        "raw_original": "lifts"
    },
    {
        "type": "vocab",
        "front": "passport control",
        "back": "паспортный контроль (пограничный контроль)",
        "transcription": "/ˈpɑːs.pɔːt kənˌtrəʊl/",
        "explanation": "Ударение на PASS-port и con-TROL. Проверка виз, паспортов и права пересечения границы.",
        "example": "There was a very long queue at passport control this morning.",
        "pronunciation_text": "passport control",
        "raw_original": "passport control [ударение: PASS-port con-TROL]"
    },
    {
        "type": "vocab",
        "front": "security check",
        "back": "предполётный досмотр / контроль безопасности",
        "transcription": "/sɪˈkjʊə.rə.ti tʃek/",
        "explanation": "Ударение на CU: se-CU-rity check. Просвечивание ручной клади сканером и проход через металлодетектор.",
        "example": "Remember to take your laptop and liquids out of your bag for the security check.",
        "pronunciation_text": "security check",
        "raw_original": "security check [ударение: se-CU-rity]"
    },
    {
        "type": "vocab",
        "front": "terminal",
        "back": "терминал (здание аэропорта)",
        "transcription": "/ˈtɜː.mɪ.nəl/",
        "explanation": "Ударение на первый слог: TER-mi-nal. Большое здание аэровокзала (Terminal 1, Terminal 2).",
        "example": "Our flight departs from Terminal 3.",
        "pronunciation_text": "terminal",
        "raw_original": "terminal [ударение: TER-mi-nal]"
    },
    {
        "type": "vocab",
        "front": "trolley",
        "back": "багажная тележка (в аэропорту)",
        "transcription": "/ˈtrɒl.i/",
        "explanation": "Ударение на первый слог: TROL-ley (US: luggage cart). Тележка на колесиках для перевозки тяжелых чемоданов.",
        "example": "Put your heavy bags on a trolley so you don't have to carry them.",
        "pronunciation_text": "trolley",
        "raw_original": "trolley [ударение: TROL-ley]"
    }
]

def main():
    added = 0
    with db.get_connection() as conn:
        cursor = conn.cursor()
        for item in AIRPORT_SIGNS:
            cursor.execute(
                "SELECT id FROM cards WHERE user_id = 0 AND front = ? AND type = ?",
                (item["front"], item["type"])
            )
            exists = cursor.fetchone()
            if not exists:
                db.add_card(item, user_id=0)
                added += 1
                print(f"[+] Добавлено: {item['front']} -> {item['back']}")
            else:
                print(f"[*] Уже есть в базе: {item['front']}")
                
    stats = db.get_stats(user_id=0)
    print(f"\n[✓] Успешно добавлено: {added} карточек.")
    print(f"Всего в базе: {stats['total']} (готовы к повторению: {stats['due']})")
    print(f"Разбивка по типам: {stats['by_type']}")

if __name__ == "__main__":
    main()
