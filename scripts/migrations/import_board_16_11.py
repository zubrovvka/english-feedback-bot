import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import database as db

BOARD_16_11_CARDS = [
    # --- Good Language ---
    {
        "type": "good_language",
        "front": "lost your time",
        "back": "потерял свое время (потратил время зря)",
        "transcription": "/lɒst jɔːr taɪm/",
        "explanation": "Фраза lose time (в прошедшем lost your time). Также в значении 'тратить зря' часто говорят waste your time.",
        "example": "He felt that he lost his time waiting in the wrong terminal line.",
        "pronunciation_text": "lost your time",
        "raw_original": "lost your time"
    },
    {
        "type": "good_language",
        "front": "wonderful environment",
        "back": "замечательная обстановка / прекрасное окружение",
        "transcription": "/ˈwʌn.də.fəl ɪnˈvaɪ.rən.mənt/",
        "explanation": "Отличная связка качественного прилагательного и существительного для описания атмосферы.",
        "example": "The hotel lounge offers a wonderful environment to relax before the flight.",
        "pronunciation_text": "wonderful environment",
        "raw_original": "wonderful environment"
    },
    {
        "type": "good_language",
        "front": "price can be different",
        "back": "цена может отличаться / варьироваться",
        "transcription": "/praɪs kæn bi ˈdɪf.ər.ənt/",
        "explanation": "Модальный глагол can выражает возможность: price can be different (или vary).",
        "example": "Depending on the season, the ticket price can be very different.",
        "pronunciation_text": "price can be different",
        "raw_original": "price can be different"
    },
    {
        "type": "good_language",
        "front": "another level",
        "back": "принципиально другой уровень",
        "transcription": "/əˈnʌð.ər ˈlev.əl/",
        "explanation": "Идиоматичное выражение высшей похвалы или масштаба: on another level.",
        "example": "First-class service on this airline is on a completely another level.",
        "pronunciation_text": "another level",
        "raw_original": "another level"
    },
    {
        "type": "good_language",
        "front": "look around",
        "back": "оглядеться вокруг / осмотреться",
        "transcription": "/lʊk əˈraʊnd/",
        "explanation": "Фразовый глагол look around — осматривать место или окрестности.",
        "example": "We had two hours before boarding, so we decided to look around the airport shops.",
        "pronunciation_text": "look around",
        "raw_original": "look around"
    },
    {
        "type": "good_language",
        "front": "main thing",
        "back": "главное / самое важное",
        "transcription": "/meɪn θɪŋ/",
        "explanation": "Разговорный оборот: The main thing is to stay calm.",
        "example": "The main thing is not to forget your passport and boarding pass.",
        "pronunciation_text": "main thing",
        "raw_original": "main thing"
    },
    {
        "type": "good_language",
        "front": "what you should do",
        "back": "что тебе следует сделать",
        "transcription": "/wɒt juː ʃʊd duː/",
        "explanation": "Косвенный вопрос с модальным глаголом should и прямым порядком слов.",
        "example": "Let me explain to you what you should do at passport control.",
        "pronunciation_text": "what you should do",
        "raw_original": "what you should do"
    },

    # --- Suggestions ---
    {
        "type": "suggestion",
        "front": "nervous ➔ anxious",
        "back": "тревожный, беспокойный (вместо nervous)",
        "transcription": "/ˈæŋk.ʃəs/",
        "explanation": "Nervous обычно означает кратковременное волнение перед сценой. Anxious — более глубокое беспокойство и тревожность.",
        "example": "She felt very anxious about flying during the storm.",
        "pronunciation_text": "anxious",
        "raw_original": "nervous -> anxious"
    },
    {
        "type": "suggestion",
        "front": "my tasks ➔ personal tasks / affairs",
        "back": "личные дела / дела (вместо 'my tasks')",
        "transcription": "/ˈpɜː.sən.əl tɑːsks / əˈfeəz/",
        "explanation": "Слово 'task' в англ. тяготеет к работе или Jira. Для личных житейских дел лучше: personal affairs или personal errands.",
        "example": "I need to take a day off to deal with some personal affairs.",
        "pronunciation_text": "personal affairs",
        "raw_original": "my tasks -> personal tasks / affairs"
    },

    # --- Corrections ---
    {
        "type": "correction",
        "front": "what is mean ➔ What DOES it mean?",
        "back": "что это значит?",
        "transcription": "/wɒt dʌz ɪt miːn/",
        "explanation": "ОШИБКА: Mean — обычный смысловой глагол. Вопрос в Present Simple строится со вспомогательным глаголом does: What DOES it mean? (а не 'what is mean').",
        "example": "Excuse me, what does this airport sign mean?",
        "pronunciation_text": "What does it mean?",
        "raw_original": "what is mean -> what does it mean"
    },
    {
        "type": "correction",
        "front": "prefer just sit ➔ prefer SITTING / prefer TO stay",
        "back": "предпочитаю просто сидеть",
        "transcription": "/prɪˈfɜː ˈsɪt.ɪŋ/",
        "explanation": "ОШИБКА: После глагола prefer используется либо герундий (prefer sitting without moving), либо to-инфинитив (prefer to stay). Голый инфинитив sit без to ставить нельзя!",
        "example": "During a long flight, I prefer sitting by the window rather than in the aisle.",
        "pronunciation_text": "prefer sitting without moving",
        "raw_original": "prefer just sit -> prefer sitting without moving / prefer TO stay"
    },
    {
        "type": "correction",
        "front": "possibility ➔ opportunity",
        "back": "возможность / шанс (a chance)",
        "transcription": "/ˌɒp.əˈtʃuː.nə.ti/",
        "explanation": "ОШИБКА: Possibility — теоретическая вероятность чего-то (there is a possibility of rain). Благоприятная жизненная возможность или шанс — строго OPPORTUNITY.",
        "example": "Studying abroad is a wonderful opportunity to practice English.",
        "pronunciation_text": "opportunity",
        "raw_original": "possibility -> opportunity (возможность, a chance)"
    },
    {
        "type": "correction",
        "front": "it is not matter ➔ it DOESN'T matter",
        "back": "это не имеет значения / без разницы",
        "transcription": "/ɪt ˈdʌz.ənt ˈmæt.ər/",
        "explanation": "ОШИБКА: Matter — это глагол 'иметь значение'. В Present Simple отрицание строится через doesn't: It doesn't matter (не 'it is not matter'!).",
        "example": "It doesn't matter which terminal you arrive at; the shuttle bus connects them all.",
        "pronunciation_text": "it doesn't matter",
        "raw_original": "it is not matter -> it doesn't matter"
    },
    {
        "type": "correction",
        "front": "connection flight ➔ connectING flight",
        "back": "стыковочный рейс",
        "transcription": "/kəˈnek.tɪŋ flaɪt/",
        "explanation": "ОШИБКА: Пересадочный рейс обозначается причастием connecting flight, а не существительным connection flight.",
        "example": "Our connecting flight leaves in less than an hour.",
        "pronunciation_text": "connecting flight",
        "raw_original": "connection flight -> connecting flight"
    },
    {
        "type": "correction",
        "front": "comfortable walk ➔ it's not convenient / comfortable TO walk",
        "back": "неудобно / некомфортно идти пешком",
        "transcription": "/ɪts nɒt kənˈviː.ni.ənt tuː wɔːk/",
        "explanation": "ОШИБКА: Конструкция с инфинитивом: It is not convenient/comfortable TO walk. Convenient — удобно по обстоятельствам; comfortable — удобно физически.",
        "example": "The terminal is too far away, so it's not convenient to walk there with heavy bags.",
        "pronunciation_text": "it's not convenient to walk",
        "raw_original": "comfortable walk -> it's not convenient/conf TO walk"
    },
    {
        "type": "correction",
        "front": "more cheap ➔ cheaper",
        "back": "дешевле",
        "transcription": "/ˈtʃiː.pər/",
        "explanation": "ОШИБКА: Односложные прилагательные (cheap) образуют сравнительную степень суффиксом -er: cheaper. Форма 'more cheap' — грубая грамматическая ошибка!",
        "example": "Booking flight tickets in advance is usually much cheaper.",
        "pronunciation_text": "cheaper",
        "raw_original": "more cheap -> cheaper"
    },
    {
        "type": "correction",
        "front": "really many handbag ➔ a lot of handbags / many handbags",
        "back": "очень много сумок (ручной клади)",
        "transcription": "/ə lɒt ɒv ˈhænd.bæɡz/",
        "explanation": "ОШИБКА: Handbag — исчисляемое существительное, во множественном числе handbags. 'Really many' неестественно, лучше 'a lot of handbags' или 'so many handbags'.",
        "example": "Passengers were carrying a lot of handbags into the cabin.",
        "pronunciation_text": "a lot of handbags",
        "raw_original": "really many handbag -> a lot of handbags"
    },
    {
        "type": "correction",
        "front": "go to something ➔ go somewhere",
        "back": "пойти куда-нибудь",
        "transcription": "/ɡəʊ ˈsʌm.weər/",
        "explanation": "ОШИБКА: Направление в неопределенное место выражается наречием somewhere: go somewhere (не 'go to something').",
        "example": "Let's go somewhere quiet to have a cup of coffee.",
        "pronunciation_text": "go somewhere",
        "raw_original": "go to something -> go somewhere"
    },

    # --- Pronunciation & Vocab ---
    {
        "type": "vocab",
        "front": "aisle",
        "back": "проход (между рядами кресел в самолете/кинотеатре)",
        "transcription": "/aɪl/",
        "explanation": "ФОНЕТИКА: Буква 'S' немая! Звучит в точности как 'ile' (/aɪl/), рифмуется с mile и smile.",
        "example": "Would you please step into the aisle to let me pass?",
        "pronunciation_text": "aisle",
        "raw_original": "Aisle [Sounds like ile]"
    },
    {
        "type": "vocab",
        "front": "procedure",
        "back": "процедура / порядок действий",
        "transcription": "/prəˈsiː.dʒər/",
        "explanation": "ФОНЕТИКА: UK /prəˈsiː.dʒər/, US /prəˈsiː.dʒɚ/. Буквосочетание 'dure' дает звук [dʒə].",
        "example": "Follow the standard security procedure before boarding.",
        "pronunciation_text": "procedure",
        "raw_original": "procedure /prəˈsiːdʒər/"
    },
    {
        "type": "vocab",
        "front": "aisle seat",
        "back": "место у прохода (в самолете)",
        "transcription": "/aɪl siːt/",
        "explanation": "Место в ряду кресел рядом с проходом (в отличие от window seat — место у иллюминатора).",
        "example": "I always choose an aisle seat on long flights so I can stretch my legs.",
        "pronunciation_text": "aisle seat",
        "raw_original": "aisle seat"
    },
    {
        "type": "vocab",
        "front": "long-haul flight",
        "back": "дальнемагистральный рейс (длительный перелет)",
        "transcription": "/ˌlɒŋ.hɔːl ˈflaɪt/",
        "explanation": "Рейс на большие расстояния (обычно более 6-8 часов непрерывного полета).",
        "example": "Hydration is essential during a long-haul flight across the ocean.",
        "pronunciation_text": "long-haul flight",
        "raw_original": "long-haul flight"
    },
    {
        "type": "vocab",
        "front": "arrive vs arrival",
        "back": "прибывать (глагол) vs прибытие/прилёт (существительное)",
        "transcription": "/əˈraɪv/ vs /əˈraɪ.vəl/",
        "explanation": "Грамматика: Arrive — действие ('We will arrive at noon'). Arrival — событие/факт/зона ('Everyone waited for his arrival').",
        "example": "The plane will arrive on time; you can check the arrival board.",
        "pronunciation_text": "arrive and arrival",
        "raw_original": "arrive vs arrival (verb vs noun)"
    },
    {
        "type": "vocab",
        "front": "Schengen Area / visa-requiring zone",
        "back": "Шенгенская зона / зона, требующая визы",
        "transcription": "/ˈʃeŋ.ən ˈeə.ri.ə/",
        "explanation": "Европейская зона без внутренних границ из 29 стран, для въезда в которую гражданам многих стран требуется шенгенская виза.",
        "example": "Citizens from a visa-requiring zone must hold a valid Schengen visa to travel freely.",
        "pronunciation_text": "Schengen Area",
        "raw_original": "The Schengen Area / visa-requiring zone"
    },

    # --- Stickers ---
    {
        "type": "vocab",
        "front": "give a talk",
        "back": "выступить с докладом / речью / презентацией",
        "transcription": "/ɡɪv ə tɔːk/",
        "explanation": "Коллокация с глаголом give: give a talk / give a presentation / give a speech.",
        "example": "She was invited to give a talk at an international tech conference.",
        "pronunciation_text": "give a talk",
        "raw_original": "give a talk"
    },
    {
        "type": "vocab",
        "front": "look forward to",
        "back": "ждать с нетерпением (чего-либо)",
        "transcription": "/lʊk ˈfɔː.wəd tuː/",
        "explanation": "ВАЖНО: После предлога to используется ГЕРУНДИЙ или существительное: look forward to MEETING you (не 'meet'!).",
        "example": "I look forward to our next vacation trip.",
        "pronunciation_text": "look forward to",
        "raw_original": "look forward"
    },
    {
        "type": "vocab",
        "front": "prefer having",
        "back": "предпочитать иметь / предпочитать (действие)",
        "transcription": "/prɪˈfɜː ˈhæv.ɪŋ/",
        "explanation": "Конструкция с герундием после prefer: prefer doing something (prefer having a window seat).",
        "example": "I prefer having breakfast before heading to the airport.",
        "pronunciation_text": "prefer having",
        "raw_original": "prefer having"
    },
    {
        "type": "correction",
        "front": "wait ➔ wait FOR sb/sth",
        "back": "ждать кого-то / чего-то",
        "transcription": "/weɪt fɔːr/",
        "explanation": "ОШИБКА: Глагол wait строго требует предлога FOR перед объектом: wait FOR a flight / wait FOR me (нельзя сказать 'wait me'!).",
        "example": "We had to wait for the boarding announcement for over thirty minutes.",
        "pronunciation_text": "wait for",
        "raw_original": "wait FOR"
    }
]

def main():
    added = 0
    with db.get_connection() as conn:
        cursor = conn.cursor()
        for item in BOARD_16_11_CARDS:
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
    print(f"\n[✓] Успешно добавлено новой партии: {added} карточек.")
    print(f"Итого в базе: {stats['total']} (готовы к повторению: {stats['due']})")
    print(f"Разбивка по категориям: {stats['by_type']}")

if __name__ == "__main__":
    main()
