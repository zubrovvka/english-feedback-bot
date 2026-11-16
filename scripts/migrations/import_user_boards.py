import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database as db

cards_to_add = [
    # =========================================================================
    # ДОСКА 1: media_1794166020108_34a7e009.jpg
    # =========================================================================
    # 1. New Vocab
    {
        "type": "vocab",
        "front": "definitely",
        "back": "определенно, безусловно, точно",
        "transcription": "/ˈdef.ɪ.nət.li/",
        "example": "I will definitely come to your lesson tomorrow.",
        "pronunciation_text": "definitely",
        "raw_original": "definitely - определенно"
    },
    {
        "type": "vocab",
        "front": "a rod",
        "back": "удочка (рыболовная)",
        "transcription": "/rɒd/",
        "example": "He bought a new carbon fishing rod yesterday.",
        "pronunciation_text": "a fishing rod",
        "raw_original": "a rod - удочка"
    },
    {
        "type": "vocab",
        "front": "to mean",
        "back": "означать, иметь в виду",
        "transcription": "/miːn/",
        "example": "What does this phrase mean in this context?",
        "pronunciation_text": "to mean",
        "raw_original": "to mean - обозначать что-то"
    },
    {
        "type": "vocab",
        "front": "to observe",
        "back": "наблюдать, изучать, исследовать",
        "transcription": "/əbˈzɜːv/",
        "example": "Scientists carefully observe the behavior of wild animals.",
        "pronunciation_text": "to observe",
        "raw_original": "to observe - изучать, исследовать"
    },
    {
        "type": "vocab",
        "front": "independent",
        "back": "независимый, самостоятельный",
        "transcription": "/ˌɪn.dɪˈpen.dənt/",
        "example": "She wants to be financially independent.",
        "pronunciation_text": "independent",
        "raw_original": "independent - независимый"
    },
    {
        "type": "vocab",
        "front": "independence",
        "back": "независимость, самостоятельность",
        "transcription": "/ˌɪn.dɪˈpen.dəns/",
        "example": "The country gained full independence in 1991.",
        "pronunciation_text": "independence",
        "raw_original": "independence - независимость"
    },
    {
        "type": "vocab",
        "front": "a spark",
        "back": "искра, вспышка",
        "transcription": "/spɑːk/",
        "example": "A single spark can cause a huge forest fire.",
        "pronunciation_text": "a spark",
        "raw_original": "a spark - вспышка, искра"
    },
    {
        "type": "vocab",
        "front": "generation",
        "back": "поколение",
        "transcription": "/ˌdʒen.əˈreɪ.ʃən/",
        "example": "The younger generation is very comfortable with digital technology.",
        "pronunciation_text": "generation",
        "raw_original": "generation - поколение"
    },

    # 2. Corrections (Board 1)
    {
        "type": "correction",
        "front": "Как сказать правильно: «это не для меня» (it's not to me)?",
        "back": "It's not for me",
        "explanation": "С выражением 'не для меня / не по мне' используется предлог FOR, а не to.",
        "example": "❌ it's not to me ➔ ✅ It's not for me.",
        "pronunciation_text": "It's not for me",
        "raw_original": "it's not to me -> not for me"
    },
    {
        "type": "correction",
        "front": "Как сказать: «я бы пропустил велопрогулку» (i skip bike rides)?",
        "back": "I would skip bike rides",
        "explanation": "Для выражения сослагательного наклонения или предпочтения ('я бы пропустил') нужен модальный глагол would.",
        "example": "❌ I skip bike rides ➔ ✅ I would skip bike rides.",
        "pronunciation_text": "I would skip bike rides",
        "raw_original": "i skip bike rides -> I would skip"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «I'm really like spend time outside»",
        "back": "I really like spending time outside",
        "explanation": "После глагола like ставится герундий с -ing (spending), а вспомогательный глагол to be (I'm) здесь не нужен.",
        "example": "❌ I'm really like spend ➔ ✅ I really like spending.",
        "pronunciation_text": "I really like spending",
        "raw_original": "I'm really like spend -> I like spending"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «we not good fishers»",
        "back": "We aren't good fishermen",
        "explanation": "В английском 'рыбаки' — это 'fishermen' (а не fishers), а отрицание строится через форму глагола to be (aren't).",
        "example": "❌ we not good fishers ➔ ✅ We aren't good fishermen.",
        "pronunciation_text": "We aren't good fishermen",
        "raw_original": "we not good fishers -> we aren't good fishermen"
    },
    {
        "type": "correction",
        "front": "Как правильно сказать «лучшее занятие / времяпрепровождение» вместо «best do»?",
        "back": "The best activity / pastime",
        "explanation": "Слово 'do' — это глагол. Существительное для занятия или хобби — 'activity' или красивое 'pastime'.",
        "example": "❌ best do ➔ ✅ the best activity / favorite pastime.",
        "pronunciation_text": "the best activity or pastime",
        "raw_original": "best do -> best activity/pastime"
    },
    {
        "type": "correction",
        "front": "Исправь грамматику: «she never talk to strangers»",
        "back": "She never talks to strangers",
        "explanation": "В Present Simple для третьего лица единственного числа (she / he / it) глагол всегда получает окончание -s.",
        "example": "❌ she never talk ➔ ✅ She never talks.",
        "pronunciation_text": "She never talks",
        "raw_original": "she never talk -> she never talks"
    },
    {
        "type": "correction",
        "front": "Как сказать «для понимания / чтобы понять» вместо «for understand»?",
        "back": "To understand (или for better understanding)",
        "explanation": "Цель действия в английском выражается инфинитивом 'to understand' либо предлогом for с существительным 'for understanding'.",
        "example": "❌ for understand ➔ ✅ to understand / for better understanding.",
        "pronunciation_text": "to understand for better understanding",
        "raw_original": "for understand -> to understand/ for better understanding"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «I use hard work every day»",
        "back": "I work hard every day",
        "explanation": "Работать усердно / тяжело — это устойчивое сочетание 'to work hard' (глагол + наречие).",
        "example": "❌ use hard work ➔ ✅ I work hard.",
        "pronunciation_text": "I work hard",
        "raw_original": "use hard work -> I work hard"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «he is more older than me»",
        "back": "He is older than me",
        "explanation": "Сравнительная степень коротких односложных прилагательных образуется суффиксом -er (older). Слово 'more' здесь грубая ошибка.",
        "example": "❌ more older ➔ ✅ older.",
        "pronunciation_text": "older",
        "raw_original": "more older -> older"
    },

    # 3. Good Language (Board 1)
    {
        "type": "good_language",
        "front": "Вспомни выражение: «нужно сделать покупки / пройтись по магазинам»",
        "back": "need some shopping",
        "explanation": "Удачная естественная фраза с урока: I need some shopping.",
        "example": "I really need some shopping this weekend.",
        "pronunciation_text": "need some shopping",
        "raw_original": "need some shopping"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «родной город»",
        "back": "native town / hometown",
        "explanation": "Город, где ты родился и вырос.",
        "example": "I love visiting my native town during summer holidays.",
        "pronunciation_text": "native town",
        "raw_original": "native town"
    },
    {
        "type": "good_language",
        "front": "Вспомни вводную фразу: «честно говоря / если быть честным»",
        "back": "to be honest",
        "explanation": "Отличная связующая фраза для разговорной речи.",
        "example": "To be honest, I'm a bit tired today.",
        "pronunciation_text": "to be honest",
        "raw_original": "to be honest"
    },
    {
        "type": "good_language",
        "front": "Вспомни слово: «тишина, молчание»",
        "back": "silence",
        "explanation": "Существительное тишина / безмолвие.",
        "example": "I enjoy the absolute silence of early mornings.",
        "pronunciation_text": "silence",
        "raw_original": "silence"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «новые знания»",
        "back": "new knowledge",
        "explanation": "Knowledge в английском неисчисляемое (без артикля 'a' и без окончания -s).",
        "example": "This course gave me a lot of new knowledge.",
        "pronunciation_text": "new knowledge",
        "raw_original": "new knowledge"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «схватывать / улавливать информацию на лету»",
        "back": "catch information",
        "explanation": "Живая разговорная фраза: схватывать смысл речи.",
        "example": "He can easily catch information even in fast dialogue.",
        "pronunciation_text": "catch information",
        "raw_original": "catch information"
    },
    {
        "type": "good_language",
        "front": "Вспомни глагол: «описывать, давать описание»",
        "back": "describe",
        "explanation": "Базовый глагол для характеристики предметов и людей.",
        "example": "Can you describe what the person looked like?",
        "pronunciation_text": "describe",
        "raw_original": "describe"
    },

    # 4. Suggestions (Board 1)
    {
        "type": "suggestion",
        "front": "Как сказать более естественно вместо «nature place» (загород / сельская местность)?",
        "back": "countryside",
        "explanation": "Вместо буквального перевода 'nature place' носители всегда используют слово 'countryside'.",
        "example": "❌ I love nature places ➔ ✅ I love spending weekends in the countryside.",
        "pronunciation_text": "countryside",
        "raw_original": "nature place -> countryside"
    },
    {
        "type": "suggestion",
        "front": "Как сказать продвинуто вместо «not understand» (неправильно понять / недопонять)?",
        "back": "misunderstand",
        "explanation": "Приставка mis- обозначает ошибочное действие. Misunderstand — неправильно истолковать.",
        "example": "❌ I did not understand you ➔ ✅ I misunderstood your question.",
        "pronunciation_text": "misunderstand",
        "raw_original": "not understand -> misunderstand"
    },
    {
        "type": "suggestion",
        "front": "Как сказать нативной идиомой вместо «it's not for me» (это не мое / не в моем вкусе)?",
        "back": "it's not my cup of tea",
        "explanation": "Классическая британская идиома: 'It's not my cup of tea' (букв. не моя чашка чая).",
        "example": "❌ Fishing is not for me ➔ ✅ Fishing is not really my cup of tea.",
        "pronunciation_text": "it's not my cup of tea",
        "raw_original": "not for me -> it's not my cup of tea"
    },

    # 5. Pronunciation (Board 1)
    {
        "type": "vocab",
        "front": "café (произношение)",
        "back": "кафе /ˈkæf.eɪ/ (UK) или /kæfˈeɪ/ (US)",
        "transcription": "/ˈkæf.eɪ/",
        "explanation": "Обрати внимание: на конце звучит отчетливое 'эй', ударение в US падает на второй слог.",
        "example": "Let's meet at a cozy café downtown.",
        "pronunciation_text": "café",
        "raw_original": "café UK /'kæf.eɪ/ US /kæf'eɪ/"
    },
    {
        "type": "vocab",
        "front": "thin (произношение)",
        "back": "тонкий, худой /θɪn/",
        "transcription": "/θɪn/",
        "explanation": "Глухой межзубный звук [θ] (кончик языка между зубами, как русская с, но продувая воздух).",
        "example": "He was wearing a thin jacket in cold weather.",
        "pronunciation_text": "thin",
        "raw_original": "thin /θɪn/"
    },
    {
        "type": "vocab",
        "front": "height (произношение)",
        "back": "высота, рост /haɪt/",
        "transcription": "/haɪt/",
        "explanation": "Произносится через дифтонг [aɪ] (хайт), рифмуется со словом bite, а НЕ 'хейт'!",
        "example": "What is the exact height of this building?",
        "pronunciation_text": "height",
        "raw_original": "height /haɪt/"
    },
    {
        "type": "vocab",
        "front": "nothing (произношение)",
        "back": "ничего, ничто /ˈnʌθ.ɪŋ/",
        "transcription": "/ˈnʌθ.ɪŋ/",
        "explanation": "Первый звук — краткий [ʌ] ('насинг'), а не 'нотинг'. Межзубный [θ].",
        "example": "There is nothing to worry about.",
        "pronunciation_text": "nothing",
        "raw_original": "nothing /'nʌθ.ɪŋ/"
    },

    # =========================================================================
    # ДОСКА 2: media_1794166057605_ff28afb2.png (Антонимы характера)
    # =========================================================================
    {
        "type": "vocab",
        "front": "friendly ↔ unfriendly",
        "back": "дружелюбный ↔ недружелюбный, неприветливый",
        "transcription": "/ˈfrend.li/ ↔ /ʌnˈfrend.li/",
        "example": "The hotel staff was very friendly and welcoming.",
        "pronunciation_text": "friendly and unfriendly",
        "raw_original": "friendly, unfriendly"
    },
    {
        "type": "vocab",
        "front": "talkative ↔ quiet",
        "back": "разговорчивый, болтливый ↔ тихий, молчаливый",
        "transcription": "/ˈtɔː.kə.tɪv/ ↔ /ˈkwaɪ.ət/",
        "example": "My sister is very talkative, while I am quiet.",
        "pronunciation_text": "talkative and quiet",
        "raw_original": "talkative, quiet"
    },
    {
        "type": "vocab",
        "front": "generous ↔ mean",
        "back": "щедрый, великодушный ↔ жадный, скупой (также злой)",
        "transcription": "/ˈdʒen.ər.əs/ ↔ /miːn/",
        "explanation": "В британском английском 'mean' часто означает именно 'жадный на деньги' (скупой).",
        "example": "He is very generous with his friends, but mean with strangers.",
        "pronunciation_text": "generous and mean",
        "raw_original": "generous, mean"
    },
    {
        "type": "vocab",
        "front": "kind ↔ unkind",
        "back": "добрый, участливый ↔ недобрый, черствый",
        "transcription": "/kaɪnd/ ↔ /ʌnˈkaɪnd/",
        "example": "It was very kind of you to help me with my project.",
        "pronunciation_text": "kind and unkind",
        "raw_original": "kind, unkind"
    },
    {
        "type": "vocab",
        "front": "lazy ↔ hard-working",
        "back": "ленивый ↔ трудолюбивый, прилежный",
        "transcription": "/ˈleɪ.zi/ ↔ /ˌhɑːdˈwɜː.kɪŋ/",
        "example": "He is not lazy; in fact, he is the most hard-working student.",
        "pronunciation_text": "lazy and hard-working",
        "raw_original": "lazy, hard-working"
    },
    {
        "type": "vocab",
        "front": "funny ↔ serious",
        "back": "смешной, веселый ↔ серьезный",
        "transcription": "/ˈfʌn.i/ ↔ /ˈsɪə.ri.əs/",
        "example": "She told a funny story that made everyone laugh.",
        "pronunciation_text": "funny and serious",
        "raw_original": "funny, serious"
    },
    {
        "type": "vocab",
        "front": "clever ↔ stupid",
        "back": "умный, сообразительный ↔ глупый",
        "transcription": "/ˈklev.ər/ ↔ /ˈstjuː.pɪd/",
        "example": "That was a very clever solution to the problem.",
        "pronunciation_text": "clever and stupid",
        "raw_original": "clever, stupid"
    },
    {
        "type": "vocab",
        "front": "shy ↔ extrovert",
        "back": "застенчивый, робкий ↔ экстраверт, открытый человек",
        "transcription": "/ʃaɪ/ ↔ /ˈek.strə.vɜːt/",
        "example": "As a child I was shy, but now I am an extrovert.",
        "pronunciation_text": "shy and extrovert",
        "raw_original": "shy, extrovert"
    },

    # =========================================================================
    # ДОСКА 3: media_1794166067905_075d7a40.jpg (Лунный фон)
    # =========================================================================
    # 1. New Vocab (Board 2)
    {
        "type": "vocab",
        "front": "greedy",
        "back": "жадный, ненасытный, алчный",
        "transcription": "/ˈɡriː.di/",
        "example": "Don't be greedy, leave some cake for the others.",
        "pronunciation_text": "greedy",
        "raw_original": "greedy"
    },
    {
        "type": "vocab",
        "front": "forgive the debts",
        "back": "прощать долги / списать задолженность",
        "transcription": "/fəˈɡɪv ðə dets/",
        "explanation": "Обрати внимание: в слове 'debts' буква 'b' не произносится (/dets/).",
        "example": "The bank agreed to forgive part of his debts.",
        "pronunciation_text": "forgive the debts",
        "raw_original": "forgive the debts"
    },
    {
        "type": "vocab",
        "front": "force somebody to do something",
        "back": "заставлять / принуждать кого-то делать что-то",
        "transcription": "/fɔːs/",
        "example": "Nobody can force you to do what you don't want.",
        "pronunciation_text": "force somebody to do something",
        "raw_original": "force sb to do sth"
    },
    {
        "type": "vocab",
        "front": "to procrastinate",
        "back": "прокрастинировать, откладывать важные дела на потом",
        "transcription": "/prəˈkræs.tɪ.neɪt/",
        "example": "I always procrastinate when I have to write reports.",
        "pronunciation_text": "to procrastinate",
        "raw_original": "to procrastinate"
    },
    {
        "type": "vocab",
        "front": "childlike",
        "back": "по-детски искренний, непосредственный (в хорошем смысле)",
        "transcription": "/ˈtʃaɪld.laɪk/",
        "explanation": "Childlike — чистый, искренний как ребенок. (Не путать с childish — инфантильный, капризный).",
        "example": "She looked at the fireworks with childlike wonder.",
        "pronunciation_text": "childlike",
        "raw_original": "childlike"
    },
    {
        "type": "vocab",
        "front": "sociable",
        "back": "общительный, компанейский",
        "transcription": "/ˈsəʊ.ʃə.bəl/",
        "example": "Rob is very sociable and makes friends wherever he goes.",
        "pronunciation_text": "sociable",
        "raw_original": "sociable"
    },
    {
        "type": "vocab",
        "front": "outgoing",
        "back": "открытый, коммуникабельный, инициативный в общении",
        "transcription": "/ˌaʊtˈɡəʊ.ɪŋ/",
        "example": "She has an outgoing personality and loves meeting new people.",
        "pronunciation_text": "outgoing",
        "raw_original": "outgoing"
    },
    {
        "type": "vocab",
        "front": "to gossip",
        "back": "сплетничать / сплетня, слухи",
        "transcription": "/ˈɡɒs.ɪp/",
        "example": "People in our office love to gossip about celebrities.",
        "pronunciation_text": "to gossip",
        "raw_original": "to gossip"
    },
    {
        "type": "vocab",
        "front": "chatty",
        "back": "болтливый, любящий поболтать",
        "transcription": "/ˈtʃæt.i/",
        "example": "The taxi driver was in a very chatty mood today.",
        "pronunciation_text": "chatty",
        "raw_original": "chatty"
    },
    {
        "type": "vocab",
        "front": "a chatterbox",
        "back": "болтун, болтушка, трещотка",
        "transcription": "/ˈtʃæt.ə.bɒks/",
        "example": "Her little daughter is a real chatterbox, she never stops talking.",
        "pronunciation_text": "a chatterbox",
        "raw_original": "a chatterbox"
    },
    {
        "type": "vocab",
        "front": "get on with somebody",
        "back": "ладить, хорошо уживаться с кем-то",
        "transcription": "/ɡet ɒn wɪð/",
        "example": "Do you get on well with your colleagues?",
        "pronunciation_text": "get on with somebody",
        "raw_original": "get on"
    },
    {
        "type": "vocab",
        "front": "confident",
        "back": "уверенный в себе",
        "transcription": "/ˈkɒn.fɪ.dənt/",
        "example": "He spoke in a very calm and confident voice.",
        "pronunciation_text": "confident",
        "raw_original": "confident"
    },
    {
        "type": "vocab",
        "front": "embarrassed",
        "back": "смущенный, чувствующий неловкость",
        "transcription": "/ɪmˈbær.əst/",
        "explanation": "Пишется с двумя 'r' и двумя 's' (embarrassed).",
        "example": "I felt so embarrassed when I forgot his name.",
        "pronunciation_text": "embarrassed",
        "raw_original": "embarassed"
    },
    {
        "type": "vocab",
        "front": "tiresome",
        "back": "утомительный, занудный, скучный",
        "transcription": "/ˈtaɪə.səm/",
        "explanation": "Tiresome — то, что утомляет (task, journey). Tired — тот, кто устал.",
        "example": "Filling out all these forms was a tiresome process.",
        "pronunciation_text": "tiresome",
        "raw_original": "tiresome"
    },

    # 2. Corrections (Board 2)
    {
        "type": "correction",
        "front": "Как сказать «нажать кнопку (на клавиатуре/мыши)» вместо «push button»?",
        "back": "To click (a button/mouse) / to press a key",
        "explanation": "На компьютере кликнуть мышью — to click, а нажать клавишу — to press a key.",
        "example": "❌ push button ➔ ✅ click the link / press Enter.",
        "pronunciation_text": "to click or to press a key",
        "raw_original": "push button (keyboard) -> to click"
    },
    {
        "type": "correction",
        "front": "Переведи на английский: «мы ждали целый час»",
        "back": "We have been waiting for an hour",
        "explanation": "Действие началось в прошлом и длилось до момента речи: используется Present Perfect Continuous.",
        "example": "❌ we wait hour ➔ ✅ We have been waiting for an hour.",
        "pronunciation_text": "We have been waiting for an hour",
        "raw_original": "ждали час -> we have been waiting for an hour"
    },
    {
        "type": "correction",
        "front": "Какая форма прилагательного от слова «activity» (активность)?",
        "back": "Active",
        "explanation": "Activity — существительное (деятельность). Прилагательное — active (активный).",
        "example": "❌ activity person ➔ ✅ active person.",
        "pronunciation_text": "active",
        "raw_original": "activity (adj) -> active"
    },
    {
        "type": "correction",
        "front": "Исправь грамматику: «try keep balance»",
        "back": "Try to keep balance",
        "explanation": "После глагола try с инфинитивом обязательна частица to: try to keep.",
        "example": "❌ try keep balance ➔ ✅ try to keep balance.",
        "pronunciation_text": "try to keep balance",
        "raw_original": "try keep balance -> try TO keep"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «I have many money»",
        "back": "I have much money (или a lot of money)",
        "explanation": "Деньги (money) в английском неисчисляемые, поэтому с ними употребляется much или a lot of, но ни в коем случае не many.",
        "example": "❌ many money ➔ ✅ much money / a lot of money.",
        "pronunciation_text": "much money or a lot of money",
        "raw_original": "many money -> much"
    },
    {
        "type": "correction",
        "front": "С каким предлогом употребляется «тратить деньги на что-то»?",
        "back": "Spend money ON something",
        "explanation": "Глагол spend всегда требует предлог on (тратить на).",
        "example": "❌ spend money for clothes ➔ ✅ spend money on clothes.",
        "pronunciation_text": "spend money on something",
        "raw_original": "тратить деньги -> spend money ON"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «she don't talkative»",
        "back": "She isn't talkative",
        "explanation": "Talkative — это прилагательное (болтливая). Отрицание строится с глаголом to be (isn't), а не с don't/doesn't.",
        "example": "❌ she don't talkative ➔ ✅ She isn't talkative.",
        "pronunciation_text": "She isn't talkative",
        "raw_original": "don't talkative -> she isn't"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «this long meeting is very tired»",
        "back": "This long meeting is very tiresome (tiring)",
        "explanation": "Tired — это состояние человека ('я уставший'). Предмет или ситуация, которая утомляет — tiresome или tiring.",
        "example": "❌ it's tired ➔ ✅ it's tiresome.",
        "pronunciation_text": "it's tiresome",
        "raw_original": "it's tired -> tiresome"
    },
    {
        "type": "correction",
        "front": "С каким предлогом говорят «на фотографии» (on the photo или in the photo)?",
        "back": "IN the photo",
        "explanation": "В английском языке объекты находятся 'внутри' кадра: строго IN the photo (НЕ on).",
        "example": "❌ on the photo ➔ ✅ in the photo.",
        "pronunciation_text": "in the photo",
        "raw_original": "on the photo -> IN the photo"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «only me can understand me»",
        "back": "Only I can understand myself",
        "explanation": "В роли подлежащего местоимение I ('only I can...'), а в роли направленного на себя действия — возвратное местоимение myself.",
        "example": "❌ only me can understand me ➔ ✅ Only I can understand myself.",
        "pronunciation_text": "Only I can understand myself",
        "raw_original": "only me can understand me -> myself"
    },
    {
        "type": "correction",
        "front": "Исправь существительное: «it is your choose»",
        "back": "It is your choice",
        "explanation": "Choose — это глагол (выбирать). Существительное 'выбор' — choice.",
        "example": "❌ your choose ➔ ✅ your choice.",
        "pronunciation_text": "your choice",
        "raw_original": "your choose -> your choice (noun)"
    },

    # 3. Good Language (Board 2)
    {
        "type": "good_language",
        "front": "Вспомни слово: «наставник, ментор»",
        "back": "mentor",
        "explanation": "Опытный советчик или наставник.",
        "example": "My mentor helped me adapt to the new company quickly.",
        "pronunciation_text": "mentor",
        "raw_original": "mentor"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «порекомендовать наш проект»",
        "back": "recommend our project",
        "example": "I hope you can recommend our project to your manager.",
        "pronunciation_text": "recommend our project",
        "raw_original": "recommend our project"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «держать равновесие / баланс»",
        "back": "keep balance",
        "example": "It is important to keep a healthy work-life balance.",
        "pronunciation_text": "keep balance",
        "raw_original": "keep balance"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «копить / экономить деньги»",
        "back": "save my money",
        "example": "I am trying to save my money for a summer trip.",
        "pronunciation_text": "save my money",
        "raw_original": "save my money"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «хранить молчание / соблюдать тишину»",
        "back": "keep silence",
        "example": "Everyone decided to keep silence during the speech.",
        "pronunciation_text": "keep silence",
        "raw_original": "keep silence"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «использовать всю свою силу / выкладываться на полную»",
        "back": "use my full power",
        "example": "I will use my full power to finish this project on time.",
        "pronunciation_text": "use my full power",
        "raw_original": "use my full power"
    },
    {
        "type": "good_language",
        "front": "Вспомни глагол: «выглядеть как / быть похожим»",
        "back": "look like",
        "example": "You look like your father when you smile.",
        "pronunciation_text": "look like",
        "raw_original": "look like"
    },
    {
        "type": "good_language",
        "front": "Вспомни описание волос: «короткие прямые каштановые волосы»",
        "back": "short straight brown hair",
        "explanation": "Правильный порядок прилагательных: размер (short) + форма (straight) + цвет (brown).",
        "example": "She has short straight brown hair.",
        "pronunciation_text": "short straight brown hair",
        "raw_original": "short straight brown"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «работает медсестрой / медбратом»",
        "back": "works as a nurse",
        "explanation": "Профессия с предлогом as: works as a nurse.",
        "example": "My aunt works as a nurse at the central hospital.",
        "pronunciation_text": "works as a nurse",
        "raw_original": "works as nurse"
    },
    {
        "type": "good_language",
        "front": "Вспомни вводное слово: «вероятно, пожалуй»",
        "back": "probably",
        "example": "It will probably rain later this afternoon.",
        "pronunciation_text": "probably",
        "raw_original": "probably"
    },
    {
        "type": "good_language",
        "front": "Вспомни прилагательное: «озадаченный, сбитый с толку»",
        "back": "confused",
        "example": "I got confused by all the conflicting instructions.",
        "pronunciation_text": "confused",
        "raw_original": "confused"
    },
    {
        "type": "good_language",
        "front": "Вспомни конструкцию: «кого я предпочитаю / кто мне больше нравится»",
        "back": "who I prefer",
        "example": "Out of these two candidates, here is who I prefer.",
        "pronunciation_text": "who I prefer",
        "raw_original": "who I prefer"
    },

    # 4. Suggestions (Board 2)
    {
        "type": "suggestion",
        "front": "Как мягко возразить вместо грубого «that's not true» (насколько я вижу...)?",
        "back": "as I can see",
        "explanation": "Более дипломатичная и вежливая подача мнения в разговоре.",
        "example": "❌ That's not true! ➔ ✅ As I can see, the situation is a bit different.",
        "pronunciation_text": "as I can see",
        "raw_original": "that's not true -> as I can see"
    },
    {
        "type": "suggestion",
        "front": "Какой короткий продвинутый синоним использовать вместо «because» (так как, поскольку)?",
        "back": "as",
        "explanation": "Союз 'as' отлично заменяет банальное 'because' в сложноподчиненных предложениях причины.",
        "example": "❌ Because it was late, we left ➔ ✅ As it was late, we left.",
        "pronunciation_text": "as",
        "raw_original": "because -> as"
    },

    # =========================================================================
    # ДОСКА 4: media_1794166078065_1088d988.jpg (Пионы)
    # =========================================================================
    # 1. New Vocab (Board 3)
    {
        "type": "vocab",
        "front": "suitable for",
        "back": "подходящий, годный для чего-либо",
        "transcription": "/ˈsuː.tə.bəl fɔːr/",
        "example": "This movie is not suitable for young children.",
        "pronunciation_text": "suitable for",
        "raw_original": "suitable for"
    },
    {
        "type": "vocab",
        "front": "event",
        "back": "событие, мероприятие",
        "transcription": "/ɪˈvent/",
        "example": "The sports event attracted thousands of spectators.",
        "pronunciation_text": "event",
        "raw_original": "event"
    },
    {
        "type": "vocab",
        "front": "fortunately",
        "back": "к счастью, по счастливой случайности",
        "transcription": "/ˈfɔː.tʃən.ət.li/",
        "example": "Fortunately, nobody was hurt during the storm.",
        "pronunciation_text": "fortunately",
        "raw_original": "fortunately"
    },
    {
        "type": "vocab",
        "front": "a prom",
        "back": "выпускной бал (в школе/колледже)",
        "transcription": "/prɒm/",
        "example": "She bought a gorgeous dress for her high school prom.",
        "pronunciation_text": "a prom",
        "raw_original": "a prom"
    },
    {
        "type": "vocab",
        "front": "graduation",
        "back": "окончание учебного заведения, вручение дипломов",
        "transcription": "/ˌɡrædʒ.uˈeɪ.ʃən/",
        "example": "My parents came to attend my university graduation.",
        "pronunciation_text": "graduation",
        "raw_original": "graduation"
    },
    {
        "type": "vocab",
        "front": "milkmaid",
        "back": "доярка",
        "transcription": "/ˈmɪlk.meɪd/",
        "example": "In old times, the milkmaid collected fresh milk every morning.",
        "pronunciation_text": "milkmaid",
        "raw_original": "milkmaid"
    },
    {
        "type": "vocab",
        "front": "enormous",
        "back": "огромный, громадный, колоссальный",
        "transcription": "/ɪˈnɔː.məs/",
        "example": "They lived in an enormous house with a large garden.",
        "pronunciation_text": "enormous",
        "raw_original": "enourmous"
    },

    # 2. Corrections (Board 3)
    {
        "type": "correction",
        "front": "Как сказать «у меня куча дел / завал» или «есть много вещей» вместо «it's many things»?",
        "back": "There are many things / There is a lot on my plate",
        "explanation": "Конструкция множественного числа: there are. А идиома о большой нагрузке: 'to have a lot on one's plate'.",
        "example": "❌ it's many things ➔ ✅ There are many things / I have a lot on my plate.",
        "pronunciation_text": "There are many things or there is a lot on my plate",
        "raw_original": "it's many things -> there are many things/ there is a lot on my plate"
    },
    {
        "type": "correction",
        "front": "Как сказать «поместиться / влезть в чемодан» вместо глагола «pack»?",
        "back": "To fit in (something)",
        "explanation": "Глагол to pack — это укладывать вещи. Поместиться внутрь — to fit (in a suitcase).",
        "example": "❌ all clothes will pack in my bag ➔ ✅ all clothes will fit in my bag.",
        "pronunciation_text": "to fit in something",
        "raw_original": "pack -> to fit (in sth)"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «it is mean that we are late»",
        "back": "It means that we are late",
        "explanation": "Глагол mean используется самостоятельно без глагола to be (is). Для 3-го лица: it means.",
        "example": "❌ it is mean ➔ ✅ it means.",
        "pronunciation_text": "it means",
        "raw_original": "it is mean -> it means"
    },
    {
        "type": "correction",
        "front": "Исправь фразу: «I'm spend my time wisely»",
        "back": "I spend my time wisely",
        "explanation": "В Present Simple глагол употребляется в базовой форме I spend (без вспомогательного I'm).",
        "example": "❌ I'm spend ➔ ✅ I spend.",
        "pronunciation_text": "I spend",
        "raw_original": "I'm spend -> I spend"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку согласования: «she work hard and look happy»",
        "back": "She works hard and looks happy",
        "explanation": "Подлежащее she требует окончания -s у обоих глаголов: works, looks.",
        "example": "❌ she work, look ➔ ✅ she works, looks.",
        "pronunciation_text": "she works, looks",
        "raw_original": "she work, look -> workS, lookS"
    },
    {
        "type": "correction",
        "front": "Как правильно назвать США с артиклем: «from America» или «from the USA»?",
        "back": "From the USA",
        "explanation": "С аббревиатурами стран во множественном числе или со словами States/Kingdom обязателен артикль THE: the USA, the UK.",
        "example": "❌ from America ➔ ✅ from the USA.",
        "pronunciation_text": "from the USA",
        "raw_original": "from America -> the USA"
    },
    {
        "type": "correction",
        "front": "Какая грамматика верна после глагола like: «likes to ride» или «likes riding»?",
        "back": "Оба варианта верны (likes to ride / likes riding)",
        "explanation": "Глагол like допускает как инфинитив с to (likes to ride), так и герундий (likes riding).",
        "example": "✅ She likes to ride her bike = She likes riding her bike.",
        "pronunciation_text": "likes to ride or likes riding",
        "raw_original": "likes to ride/riding"
    },

    # 3. Good Language (Board 3)
    {
        "type": "good_language",
        "front": "Вспомни слово: «багаж» (исчисляемое или нет?)",
        "back": "luggage (неисчисляемое)",
        "explanation": "Luggage — неисчисляемое существительное: нельзя сказать 'a luggage' или 'luggages'. Говорят: a piece of luggage.",
        "example": "Can you help me carry this heavy luggage?",
        "pronunciation_text": "luggage",
        "raw_original": "luggage"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «множество мероприятий / событий»",
        "back": "many events",
        "example": "There are many interesting cultural events this weekend.",
        "pronunciation_text": "many events",
        "raw_original": "many events"
    },
    {
        "type": "good_language",
        "front": "Вспомни оборот: «что мне следует сделать»",
        "back": "which I should do",
        "example": "Here is a list of tasks which I should do today.",
        "pronunciation_text": "which I should do",
        "raw_original": "which I should do"
    },
    {
        "type": "good_language",
        "front": "Вспомни слово: «рутина, установленный распорядок дня»",
        "back": "routine",
        "example": "Exercise has become an essential part of my daily routine.",
        "pronunciation_text": "routine",
        "raw_original": "routine"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «подарок / презент на конкурс»",
        "back": "present for a competition",
        "example": "We prepared a special present for the competition winner.",
        "pronunciation_text": "present for a competition",
        "raw_original": "present for competition"
    },

    # 4. Suggestions (Board 3)
    {
        "type": "suggestion",
        "front": "Как назвать ручную кладь в аэропорту вместо «hand bag»?",
        "back": "cabin luggage / carry-on bag",
        "explanation": "В контексте перелетов ручная кладь обозначается как 'cabin luggage' или 'carry-on'. Handbag — это дамская сумочка.",
        "example": "❌ hand bag ➔ ✅ cabin luggage / carry-on.",
        "pronunciation_text": "cabin luggage",
        "raw_original": "hand bag -> cabin luggage (airport setting)"
    },
    {
        "type": "suggestion",
        "front": "Как нативно сказать «в глубине души» вместо буквального «in my soul»?",
        "back": "deep down",
        "explanation": "Английская нативная идиома для внутреннего сокровенного чувства: 'deep down'.",
        "example": "❌ in my soul I knew the truth ➔ ✅ deep down I knew the truth.",
        "pronunciation_text": "deep down",
        "raw_original": "in my soul -> deep down"
    },
    {
        "type": "suggestion",
        "front": "Как красивее сказать вместо «how we cook» (то, как мы готовим)?",
        "back": "the way we cook",
        "explanation": "Конструкция 'the way + subject + verb' звучит намного естественнее в разговорной речи, чем 'how we...'.",
        "example": "❌ how we cook ➔ ✅ the way we cook.",
        "pronunciation_text": "the way we cook",
        "raw_original": "how we cook -> the way we cook"
    },

    # 5. Pronunciation (Board 3)
    {
        "type": "vocab",
        "front": "official (произношение)",
        "back": "официальный /əˈfɪʃ.əl/",
        "transcription": "/əˈfɪʃ.əl/",
        "explanation": "Звук 'ш' в середине (/ʃ/), нейтральный безударный звук 'э' в начале (/ə/).",
        "example": "We are waiting for an official announcement.",
        "pronunciation_text": "official",
        "raw_original": "official /ə'fɪʃ.əl/"
    },
    {
        "type": "vocab",
        "front": "trousers (произношение)",
        "back": "брюки, штаны /ˈtraʊ.zəz/",
        "transcription": "/ˈtraʊ.zəz/",
        "explanation": "Дифтонг [aʊ] ('трау-зерз'), озвончение [z] на конце.",
        "example": "He bought a pair of dark blue trousers.",
        "pronunciation_text": "trousers",
        "raw_original": "trouser UK /'traʊ.zə/ US /'traʊ.zɚ/"
    },
    {
        "type": "vocab",
        "front": "blouse (произношение)",
        "back": "блузка /blaʊz/ (UK) или /blaʊs/ (US)",
        "transcription": "/blaʊz/",
        "explanation": "В британском произношении звонкий [z] на конце (блауз), в американском глухой [s] (блаус).",
        "example": "She wore an elegant white silk blouse.",
        "pronunciation_text": "blouse",
        "raw_original": "blouse UK /blaʊz/ US /blaʊs/"
    },
    {
        "type": "vocab",
        "front": "jewellery / jewelry (произношение)",
        "back": "ювелирные украшения, драгоценности /ˈdʒuː.əl.ri/",
        "transcription": "/ˈdʒuː.əl.ri/",
        "explanation": "Джуэлри. В UK пишется jewellery, в US — jewelry. Всегда неисчисляемое!",
        "example": "Gold and silver jewellery was displayed in the shop window.",
        "pronunciation_text": "jewellery",
        "raw_original": "jewellery /'dʒuː.əl.ri/"
    },

    # =========================================================================
    # ДОСКА 5: media_1794166091818_c515a87e.jpg (Капли дождя + стикеры)
    # =========================================================================
    # 1. New Vocab (Board 4)
    {
        "type": "vocab",
        "front": "pitch",
        "back": "подача/презентация идеи (elevator pitch) / смола / футбольное поле",
        "transcription": "/pɪtʃ/",
        "example": "He made a brilliant three-minute business pitch to the investors.",
        "pronunciation_text": "pitch",
        "raw_original": "pitch"
    },
    {
        "type": "vocab",
        "front": "an attic",
        "back": "чердак, мансарда",
        "transcription": "/ˈæt.ɪk/",
        "example": "We store old books and vintage boxes in the attic.",
        "pronunciation_text": "an attic",
        "raw_original": "an attic"
    },
    {
        "type": "vocab",
        "front": "to hold",
        "back": "держать, удерживать в руках / проводить (встречу)",
        "transcription": "/həʊld/",
        "example": "Please hold my coffee for a second.",
        "pronunciation_text": "to hold",
        "raw_original": "to hold"
    },
    {
        "type": "vocab",
        "front": "tense",
        "back": "напряженный, натянутый / грамматическое время",
        "transcription": "/tens/",
        "example": "The atmosphere in the room was quiet and tense.",
        "pronunciation_text": "tense",
        "raw_original": "tense"
    },
    {
        "type": "vocab",
        "front": "an oven",
        "back": "духовка, печь",
        "transcription": "/ˈʌv.ən/",
        "explanation": "Произносится как 'авен' через краткий гласный [ʌ], а не через 'о'!",
        "example": "Bake the apple pie in a preheated oven for 30 minutes.",
        "pronunciation_text": "an oven",
        "raw_original": "an oven"
    },
    {
        "type": "vocab",
        "front": "genuine",
        "back": "подлинный, искренний, неподдельный",
        "transcription": "/ˈdʒen.ju.ɪn/",
        "explanation": "Произносится: 'дже-нью-ин' (ударение на первый слог).",
        "example": "She showed genuine interest in our conversation.",
        "pronunciation_text": "genuine",
        "raw_original": "genuine"
    },
    {
        "type": "vocab",
        "front": "charming",
        "back": "очаровательный, прелестный, обаятельный",
        "transcription": "/ˈtʃɑː.mɪŋ/",
        "example": "We stayed at a charming little hotel by the seaside.",
        "pronunciation_text": "charming",
        "raw_original": "charming"
    },

    # 2. Corrections (Board 4)
    {
        "type": "correction",
        "front": "Исправь ошибку: «he wearing a black coat»",
        "back": "He IS wearing a black coat",
        "explanation": "В Present Continuous обязательно нужен вспомогательный глагол to be (is/am/are).",
        "example": "❌ he wearing ➔ ✅ he is wearing.",
        "pronunciation_text": "he is wearing",
        "raw_original": "he wearing -> he IS wearing"
    },
    {
        "type": "correction",
        "front": "Как сказать «одни наручные часы» по-английски?",
        "back": "A watch",
        "explanation": "Наручные часы в единственном числе — исчисляемое существительное: 'a watch'. 'Watches' — это несколько часов.",
        "example": "❌ I bought a watches ➔ ✅ I bought a watch.",
        "pronunciation_text": "a watch",
        "raw_original": "watches (1) -> a watch"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «it is look like rain»",
        "back": "It looks like rain",
        "explanation": "Глагол look не требует вспомогательного 'is'. В Present Simple: it looks like.",
        "example": "❌ it is look like ➔ ✅ it looks like.",
        "pronunciation_text": "it looks like",
        "raw_original": "it is look like -> it looks like"
    },
    {
        "type": "correction",
        "front": "Как сказать «создать атмосферу» вместо «do atmosphere»?",
        "back": "Create an atmosphere / make an atmosphere",
        "explanation": "Атмосферу создают (create или make), но никогда не 'do'.",
        "example": "❌ do atmosphere ➔ ✅ create a cozy atmosphere.",
        "pronunciation_text": "create an atmosphere",
        "raw_original": "do atmosphere -> make/create"
    },
    {
        "type": "correction",
        "front": "С каким предлогом говорят «посмотри на эту женщину» (see on this woman)?",
        "back": "Look at this woman",
        "explanation": "Направленный взгляд выражается глаголом look с предлогом AT: look at somebody.",
        "example": "❌ see on this woman ➔ ✅ look at this woman.",
        "pronunciation_text": "look at this woman",
        "raw_original": "see on this woman -> look at this woman"
    },
    {
        "type": "correction",
        "front": "Исправь порядок слов: «the way how live modern poets»",
        "back": "The way modern poets live",
        "explanation": "В косвенных оборотах всегда прямой порядок слов: подлежащее (modern poets) + сказуемое (live).",
        "example": "❌ how live modern poets ➔ ✅ the way modern poets live.",
        "pronunciation_text": "the way modern poets live",
        "raw_original": "how live modern poets -> the way modern poets live (subject + verb + ...)"
    },

    # 3. Good Language (Board 4)
    {
        "type": "good_language",
        "front": "Вспомни фразу: «документы, которые мне нужно подать»",
        "back": "papers I need to apply",
        "example": "Here are all the papers I need to apply for the visa.",
        "pronunciation_text": "papers I need to apply",
        "raw_original": "papers I need to apply"
    },
    {
        "type": "good_language",
        "front": "Вспомни прилагательное: «запутанный, сбивающий с толку»",
        "back": "confusing",
        "example": "These new traffic rules are very confusing.",
        "pronunciation_text": "confusing",
        "raw_original": "confusing"
    },
    {
        "type": "good_language",
        "front": "Вспомни слово: «высокие каблуки / шпильки»",
        "back": "high heels",
        "example": "She doesn't like walking in high heels all day.",
        "pronunciation_text": "high heels",
        "raw_original": "high heels"
    },
    {
        "type": "good_language",
        "front": "Вспомни вводную фразу: «полагаю, мне кажется»",
        "back": "I guess",
        "example": "I guess we should call him to make sure.",
        "pronunciation_text": "I guess",
        "raw_original": "I guess"
    },
    {
        "type": "good_language",
        "front": "Вспомни выражение: «цепляющая мысль / идея»",
        "back": "catching idea",
        "example": "That is a very catching idea for our marketing campaign.",
        "pronunciation_text": "catching idea",
        "raw_original": "catching idea"
    },

    # 4. Suggestions (Board 4)
    {
        "type": "suggestion",
        "front": "Как назвать пакет для покупок вместо «package»?",
        "back": "A carry bag / shopping bag",
        "explanation": "Package — это посылка или коробка. Пакет с ручками в магазине — a shopping bag или carry bag.",
        "example": "❌ give me a package ➔ ✅ could I have a shopping bag, please?",
        "pronunciation_text": "a shopping bag or carry bag",
        "raw_original": "package -> a carry bag"
    },
    {
        "type": "suggestion",
        "front": "Как сказать «испытывать эмоции» вместо буквального «feel emotions»?",
        "back": "Experience emotions",
        "explanation": "В литературном и продвинутом английском 'испытывать эмоции' — to experience emotions.",
        "example": "❌ feel emotions ➔ ✅ experience deep emotions.",
        "pronunciation_text": "experience emotions",
        "raw_original": "feel emotions"
    },

    # 5. Pronunciation (Board 4)
    {
        "type": "vocab",
        "front": "OK (произношение)",
        "back": "окей, хорошо /ˌəʊˈkeɪ/ (UK) или /ˌoʊˈkeɪ/ (US)",
        "transcription": "/ˌəʊˈkeɪ/",
        "explanation": "Первый звук дифтонг [əʊ] / [oʊ], второй — [eɪ].",
        "example": "Is everything OK with you?",
        "pronunciation_text": "OK",
        "raw_original": "OK UK /'əʊ keɪ/ US /'oʊ keɪ/"
    },
    {
        "type": "vocab",
        "front": "modern (произношение)",
        "back": "современный /ˈmɒd.ən/ (UK) или /ˈmɑː.dɚn/ (US)",
        "transcription": "/ˈmɒd.ən/",
        "explanation": "В британском краткий о /ˈmɒd.ən/, в американском долгий а /ˈmɑː.dɚn/.",
        "example": "They bought a modern apartment in the city center.",
        "pronunciation_text": "modern",
        "raw_original": "modern UK /'mɒd.ən/ US /'mɑː.dɚn/"
    },
    {
        "type": "vocab",
        "front": "symbol (произношение)",
        "back": "символ /ˈsɪm.bəl/",
        "transcription": "/ˈsɪm.bəl/",
        "explanation": "Краткий звук [ɪ] в первом слоге: 'симбл'.",
        "example": "The dove is a universal symbol of peace.",
        "pronunciation_text": "symbol",
        "raw_original": "symbol /'sɪm.bəl/"
    },

    # 6. Стикеры на полях и вокруг доски 5
    {
        "type": "correction",
        "front": "Как при описании картины сказать «мы видим...» более нативно?",
        "back": "There is / There are",
        "explanation": "При описании иллюстраций вместо 'we can see' носители используют конструкцию наличия: 'There is a man...', 'There are two trees...'.",
        "example": "❌ We can see an old man ➔ ✅ There is an old man.",
        "pronunciation_text": "There is and there are",
        "raw_original": "we can see -> there is/there are"
    },
    {
        "type": "correction",
        "front": "Как при описании картинки сказать «он не получает удовольствия прямо сейчас»?",
        "back": "He isn't enjoying (it)",
        "explanation": "Так как мы описываем происходящее на картинке в текущий момент, используется Present Continuous (he isn't enjoying), а не Present Simple (he doesn't enjoy).",
        "example": "❌ he doesn't enjoy ➔ ✅ he isn't enjoying.",
        "pronunciation_text": "he isn't enjoying",
        "raw_original": "how it's fixed: he doesn't enjoy -> isn't enjoying"
    },
    {
        "type": "correction",
        "front": "Как сказать «на заднем плане» вместо «behind part»?",
        "back": "In the background",
        "explanation": "На заднем плане на фото или картине — 'in the background'. На переднем плане — 'in the foreground'.",
        "example": "❌ young woman behind part ➔ ✅ in the background there is a young woman.",
        "pronunciation_text": "in the background",
        "raw_original": "(a) young woman behind part -> in the background"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу для описания картинки: «в средней части / посередине»",
        "back": "in the middle (part)",
        "example": "In the middle of the picture there is a table.",
        "pronunciation_text": "in the middle",
        "raw_original": "in the middle part there is no"
    },
    {
        "type": "good_language",
        "front": "Вспомни фразу: «там пожилой мужчина, он чувствует себя нездоровым»",
        "back": "There is an old man, he is feeling ill / sick",
        "example": "There is an old man, he is feeling ill near the poet.",
        "pronunciation_text": "There is an old man, he is feeling ill",
        "raw_original": "there is an old man, he is sick/ he is feeling ill near the poet"
    },

    # 7. Карточки-памятки по предлогам места (стикеры доски 5)
    {
        "type": "vocab",
        "front": "in front of  VS  at the front of (в чем разница?)",
        "back": "in front of = СНАРУЖИ перед чем-то\nat the front of = ВНУТРИ на переднем плане",
        "explanation": "The car is in front of the building (снаружи на улице). The teacher is standing at the front of the classroom (внутри у доски).",
        "example": "Wait for me in front of the cinema. / Sit at the front of the bus.",
        "pronunciation_text": "in front of versus at the front of",
        "raw_original": "IN FRONT OF vs AT THE FRONT OF"
    },
    {
        "type": "vocab",
        "front": "above  VS  over  VS  below  VS  under (предлоги положения)",
        "back": "above = выше (без контакта)\nover = над (покрывая сверху)\nbelow = ниже\nunder = прямо под (под защитой или крышей)",
        "example": "A lamp is above the table. A blanket is over the bed. Shoes are under the bed.",
        "pronunciation_text": "above, over, below, under",
        "raw_original": "Position / place: above, over, below, under"
    },
    {
        "type": "vocab",
        "front": "Prepositions of distance: close to, near, next to, beside, by, nearby",
        "back": "close to = близко к\nnear = рядом (БЕЗ to!)\nnext to = вплотную рядом\nbeside = бок о бок, рядом\nby = у, возле\nnearby = поблизости (наречие)",
        "explanation": "Главная ошибка студентов: говорить 'near to'. Правильно: 'near my house' (без to!) или 'close to my house'.",
        "example": "He sat beside me. My office is near the station.",
        "pronunciation_text": "close to, near, next to, beside, by, nearby",
        "raw_original": "Mistaken words: Close, Near, Next to, Beside, By, Nearby"
    }
]

def run_import():
    db.init_db()
    added_count = 0
    by_type = {}
    
    for card in cards_to_add:
        card_id = db.add_card(card, user_id=0)
        added_count += 1
        t = card.get("type", "vocab")
        by_type[t] = by_type.get(t, 0) + 1

    stats = db.get_stats(user_id=0)
    print(f"\n[✓] Успешно добавлено карточек: {added_count}")
    print("По категориям добавленного:")
    for k, v in by_type.items():
        print(f"  • {k}: {v}")
    print("\nИтоговое состояние базы данных:")
    print(f"  Всего карточек: {stats['total']}")
    print(f"  Категории: {stats['by_type']}")

if __name__ == "__main__":
    run_import()
