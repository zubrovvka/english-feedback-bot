import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import database as db

NEW_CARDS = [
    {
        "type": "vocab",
        "front": "stopover",
        "back": "стоповер / пересадка с остановкой (промежуточная остановка в пути)",
        "transcription": "/ˈstɒp.əʊ.vər/",
        "explanation": "Определение: a short stay somewhere between two parts of a journey. В отличие от обычной короткой пересадки (layover), стоповер длится больше 24 часов и позволяет погулять по городу.",
        "example": "We had a 24-hour stopover in Doha on our way to Bangkok.",
        "pronunciation_text": "stopover",
        "raw_original": "stopover /ˈstɒpəʊvə/ = a short stay somewhere between two parts of a journey"
    },
    {
        "type": "vocab",
        "front": "connecting flight",
        "back": "стыковочный рейс / пересадочный рейс",
        "transcription": "/kəˈnek.tɪŋ flaɪt/",
        "explanation": "Определение: a second flight where you have had to change planes. Второй сегмент перелета со сменой самолета.",
        "example": "Hurry up, we only have 45 minutes to catch our connecting flight!",
        "pronunciation_text": "connecting flight",
        "raw_original": "connecting flight /kə'nektɪŋ flaɪt/ = a second flight where you have had to change planes"
    },
    {
        "type": "vocab",
        "front": "departure lounge",
        "back": "зал ожидания вылета (зона у гейтов в аэропорту)",
        "transcription": "/dɪˈpɑː.tʃə laʊndʒ/",
        "explanation": "Определение: the place at an airport where you wait for your flight. Зал после досмотра, где пассажиры ждут посадку на рейс.",
        "example": "Passengers were asked to proceed to the departure lounge at gate 14.",
        "pronunciation_text": "departure lounge",
        "raw_original": "departure lounge /dɪ'pɑ:tʃə laʊndʒ/ = the place at an airport where you wait for your flight"
    },
    {
        "type": "vocab",
        "front": "duty-free shop",
        "back": "магазин беспошлинной торговли (дьюти-фри)",
        "transcription": "/ˌdjuː.tiˈfriː ʃɒp/",
        "explanation": "Определение: a shop in an airport or on a ship that sells goods without local taxes and duties.",
        "example": "She bought some perfume and Belgian chocolate at the airport duty-free shop.",
        "pronunciation_text": "duty-free shop",
        "raw_original": "duty-free shop /ˌdju:ti 'fri: ʃɒp/ = a shop that sells things without tax on them"
    },
    {
        "type": "vocab",
        "front": "air traveller",
        "back": "авиапассажир / авиапутешественник",
        "transcription": "/eə ˈtræv.əl.ər/",
        "explanation": "Определение: a passenger on a plane. Человек, путешествующий самолетом.",
        "example": "Frequent flight delays are a major source of stress for any air traveller.",
        "pronunciation_text": "air traveller",
        "raw_original": "air traveller /eə 'trævələ/ = a passenger on a plane"
    }
]

def main():
    added = 0
    with db.get_connection() as conn:
        cursor = conn.cursor()
        for item in NEW_CARDS:
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
