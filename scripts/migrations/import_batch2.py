import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database as db

cards_batch2 = [
    # =========================================================================
    # ДОСКА 1: media_1794166150112_9857bc93.jpg (Розовый голографический фон)
    # =========================================================================
    # 1. Good Language
    {
        "type": "good_language",
        "front": "Вспомни фразу: «срок действия визы истек / закончился»",
        "back": "visa expired",
        "example": "My tourist visa expired last week, so I had to renew it.",
        "pronunciation_text": "visa expired",
        "raw_original": "visa expired"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «номер деактивирован / отключен»",
        "back": "number is deactivated",
        "example": "Your SIM card number is deactivated due to inactivity.",
        "pronunciation_text": "number is deactivated",
        "raw_original": "number is deactivated"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «проводить время вместе»",
        "back": "spend time together",
        "example": "We love to spend time together on Sunday evenings.",
        "pronunciation_text": "spend time together",
        "raw_original": "spend time together"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «пунктуальный человек»",
        "back": "punctual person",
        "example": "He is a very punctual person who is never late for meetings.",
        "pronunciation_text": "punctual person",
        "raw_original": "punctual person"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразовый глагол: «тусить / зависать / проводить время с ним»",
        "back": "hang out with him",
        "example": "Do you want to hang out with him after work?",
        "pronunciation_text": "hang out with him",
        "raw_original": "hang out with him"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «сломанная дверь»",
        "back": "broken door",
        "example": "The carpenter came to fix the broken door.",
        "pronunciation_text": "broken door",
        "raw_original": "broken door"
    },

    # 2. Suggestions (Board 1)
    {
        "type": "suggestion",
        "front": "Как нативно сказать вместо «uses your powers» (отнимает у тебя силы / высасывает энергию)?",
        "back": "takes your strength away",
        "explanation": "В английском языке упадок сил выражается через 'takes your strength away' или 'drains your energy'.",
        "example": "❌ this argument uses your powers ➔ ✅ this argument takes your strength away.",
        "pronunciation_text": "takes your strength away",
        "raw_original": "uses your powers -> takes your strength away"
    },
    {
        "type": "suggestion",
        "front": "Как сказать правильно вместо «say help me» (попросить о помощи)?",
        "back": "ask for help",
        "explanation": "Просить о помощи — устойчивое глагольное сочетание 'to ask for help'.",
        "example": "❌ Don't be afraid to say help me ➔ ✅ Don't be afraid to ask for help.",
        "pronunciation_text": "ask for help",
        "raw_original": "say help me -> ask for help"
    },
    {
        "type": "suggestion",
        "front": "Вспомни продвинутое выражение: «суматошный / напряженный график»",
        "back": "hectic schedule",
        "explanation": "Слово 'hectic' означает суматошный, безумно занятой, полный дел.",
        "example": "Despite his hectic schedule, he finds time to study English.",
        "pronunciation_text": "hectic schedule",
        "raw_original": "hectic schedule"
    },

    # 3. Corrections (Board 1)
    {
        "type": "correction",
        "front": "Исправь слово: «under these conditionals» (при этих условиях)",
        "back": "Under these conditions",
        "explanation": "Условия договора или жизни — conditions. Слово 'conditionals' в английском означает исключительно условные предложения в грамматике.",
        "example": "❌ work in harsh conditionals ➔ ✅ work in harsh conditions.",
        "pronunciation_text": "under these conditions",
        "raw_original": "conditionals -> conditions"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «I'm staying in London one week»",
        "back": "I'm staying in London FOR one week",
        "explanation": "Продолжительность по времени требует предлога FOR: for one week, for three days.",
        "example": "❌ staying one week ➔ ✅ staying for one week.",
        "pronunciation_text": "staying for one week",
        "raw_original": "i'm staying one week -> FOR one week"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «Gemini AI is very comfortable to use»",
        "back": "Gemini AI is very convenient to use",
        "explanation": "Comfortable — физически удобный (кресло, обувь, кровать). Удобный по ситуации, функциям или времени — CONVENIENT.",
        "example": "❌ comfortable app ➔ ✅ convenient app / convenient service.",
        "pronunciation_text": "convenient",
        "raw_original": "gemini is comfortable -> convenient"
    },
    {
        "type": "correction",
        "front": "Исправь Past Simple: «yesterday she did go to the office»",
        "back": "Yesterday she went to the office",
        "explanation": "В утвердительных предложениях Past Simple используется 2-я форма глагола (went), а вспомогательный 'did' употребляется только для особого эмфатического усиления.",
        "example": "❌ she did go ➔ ✅ she went.",
        "pronunciation_text": "she went",
        "raw_original": "she did go -> she went"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «he said me the truth»",
        "back": "He told me the truth (или he said TO me)",
        "explanation": "Глагол tell требует прямого дополнения: told me. Глагол say требует предлога to: said to me. 'Said me' — грубая ошибка.",
        "example": "❌ said me ➔ ✅ told me / said to me.",
        "pronunciation_text": "told me or said to me",
        "raw_original": "said me -> TOLD me/ said TO me"
    },

    # 4. New Vocab & Stickers (Board 1)
    {
        "type": "vocab",
        "front": "to rearrange / rearrangement",
        "back": "переставлять, реорганизовать / перестановка, изменение порядка",
        "transcription": "/ˌriː.əˈreɪndʒ/ /ˌriː.əˈreɪndʒ.mənt/",
        "example": "We decided to rearrange the furniture in the living room.",
        "pronunciation_text": "to rearrange and rearrangement",
        "raw_original": "to rearrange/rearrangement"
    },
    {
        "type": "vocab",
        "front": "take apart / dismantle",
        "back": "разбирать на части / демонтировать",
        "transcription": "/teɪk əˈpɑːt/ /dɪsˈmæn.təl/",
        "example": "He had to take the engine apart to find the broken part.",
        "pronunciation_text": "take apart and dismantle",
        "raw_original": "take apart/dismantle"
    },
    {
        "type": "vocab",
        "front": "an armchair",
        "back": "кресло (с подлокотниками)",
        "transcription": "/ˈɑːm.tʃeər/",
        "example": "He sat reading in a comfortable leather armchair.",
        "pronunciation_text": "an armchair",
        "raw_original": "an armchair"
    },
    {
        "type": "vocab",
        "front": "backpack",
        "back": "рюкзак",
        "transcription": "/ˈbæk.pæk/",
        "example": "I packed my laptop and notebooks into my backpack.",
        "pronunciation_text": "backpack",
        "raw_original": "backpack"
    },
    {
        "type": "vocab",
        "front": "figure out",
        "back": "выяснить, разобраться, понять, сообразить",
        "transcription": "/ˈfɪɡ.ər aʊt/",
        "example": "It took me a while to figure out how this code works.",
        "pronunciation_text": "figure out",
        "raw_original": "figure out"
    },
    {
        "type": "vocab",
        "front": "go sightseeing",
        "back": "осматривать достопримечательности",
        "transcription": "/ɡəʊ ˈsaɪtˌsiː.ɪŋ/",
        "example": "On our first day in Paris, we decided to go sightseeing.",
        "pronunciation_text": "go sightseeing",
        "raw_original": "go sightseeing"
    },
    {
        "type": "vocab",
        "front": "a carpenter",
        "back": "плотник, столяр",
        "transcription": "/ˈkɑː.pɪn.tər/",
        "example": "The carpenter made a custom wooden dining table for us.",
        "pronunciation_text": "a carpenter",
        "raw_original": "a carpenter"
    },
    {
        "type": "vocab",
        "front": "put through (телефонный фразовый глагол)",
        "back": "соединить кого-то по телефону с кем-то (connect someone on the phone)",
        "transcription": "/pʊt θruː/",
        "explanation": "Стандартная деловая фраза при телефонном звонке: соединить со специалистом или добавочным номером.",
        "example": "Could you please put me through to Dr. Smith? / I will put you through now.",
        "pronunciation_text": "put through",
        "raw_original": "PUT THROUGH - to connect someone to another person on the phone"
    },
    {
        "type": "good_language",
        "front": "Вспомни вежливую фразу: «извините за беспокойство / извините, что отвлекаю»",
        "back": "sorry to bother you",
        "example": "Sorry to bother you, but do you have a minute to answer a question?",
        "pronunciation_text": "sorry to bother you",
        "raw_original": "sorry to bother you"
    },

    # =========================================================================
    # ДОСКА 2: media_1794166234555_15260dd6.jpg (Дата 17.06.26, Ракушки)
    # =========================================================================
    # 1. Good Language
    {
        "type": "good_language",
        "front": "Вспомни выражение: «я не вижу пользы / выгоды»",
        "back": "I don't see benefits",
        "example": "I don't see any real benefits in changing the current design.",
        "pronunciation_text": "I don't see benefits",
        "raw_original": "I don't see benefits"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «проявлять уважение»",
        "back": "show respect",
        "example": "It is crucial to show respect to your opponents in sport.",
        "pronunciation_text": "show respect",
        "raw_original": "show respect"
    },
    {
        "type": "good_language",
        "front": "Вспомни популярный неологизм: «отпуск, проведенный дома / без выезда»",
        "back": "staycation",
        "explanation": "Слово образовано от stay + vacation: отдых дома в своем городе.",
        "example": "Instead of travelling abroad this year, we had a relaxing staycation.",
        "pronunciation_text": "staycation",
        "raw_original": "staycation"
    },
    {
        "type": "good_language",
        "front": "Вспомни глагол: «принимать солнечные ванны / загорать»",
        "back": "sunbath / to sunbathe",
        "example": "Tourists love to lie on the sandy beach and sunbathe.",
        "pronunciation_text": "sunbath",
        "raw_original": "sunbath"
    },
    {
        "type": "good_language",
        "front": "Вспомни слово: «серфинг»",
        "back": "surfing",
        "example": "Surfing requires great physical endurance and balance.",
        "pronunciation_text": "surfing",
        "raw_original": "surfing"
    },
    {
        "type": "good_language",
        "front": "Вспомни слово: «морские волны»",
        "back": "waves",
        "example": "The ocean waves crashed loudly against the rocky shore.",
        "pronunciation_text": "waves",
        "raw_original": "waves"
    },
    {
        "type": "good_language",
        "front": "Вспомни прилагательное: «понятный, объяснимый»",
        "back": "understandable",
        "example": "His anger was completely understandable given the circumstances.",
        "pronunciation_text": "understandable",
        "raw_original": "understandable"
    },
    {
        "type": "good_language",
        "front": "Вспомни оборот: «что произойдет дальше»",
        "back": "what will happen next",
        "example": "Nobody can predict what will happen next in the market.",
        "pronunciation_text": "what will happen next",
        "raw_original": "what will happen next"
    },
    {
        "type": "good_language",
        "front": "Вспомни глагол: «прогнозировать, предсказывать»",
        "back": "predict",
        "example": "It is difficult to predict the exact weather for next week.",
        "pronunciation_text": "predict",
        "raw_original": "predict"
    },

    # 2. Corrections (Board 2)
    {
        "type": "correction",
        "front": "Исправь грамматику: «these files need created»",
        "back": "These files need to be created (или need creating)",
        "explanation": "После глагола need используется инфинитив в пассиве (need to be created) или герундий (need creating).",
        "example": "❌ need created ➔ ✅ need to be created / need to create.",
        "pronunciation_text": "need to be created",
        "raw_original": "need created ->"
    },
    {
        "type": "correction",
        "front": "Исправь прилагательное: «this apple is very sweety»",
        "back": "This apple is very sweet",
        "explanation": "Прилагательное 'сладкий' — sweet. Слово 'sweety' (или sweetie) — это неформальное ласковое обращение (милый, зайка).",
        "example": "❌ sweety taste ➔ ✅ sweet taste.",
        "pronunciation_text": "sweet",
        "raw_original": "sweety -> sweet"
    },
    {
        "type": "correction",
        "front": "Исправь согласование: «Emma prefer tea over coffee»",
        "back": "Emma prefers tea over coffee",
        "explanation": "Emma — 3-е лицо единственное число (she), поэтому глагол требует окончания -s: prefers.",
        "example": "❌ Emma prefer ➔ ✅ Emma prefers.",
        "pronunciation_text": "Emma prefers",
        "raw_original": "Emma prefer -> preferS"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «she participated in every activities»",
        "back": "She participated in every activity (или all the activities)",
        "explanation": "Слово every требует после себя существительное СТРОГО в единственном числе: every activity. Для множественного используется: all the activities.",
        "example": "❌ every activities ➔ ✅ every activity / all the activities.",
        "pronunciation_text": "every activity or all the activities",
        "raw_original": "every activities -> all the activities"
    },
    {
        "type": "correction",
        "front": "Исправь предлог: «I want to go to abroad this summer»",
        "back": "I want to go abroad this summer",
        "explanation": "Abroad — это наречие места ('за границу'). Перед ним предлог TO НЕ СТАВИТСЯ: go abroad, live abroad, travel abroad.",
        "example": "❌ go to abroad ➔ ✅ go abroad.",
        "pronunciation_text": "go abroad",
        "raw_original": "go to abroad -> go abroad"
    },
    {
        "type": "correction",
        "front": "Исправь сравнительную степень: «he became more strong»",
        "back": "He became stronger",
        "explanation": "Односложные прилагательные образуют сравнительную степень с помощью суффикса -er: strong ➔ stronger. Слово more не нужно.",
        "example": "❌ more strong ➔ ✅ stronger.",
        "pronunciation_text": "stronger",
        "raw_original": "more strong -> stronger"
    },

    # 3. Pronunciation (Board 2)
    {
        "type": "vocab",
        "front": "colleagues (произношение)",
        "back": "коллеги /ˈkɒl.iːɡz/ (UK) или /ˈkɑː.liːɡz/ (US)",
        "transcription": "/ˈkɒl.iːɡz/",
        "explanation": "Произносится как 'кО-лигз' (ударение на первый слог, буква u немая).",
        "example": "I discussed the project with my colleagues at work.",
        "pronunciation_text": "colleagues",
        "raw_original": "colleagues ko-leegz"
    },

    # 4. New Vocab (Board 2)
    {
        "type": "vocab",
        "front": "buzzing / bustling",
        "back": "жужжащий, оживленный, суетливый, кипящий жизнью",
        "transcription": "/ˈbʌz.ɪŋ/ /ˈbʌs.lɪŋ/",
        "explanation": "Buzzing — жужжащий (как пчела) или полный звуков/энергии. Bustling — суетливый, оживленный (о городе/улице).",
        "example": "The bee was buzzing around the flower. The market was bustling with people.",
        "pronunciation_text": "buzzing and bustling",
        "raw_original": "buzzling (buzz buzz buzz)"
    },
    {
        "type": "vocab",
        "front": "revealing (clothes)",
        "back": "откровенная, открытая, вызывающая (об одежде)",
        "transcription": "/rɪˈviː.lɪŋ/",
        "example": "She was asked not to wear such revealing clothes to the office.",
        "pronunciation_text": "revealing clothes",
        "raw_original": "revealing (clothes)"
    },
    {
        "type": "vocab",
        "front": "day off",
        "back": "выходной день, отгул",
        "transcription": "/deɪ ɒf/",
        "example": "I took a day off on Friday to travel to the mountains.",
        "pronunciation_text": "day off",
        "raw_original": "day off"
    },
    {
        "type": "vocab",
        "front": "adrenaline rush",
        "back": "прилив адреналина, всплеск адреналина",
        "transcription": "/əˈdren.əl.ɪn rʌʃ/",
        "example": "Skydiving gives you an incredible adrenaline rush.",
        "pronunciation_text": "adrenaline rush",
        "raw_original": "adrenaline rush"
    },

    # =========================================================================
    # ДОСКА 3: media_1794166241929_e698dd5a.jpg (Дата 24.06.26, Ракушки)
    # =========================================================================
    # 1. Good Language
    {
        "type": "good_language",
        "front": "Вспомни глагол в Past Simple: «прибыл, приехал»",
        "back": "arrived",
        "example": "The train arrived at the station precisely on time.",
        "pronunciation_text": "arrived",
        "raw_original": "arrived"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «около 2000 километров»",
        "back": "about 2000 km",
        "example": "The journey was about 2000 km long.",
        "pronunciation_text": "about 2000 kilometers",
        "raw_original": "about 2000 km"
    },
    {
        "type": "good_language",
        "front": "Вспомни конструкцию: «он беспокоится об этом»",
        "back": "he worries about it",
        "explanation": "Глагол to worry с предлогом about.",
        "example": "He worries about his upcoming exams every night.",
        "pronunciation_text": "he worries about it",
        "raw_original": "he worries about it"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «я встревожен / взволнован»",
        "back": "I'm worried",
        "example": "I'm worried about missing the flight tomorrow.",
        "pronunciation_text": "I'm worried",
        "raw_original": "I'm worried"
    },
    {
        "type": "good_language",
        "front": "Вспомни пару синонимов: «худой / стройный»",
        "back": "thin / slim",
        "explanation": "Thin — худой, тонкий. Slim — стройный, изящный (с позитивным оттенком).",
        "example": "She has a slim and athletic figure.",
        "pronunciation_text": "thin and slim",
        "raw_original": "thin/slim"
    },

    # 2. Suggestions (Board 3)
    {
        "type": "suggestion",
        "front": "Как нативно сказать вместо «big story» (долгая история)?",
        "back": "long story",
        "explanation": "Английская классическая идиома: 'It's a long story' (это долгая история) или 'Long story short' (короче говоря). Словосочетание 'big story' не используется.",
        "example": "❌ It's a big story ➔ ✅ It's a long story / Long story short.",
        "pronunciation_text": "long story",
        "raw_original": "big story -> long story"
    },

    # 3. Corrections (Board 3)
    {
        "type": "correction",
        "front": "Исправь ошибку: «he is very kindly to everybody»",
        "back": "He is very kind to everybody",
        "explanation": "После глагола to be нужно прилагательное: kind (добрый). Kindly — это наречие (любезно), либо устаревшее обращение.",
        "example": "❌ he is kindly ➔ ✅ he is kind.",
        "pronunciation_text": "he is kind",
        "raw_original": "kindly -> kind"
    },
    {
        "type": "correction",
        "front": "Исправь словосочетание: «the car was moving at a big speed»",
        "back": "At a high speed",
        "explanation": "Скорость в английском бывает высокой (high speed) или низкой (low speed), но никогда не 'big'!",
        "example": "❌ big speed ➔ ✅ high speed.",
        "pronunciation_text": "high speed",
        "raw_original": "big speed -> high speed"
    },
    {
        "type": "correction",
        "front": "Исправь глагол: «we need to put the injured dog to the shelter»",
        "back": "Take it to the shelter",
        "explanation": "Отвезти, доставить живое существо в приют — глагол TAKE (take to the shelter). Глагол put означает положить предмет.",
        "example": "❌ put it to the shelter ➔ ✅ take it to the shelter.",
        "pronunciation_text": "take it to the shelter",
        "raw_original": "put it to the shelter -> take it to the shelter"
    },
    {
        "type": "correction",
        "front": "Какое слово использовать для травмы человека/животного вместо «damage»?",
        "back": "Injury",
        "explanation": "Damage — это материальный ущерб неживым предметам (машине, дому). Телесное повреждение или рана живого существа — INJURY.",
        "example": "❌ dog has severe damage ➔ ✅ the dog has a severe injury.",
        "pronunciation_text": "injury",
        "raw_original": "damage -> injury"
    },
    {
        "type": "correction",
        "front": "Исправь отрицание: «I'm not care about their opinion»",
        "back": "I don't care about their opinion",
        "explanation": "Care — это смысловой глагол (заботиться, волноваться). В Present Simple отрицание строится через 'I don't care', а не 'I'm not'.",
        "example": "❌ I'm not care ➔ ✅ I don't care.",
        "pronunciation_text": "I don't care",
        "raw_original": "I'm not care -> I don't care"
    },

    # 4. New Vocab (Board 3)
    {
        "type": "vocab",
        "front": "to plant (в криминальном контексте)",
        "back": "подбросить (улику, наркотики, оружие) / сажать растения",
        "transcription": "/plɑːnt/",
        "example": "The detective realized the gun had been planted in the suspect's car.",
        "pronunciation_text": "to plant",
        "raw_original": "to plant - подбросить"
    },
    {
        "type": "vocab",
        "front": "to drop something",
        "back": "уронить что-либо (случайно или намеренно)",
        "transcription": "/drɒp/",
        "example": "Be careful not to drop that fragile glass vase.",
        "pronunciation_text": "to drop something",
        "raw_original": "to drop sth - уронить"
    },
    {
        "type": "vocab",
        "front": "a wing",
        "back": "крыло (птицы, самолета или здания)",
        "transcription": "/wɪŋ/",
        "example": "The injured pigeon could not fly because of a broken wing.",
        "pronunciation_text": "a wing",
        "raw_original": "a wing"
    },
    {
        "type": "vocab",
        "front": "to nod your head",
        "back": "кивать головой (в знак согласия)",
        "transcription": "/nɒd jɔːr hed/",
        "explanation": "Кивать (да) — nod head. Качать головой из стороны в сторону (нет) — shake head.",
        "example": "She didn't speak, but just nodded her head in agreement.",
        "pronunciation_text": "to nod your head",
        "raw_original": "to nod your head"
    },
    {
        "type": "vocab",
        "front": "a shelter",
        "back": "приют (для животных / бездомных), навес, убежище",
        "transcription": "/ˈʃel.tər/",
        "example": "We adopted a lovely rescue puppy from the local animal shelter.",
        "pronunciation_text": "a shelter",
        "raw_original": "a shelter"
    },

    # =========================================================================
    # ДОСКА 4: media_1794166296090_60f157f7.jpg (Дата 30.06.26, Ракушки)
    # =========================================================================
    # 1. Good Language
    {
        "type": "good_language",
        "front": "Вспомни фразу: «худшая / самая тяжелая проблема»",
        "back": "worst problem",
        "example": "Traffic jams are the worst problem in modern megacities.",
        "pronunciation_text": "worst problem",
        "raw_original": "worst problem"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «это мой триггер (то, что меня цепляет/злит)»",
        "back": "it's my trigger",
        "example": "Loud noise while I am trying to focus is my biggest trigger.",
        "pronunciation_text": "it's my trigger",
        "raw_original": "it's my trigger"
    },
    {
        "type": "good_language",
        "front": "Вспомни словосочетание: «базовая / основная проблема»",
        "back": "basic problem",
        "example": "The basic problem is the lack of proper communication between teams.",
        "pronunciation_text": "basic problem",
        "raw_original": "basic problem"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «гулять по моему городу»",
        "back": "walk around my city",
        "example": "I love to walk around my city in warm summer evenings.",
        "pronunciation_text": "walk around my city",
        "raw_original": "walk around my city"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «для всего человечества»",
        "back": "for humanity",
        "example": "Scientific discoveries should serve for the good of all humanity.",
        "pronunciation_text": "for humanity",
        "raw_original": "for humanity"
    },

    # 2. Suggestions (Board 4)
    {
        "type": "suggestion",
        "front": "Как сказать «остыть / освежиться в жару» вместо «to feel colder»?",
        "back": "to cool off",
        "explanation": "Фразовый глагол 'to cool off' означает охладиться, освежиться после жары.",
        "example": "❌ I jumped into the pool to feel colder ➔ ✅ I jumped into the pool to cool off.",
        "pronunciation_text": "to cool off",
        "raw_original": "to feel colder -> to cool off"
    },
    {
        "type": "suggestion",
        "front": "Как назвать иностранца вместо обобщенного «another guy»?",
        "back": "a foreigner",
        "explanation": "Человек из другой страны — a foreigner (или an expat / tourist).",
        "example": "❌ I talked to another guy on the plane ➔ ✅ I talked to a foreigner on the plane.",
        "pronunciation_text": "a foreigner",
        "raw_original": "another guy -> a foreigner"
    },

    # 3. Corrections (Board 4)
    {
        "type": "correction",
        "front": "Как называется кондиционер в помещении вместо «air cooler»?",
        "back": "Air conditioning (или AC)",
        "explanation": "Система кондиционирования воздуха — air conditioning (сокращенно AC). Air cooler — это водяной вентилятор, а не кондиционер.",
        "example": "❌ turn on the air cooler ➔ ✅ turn on the air conditioning (AC).",
        "pronunciation_text": "air conditioning",
        "raw_original": "air cooler -> air conditioning"
    },
    {
        "type": "correction",
        "front": "Исправь словосочетание: «there were crowded people on the street»",
        "back": "Crowded streets (или crowds of people)",
        "explanation": "Прилагательное crowded описывает место ('многолюдное/переполненное'): crowded streets. Сами люди — это толпы: crowds of people. 'Crowded people' не говорят.",
        "example": "❌ crowded people ➔ ✅ crowded streets / crowds of people.",
        "pronunciation_text": "crowded streets or crowds of people",
        "raw_original": "crowded people -> crowded streets / crowds of people"
    },
    {
        "type": "correction",
        "front": "Как правильно назвать Невский проспект по-английски вместо «Nevskiy street»?",
        "back": "Nevsky Prospect / avenue",
        "explanation": "Широкая главная магистраль или проспект переводится как 'avenue' или транслитерируется как 'Nevsky Prospect', но не 'street'.",
        "example": "❌ Nevskiy street ➔ ✅ Nevsky Prospect / Nevsky Avenue.",
        "pronunciation_text": "Nevsky Prospect",
        "raw_original": "Nevskiy street -> avenue"
    },
    {
        "type": "correction",
        "front": "Как сказать «авиакомпания» вместо буквального «air company»?",
        "back": "Airline",
        "explanation": "Авиакомпания, осуществляющая пассажирские перевозки — всегда AIRLINE.",
        "example": "❌ which air company do you fly with? ➔ ✅ which airline do you fly with?",
        "pronunciation_text": "airline",
        "raw_original": "air company -> airline"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «I have traveled in another countries»",
        "back": "In other countries",
        "explanation": "С множественным числом (countries) используется OTHER. Слово another (an + other) употребляется ТОЛЬКО с единственным числом (another country).",
        "example": "❌ in another countries ➔ ✅ in other countries.",
        "pronunciation_text": "in other countries",
        "raw_original": "in another countries -> in other countries"
    },
    {
        "type": "correction",
        "front": "Исправь отрицание в Past Simple: «he don't checked the ticket»",
        "back": "He didn't check the ticket",
        "explanation": "В прошедшем времени Past Simple отрицание строится через 'didn't' + базовый инфинитив без окончания: didn't check.",
        "example": "❌ he don't checked ➔ ✅ he didn't check.",
        "pronunciation_text": "he didn't check",
        "raw_original": "he don't checked -> didn't check"
    },

    # 4. Pronunciation (Board 4)
    {
        "type": "vocab",
        "front": "police (произношение)",
        "back": "полиция /pəˈliːs/",
        "transcription": "/pəˈliːs/",
        "explanation": "Ударение падает на ВТОРОЙ слог ('пэ-ЛИС'). Ни в коем случае не на первый!",
        "example": "Someone called the police immediately after the accident.",
        "pronunciation_text": "police",
        "raw_original": "police /pə'li:s/"
    },
    {
        "type": "vocab",
        "front": "foreigner (n) / foreign (adj) (произношение)",
        "back": "иностранец /ˈfɒr.ə.nər/ / иностранный /ˈfɒr.ɪn/",
        "transcription": "/ˈfɒr.ə.nər/ /ˈfɒr.ɪn/",
        "explanation": "Буква 'g' немая и НЕ произносится: 'фо-ри-нер' и 'фо-рин'.",
        "example": "She speaks three foreign languages without an accent.",
        "pronunciation_text": "foreigner and foreign",
        "raw_original": "foreigner /'fɒrənə(r)/ foreign(adj)"
    },

    # 5. New Vocab (Board 4)
    {
        "type": "vocab",
        "front": "body type",
        "back": "тип телосложения, комплекция, фигура",
        "transcription": "/ˈbɒd.i taɪp/",
        "example": "Choose clothes that fit and flatter your specific body type.",
        "pronunciation_text": "body type",
        "raw_original": "body type"
    },
    {
        "type": "vocab",
        "front": "mosquito repellent (repellent for mosquitoes)",
        "back": "репеллент, спрей / средство от комаров",
        "transcription": "/məsˈkiː.təʊ rɪˈpel.ənt/",
        "example": "Don't forget to spray mosquito repellent before going to the forest.",
        "pronunciation_text": "mosquito repellent",
        "raw_original": "repellent for mosquitoes"
    },
    {
        "type": "vocab",
        "front": "citizenship",
        "back": "гражданство, подданство",
        "transcription": "/ˈsɪt.ɪ.zən.ʃɪp/",
        "example": "He applied for dual citizenship after living in Canada for five years.",
        "pronunciation_text": "citizenship",
        "raw_original": "citizenship"
    },

    # =========================================================================
    # ДОСКА 5: media_1794166309912_a605094e.png (Желтые стикеры-паронимы)
    # =========================================================================
    {
        "type": "vocab",
        "front": "mansion",
        "back": "поместье, большой особняк, барский дом",
        "transcription": "/ˈmæn.ʃən/",
        "example": "The millionaire purchased a luxurious historic mansion outside the city.",
        "pronunciation_text": "mansion",
        "raw_original": "mansion - поместье"
    },
    {
        "type": "vocab",
        "front": "to mention",
        "back": "упоминать, ссылаться, говорить вскользь",
        "transcription": "/ˈmen.ʃən/",
        "explanation": "Не путать с mansion (особняк)! To mention — глагол упоминать (Don't mention it — Не стоит благодарности).",
        "example": "Did he mention anything about the budget in the meeting?",
        "pronunciation_text": "to mention",
        "raw_original": "to mention - упоминать"
    }
]

def run_import_batch2():
    db.init_db()
    added_count = 0
    by_type = {}

    for card in cards_batch2:
        db.add_card(card, user_id=0)
        added_count += 1
        t = card.get("type", "vocab")
        by_type[t] = by_type.get(t, 0) + 1

    # Deduplicate in case of duplicate runs
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM cards 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM cards 
        GROUP BY front, type, back
    )
    """)
    conn.commit()
    conn.close()

    stats = db.get_stats(user_id=0)
    print(f"\n[✓] Успешно добавлено новых карточек партии 2: {added_count}")
    print("По категориям новой партии:")
    for k, v in by_type.items():
        print(f"  • {k}: {v}")
    print("\nИтоговое общее состояние базы данных тренажера:")
    print(f"  📚 Всего карточек в базе: {stats['total']}")
    print(f"  ⏰ Ждут повторения: {stats['due']}")
    print(f"  Разбивка: {stats['by_type']}")

if __name__ == "__main__":
    run_import_batch2()
