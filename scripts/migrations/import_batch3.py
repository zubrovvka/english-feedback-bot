import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import database as db

BATCH_3_CARDS = [
    # ----------------------------------------------------
    # Изображение 11: Доска 05.09.26 (media_1794166320288_e3c86dec.jpg)
    # ----------------------------------------------------
    {
        "front": "another country",
        "back": "другая страна",
        "type": "good_language",
        "explanation": "Грамотное сочетание: another + исчисляемое существительное в единственном числе.",
        "example": "Moving to another country can be both exciting and challenging."
    },
    {
        "front": "patient people",
        "back": "терпеливые люди",
        "type": "good_language",
        "explanation": "Прилагательное patient (терпеливый). Удачное выражение для описания характера.",
        "example": "Teachers need to be very patient people."
    },
    {
        "front": "interesting experience",
        "back": "интересный опыт",
        "type": "good_language",
        "explanation": "Experience в значении 'опыт/жизненный случай' часто используется с артиклем an interesting experience.",
        "example": "Traveling alone across the mountains was an interesting experience."
    },
    {
        "front": "didn't enjoy",
        "back": "не понравилось / не получил удовольствия",
        "type": "good_language",
        "explanation": "Естественный способ сказать, что событие или фильм не понравились: I didn't enjoy it.",
        "example": "I didn't enjoy the movie because the plot was too predictable."
    },
    {
        "front": "solution",
        "back": "решение (проблемы, задачи)",
        "type": "good_language",
        "explanation": "Существительное от глагола solve. Часто с предлогом TO: a solution to the problem.",
        "example": "We finally found a simple solution to our technical issues."
    },
    {
        "front": "environment nearby you",
        "back": "окружающая вас среда / обстановка вокруг",
        "type": "good_language",
        "explanation": "Хорошая формулировка для описания пространства и атмосферы вокруг человека.",
        "example": "Pay attention to the environment nearby you when choosing an apartment."
    },
    {
        "front": "outdoor",
        "back": "на открытом воздухе / на улице",
        "type": "good_language",
        "explanation": "Outdoor (прилагательное) — происходящий снаружи помещений (outdoor activities / outdoor cafe).",
        "example": "We prefer outdoor sports during the warm summer months."
    },
    {
        "front": "we ask staff",
        "back": "мы спрашиваем персонал / сотрудников",
        "type": "good_language",
        "explanation": "Staff — неисчисляемое собирательное существительное (персонал, сотрудники).",
        "example": "Whenever you are lost in the hotel, ask the staff for help."
    },
    {
        "front": "another level",
        "back": "другой уровень / принципиально новый уровень",
        "type": "good_language",
        "explanation": "Отличная идиоматическая фраза: take something to another level.",
        "example": "Her new project is on a completely another level of quality."
    },
    {
        "front": "in late evening",
        "back": "поздним вечером",
        "type": "good_language",
        "explanation": "Удачный временной маркер: in the late evening / late in the evening.",
        "example": "I usually enjoy reading books in late evening when it is quiet."
    },
    {
        "front": "it needs some time ➔ it requires some time",
        "back": "требуется некоторое время",
        "type": "suggestion",
        "explanation": "Require звучит более профессионально, точно и зрело в деловом и продвинутом английском.",
        "example": "This migration is complex, so it requires some time to test thoroughly."
    },
    {
        "front": "it's a hard question ➔ it's a tough question",
        "back": "это сложный / каверзный вопрос",
        "type": "suggestion",
        "explanation": "В живой речи носители для сложных, требующих размышлений вопросов говорят 'tough question'.",
        "example": "That is a tough question, let me think about it for a second."
    },
    {
        "front": "summer was quickly ➔ it was fast / time flew by",
        "back": "лето прошло быстро / пролетело",
        "type": "correction",
        "explanation": "ОШИБКА: quickly — это наречие (отвечает на вопрос 'как?'). После was нужно прилагательное (it was fast) или глагол (summer went by quickly / time flew by).",
        "example": "This summer went by so quickly, it was really fast."
    },
    {
        "front": "usually situation ➔ usual situation",
        "back": "обычная ситуация / привычное дело",
        "type": "correction",
        "explanation": "ОШИБКА: usually — это наречие ('обычно'). Перед существительным situation требуется прилагательное usual.",
        "example": "Traffic jams during rush hour are a usual situation in our city."
    },
    {
        "front": "Пекин ➔ Beijing",
        "back": "Пекин (столица Китая на английском)",
        "type": "correction",
        "explanation": "По-английски Пекин пишется и произносится как Beijing (/beɪˈdʒɪŋ/).",
        "example": "He had a business flight to Beijing last week."
    },
    {
        "front": "two travellings ➔ two journeys / two trips",
        "back": "два путешествия / две поездки",
        "type": "correction",
        "explanation": "ОШИБКА: Travel — неисчисляемое общее понятие. Отдельные конкретные поездки — это trips или journeys.",
        "example": "We took two trips abroad this year."
    },
    {
        "front": "wait my friends ➔ wait FOR my friends",
        "back": "ждать друзей",
        "type": "correction",
        "explanation": "ОШИБКА: Глагол wait требует предлога for перед объектом ожидания (wait for somebody/something). Сравните с await (без предлога).",
        "example": "I'm standing near the subway entrance waiting for my friends."
    },
    {
        "front": "I'm live here ➔ I'm living here / I live here",
        "back": "я живу здесь",
        "type": "correction",
        "explanation": "ОШИБКА: Нельзя ставить 'am' вместе с базовым глаголом в Present Simple. Либо постоянный факт: 'I live here', либо временный: 'I am living here'.",
        "example": "I live here with my family permanently."
    },
    {
        "front": "do study ➔ study / do some studying",
        "back": "учиться / заниматься учебой",
        "type": "correction",
        "explanation": "ОШИБКА: Калька с русского. В английском study сам по себе полноценный глагол: 'I need to study', а не 'do study'.",
        "example": "I need to study every evening to prepare for the IELTS exam."
    },
    {
        "front": "international students ➔ foreign students / foreigners",
        "back": "иностранные студенты / иностранцы",
        "type": "correction",
        "explanation": "Когда говорим о людях из других стран, обычно используется foreign students или просто foreigners.",
        "example": "Many foreign students study medicine at this university."
    },
    {
        "front": "feel yourself good ➔ feel good / feel well",
        "back": "чувствовать себя хорошо",
        "type": "correction",
        "explanation": "ОШИБКА: В русском 'чувствовать себя', но в английском feel уже означает 'чувствовать себя'. 'Feel yourself' означает трогать себя физически!",
        "example": "After a good night's sleep, I feel really good."
    },
    {
        "front": "we was ➔ we were",
        "back": "мы были",
        "type": "correction",
        "explanation": "ОШИБКА: Согласование местоимения множественного числа во времени Past Simple: We were (не was).",
        "example": "We were very excited to see our old classmates."
    },
    {
        "front": "how I feel ➔ the way I feel",
        "back": "то, как я себя чувствую / мои ощущения",
        "type": "correction",
        "explanation": "Вместо буквальной конструкции 'how I feel' в качестве подлежащего естественнее использовать 'the way I feel'.",
        "example": "The way I feel about this job has completely changed."
    },
    {
        "front": "calm",
        "back": "спокойный / спокойствие [произношение: /kɑːm/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Буква 'L' немая! Звучит как 'kahm', рифмуется с palm и balm.",
        "example": "Stay calm and do not panic during an emergency."
    },
    {
        "front": "Chinese",
        "back": "китайский / китаец [произношение: /tʃaɪˈniːz/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Ударение на второй слог: chai·neez.",
        "example": "She is learning Chinese and loves Cantonese cuisine."
    },
    {
        "front": "choir",
        "back": "хор [произношение: /ˈkwaɪ.ər/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Читается как 'kwai·ur' (похоже на acquire без 'a-'), ни в коем случае не через 'ч'!",
        "example": "He sings tenor in a church choir."
    },

    # ----------------------------------------------------
    # Изображение 12: Доска 14.09.26 (media_1794166329623_24657a4f.jpg)
    # ----------------------------------------------------
    {
        "front": "for myself",
        "back": "для себя",
        "type": "good_language",
        "explanation": "Возвратное местоимение myself в предложной фразе.",
        "example": "I bought this new coffee machine purely for myself."
    },
    {
        "front": "I will do",
        "back": "я сделаю (это)",
        "type": "good_language",
        "explanation": "Четкое обещание или спонтанное решение через Future Simple: I'll do it.",
        "example": "Don't worry about the report, I will do it first thing tomorrow."
    },
    {
        "front": "suddenly",
        "back": "внезапно / вдруг",
        "type": "good_language",
        "explanation": "Наречие внезапности, оживляющее повествование.",
        "example": "Suddenly, the lights went off and the music stopped."
    },
    {
        "front": "Head of Department",
        "back": "руководитель отдела / заведующий кафедрой",
        "type": "good_language",
        "explanation": "Официальная должность в компании или университете.",
        "example": "The Head of Department approved our new budget yesterday."
    },
    {
        "front": "skills, ability",
        "back": "навыки, способности",
        "type": "good_language",
        "explanation": "Отличная связка терминов для резюме и профессионального общения.",
        "example": "He demonstrated outstanding analytical skills and ability to lead."
    },
    {
        "front": "earn my money",
        "back": "зарабатывать свои деньги (честным трудом)",
        "type": "good_language",
        "explanation": "Earn money — зарабатывать трудом. (В гейминг-сленге также шутливо говорят 'farm money').",
        "example": "I prefer to earn my money independently and not depend on anyone."
    },
    {
        "front": "approve",
        "back": "одобрять / утверждать",
        "type": "good_language",
        "explanation": "Глагол: approve something (утвердить документ) или approve of something (одобрять чье-то поведение).",
        "example": "The manager needs to approve the design before we start coding."
    },
    {
        "front": "available",
        "back": "доступный / свободный",
        "type": "good_language",
        "explanation": "Ключевое слово для встреч и наличия товаров/ресурсов.",
        "example": "Are you available for a quick call at 3 PM?"
    },
    {
        "front": "good connection",
        "back": "хорошая связь / хороший контакт",
        "type": "good_language",
        "explanation": "Используется как о качестве связи (Wi-Fi/телефон), так и о взаимопонимании между людьми.",
        "example": "We have a very good internet connection in our new office."
    },
    {
        "front": "mid, late autumn",
        "back": "середина осени, поздняя осень",
        "type": "good_language",
        "explanation": "Естественный способ указания времени года: early/mid/late autumn.",
        "example": "In late autumn, trees lose all their colorful leaves."
    },
    {
        "front": "I think so",
        "back": "я думаю, что да / полагаю, что так",
        "type": "good_language",
        "explanation": "Идиоматичный краткий ответ подтверждения (вместо неуклюжего 'I think yes').",
        "example": "'Is the meeting still happening?' — 'I think so.'"
    },
    {
        "front": "organizate ➔ organize",
        "back": "организовывать",
        "type": "correction",
        "explanation": "ОШИБКА: Слова 'organizate' не существует в английском! Правильный глагол — organize (UK: organise).",
        "example": "We need to organize the files before the client meeting."
    },
    {
        "front": "back week ➔ last week",
        "back": "на прошлой неделе",
        "type": "correction",
        "explanation": "ОШИБКА: 'Back week' — калька. Прошлая неделя — это строго LAST week.",
        "example": "I submitted the project report last week."
    },
    {
        "front": "I try go to my work ➔ try TO go to my work",
        "back": "стараюсь / пытаюсь пойти на работу",
        "type": "correction",
        "explanation": "ОШИБКА: Глагол try перед инфинитивом требует частицы TO: try TO do something.",
        "example": "I try to go to work early to avoid heavy morning traffic."
    },
    {
        "front": "need understand ➔ need TO understand",
        "back": "нужно / необходимо понять",
        "type": "correction",
        "explanation": "ОШИБКА: После глагола need перед действием ставится частица TO (need to do sth).",
        "example": "You need to understand the basic concepts before moving to advanced topics."
    },
    {
        "front": "more cold ➔ colder",
        "back": "холоднее",
        "type": "correction",
        "explanation": "ОШИБКА: Односложные прилагательные образуют сравнительную степень с помощью суффикса -er: cold ➔ colder (не 'more cold').",
        "example": "It gets much colder at night in November."
    },
    {
        "front": "I'm disappoint ➔ I'm disappointed",
        "back": "я разочарован",
        "type": "correction",
        "explanation": "ОШИБКА: Disappoint — это глагол 'разочаровывать'. Состояние человека — причастие disappointed (разочарованный).",
        "example": "I am deeply disappointed with the test results."
    },
    {
        "front": "focus in ➔ focus ON sth",
        "back": "сосредоточиться на чем-то",
        "type": "correction",
        "explanation": "ОШИБКА: Устойчивый предлог при глаголе focus — всегда ON (focus on details/goals).",
        "example": "Please focus on your main priorities today."
    },
    {
        "front": "course",
        "back": "курс / блюдо [произношение: UK /kɔːs/, US /kɔːrs/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Гласный звук долгий [ɔː]. Означает как учебный курс, так и смену блюд (main course).",
        "example": "I enrolled in an online English language course."
    },
    {
        "front": "wholeheartedly",
        "back": "всем сердцем, искренне, от всей души (/ˌhəʊlˈhɑː.tɪd.li/)",
        "type": "vocab",
        "explanation": "Наречие от wholehearted (целостный, искренний).",
        "example": "I wholeheartedly agree with your proposal."
    },
    {
        "front": "deputy head / chief",
        "back": "заместитель начальника / замруководителя",
        "type": "vocab",
        "explanation": "Deputy — заместитель должностного лица (deputy director, deputy chief).",
        "example": "The deputy chief took charge of the department while the boss was away."
    },
    {
        "front": "loan",
        "back": "займ, кредит, ссуда (/ləʊn/)",
        "type": "vocab",
        "explanation": "Финансовый инструмент: taking out a loan (взять кредит) / bank loan.",
        "example": "They took out a bank loan to buy their first home."
    },
    {
        "front": "branch",
        "back": "филиал, отделение (в офисе/банке) / ветка",
        "type": "vocab",
        "explanation": "Используется для подразделений компаний (branch office) и веток деревьев/гита.",
        "example": "Our company just opened a new branch in Berlin."
    },
    {
        "front": "cozy",
        "back": "уютный, теплый, комфортный (/ˈkəʊ.zi/)",
        "type": "vocab",
        "explanation": "Британское написание cosy, американское cozy. Означает ощущение тепла, безопасности и комфорта.",
        "example": "This small café feels so cozy on a rainy autumn day."
    },
    {
        "front": "master's degree",
        "back": "степень магистра / магистратура",
        "type": "vocab",
        "explanation": "Академическая степень после бакалавриата (обычно 1-2 года учебы).",
        "example": "She decided to get a master's degree in computer science."
    },
    {
        "front": "defend thesis",
        "back": "защищать диплом / диссертацию",
        "type": "vocab",
        "explanation": "Устойчивое академическое выражение: defend one's thesis / dissertation.",
        "example": "He will defend his master's thesis next Tuesday."
    },
    {
        "front": "puddle",
        "back": "лужа (/ˈpʌd.əl/)",
        "type": "vocab",
        "explanation": "Небольшое скопление воды на дороге или тротуаре после дождя.",
        "example": "The child jumped right into the middle of the puddle."
    },

    # ----------------------------------------------------
    # Изображение 13: Доска 20.09.26 (media_1794166351203_795898c5.jpg)
    # ----------------------------------------------------
    {
        "front": "association",
        "back": "ассоциация / объединение",
        "type": "good_language",
        "explanation": "Существительное association (/əˌsəʊ.siˈeɪ.ʃən/).",
        "example": "What is your first association with this image?"
    },
    {
        "front": "awful film",
        "back": "ужасный фильм",
        "type": "good_language",
        "explanation": "Awful — сильное эмоциональное прилагательное (terrible, very bad).",
        "example": "That was an awful film, we left the cinema halfway through."
    },
    {
        "front": "magazines",
        "back": "журналы",
        "type": "good_language",
        "explanation": "Ложный друг переводчика: magazine — это периодический иллюстрированный журнал (не магазин!).",
        "example": "She loves reading fashion magazines during flights."
    },
    {
        "front": "I can guess",
        "back": "могу догадаться / предполагаю",
        "type": "good_language",
        "explanation": "Вежливая фраза предположения в диалоге.",
        "example": "I can guess why he decided not to come to the party."
    },
    {
        "front": "read news",
        "back": "читать новости",
        "type": "good_language",
        "explanation": "Обратите внимание: news в английском грамматически ВСЕГДА единственного числа (The news is good).",
        "example": "I prefer to read the news online every morning."
    },
    {
        "front": "find job",
        "back": "найти работу (find a job)",
        "type": "good_language",
        "explanation": "Job — исчисляемое (find A job), а work — неисчисляемое (find work).",
        "example": "It took him only two weeks to find a great job in IT."
    },
    {
        "front": "on the tree",
        "back": "на дереве (на ветках)",
        "type": "good_language",
        "explanation": "Плоды и листья растут ON the tree; птицы и белки часто сидят IN the tree.",
        "example": "Apples were hanging ripe on the tree."
    },
    {
        "front": "was taken",
        "back": "был занят / был сделан (снимок)",
        "type": "good_language",
        "explanation": "Пассивный залог: The seat was taken (место было занято) или The photo was taken.",
        "example": "Excuse me, this seat was taken a few minutes ago."
    },
    {
        "front": "great ➔ amazing, unbelievable",
        "back": "потрясающий, невероятный (замена слову great)",
        "type": "suggestion",
        "explanation": "Слово 'great' часто перегружено. Для яркой речи используйте сильные синонимы: amazing, unbelievable, stunning.",
        "example": "The concert was truly amazing, an unbelievable experience!"
    },
    {
        "front": "love ➔ fall in love (fall - fell - fallen)",
        "back": "влюбиться",
        "type": "suggestion",
        "explanation": "Различие: love — состояние (любить), а fall in love — процесс возникновения чувства (влюбиться).",
        "example": "They fell in love the first day they met in Florence."
    },
    {
        "front": "walk ➔ go for a walk",
        "back": "пойти на прогулку / прогуляться",
        "type": "suggestion",
        "explanation": "Вместо сухого одиночного глагола walk носители предпочитают идиому 'go for a walk'.",
        "example": "Let's go for a walk in the park while the weather is fine."
    },
    {
        "front": "strange people ➔ weird people",
        "back": "странные люди (с причудами / необычные)",
        "type": "correction",
        "explanation": "Разница: strange — незнакомый или непонятный; weird — со странностями, чудаковатый.",
        "example": "He has a weird sense of humor that not everyone understands."
    },
    {
        "front": "she loved him ➔ she fell in love with him",
        "back": "она влюбилась в него",
        "type": "correction",
        "explanation": "ОШИБКА: 'She loved him' описывает факт любви в прошлом, а если речь идет о моменте зарождения чувств — 'she fell in love with him'.",
        "example": "As soon as they started talking, she fell in love with him."
    },
    {
        "front": "moved on Paris ➔ moved TO Paris",
        "back": "переехал в Париж",
        "type": "correction",
        "explanation": "ОШИБКА: Направление движения при переезде требует предлога TO (move to Paris/London/Canada). 'Move on' значит двигаться дальше по жизни.",
        "example": "She packed her bags and moved to Paris for work."
    },
    {
        "front": "many think about it ➔ I thought about it many times",
        "back": "я думал об этом много раз",
        "type": "correction",
        "explanation": "ОШИБКА: Нарушение структуры предложения. 'Many times' — это обстоятельство частотности, глагол — thought.",
        "example": "I thought about it many times before making my final decision."
    },
    {
        "front": "nature ➔ natural",
        "back": "естественный (прилагательное)",
        "type": "correction",
        "explanation": "ОШИБКА: Nature — существительное ('природа'). Если нужно описать качество ('естественный, натуральный'), используем прилагательное natural.",
        "example": "Honey is a natural alternative to refined sugar."
    },
    {
        "front": "agency",
        "back": "агентство [произношение: UK /ˈeɪ.dʒən.si/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Ударение на первый дифтонг 'ei': /ˈeɪ.dʒən.si/.",
        "example": "She hired a creative agency to redesign her website."
    },
    {
        "front": "south",
        "back": "юг [произношение: UK /saʊθ/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Существительное south оканчивается на глухой звук [θ]. (Но в southern произносится /ˈsʌð.ən/!).",
        "example": "Birds fly to the south in autumn."
    },
    {
        "front": "although",
        "back": "хотя, несмотря на то что [произношение: UK /ɔːlˈðəʊ/, US /ɑːlˈðoʊ/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Звонкий межзубный [ð] в середине, gh не читается. Союз уступки.",
        "example": "Although it was raining, they went for a hike."
    },
    {
        "front": "sign",
        "back": "знак / вывеска / подписывать [произношение: /saɪn/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Буква 'g' не читается, гласная дает долгий дифтонг [aɪ].",
        "example": "Please sign your name at the bottom of the page."
    },
    {
        "front": "nature",
        "back": "природа [произношение: UK /ˈneɪ.tʃər/, US /ˈneɪ.tʃɚ/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Первый слог звучит как 'nei', сочетание ture дает [tʃə(r)].",
        "example": "Spending time in nature helps reduce mental stress."
    },
    {
        "front": "decade",
        "back": "десятилетие (период в 10 лет)",
        "type": "vocab",
        "explanation": "Отрезок времени в десять лет (/ˈdek.eɪd/).",
        "example": "Over the past decade, technology has completely transformed our daily lives."
    },
    {
        "front": "a couple",
        "back": "пара (два человека / несколько предметов)",
        "type": "vocab",
        "explanation": "Может означать как пару людей в отношениях (they are a cute couple), так и 'a couple of' (пара-тройка).",
        "example": "We spent a couple of hours discussing the project."
    },
    {
        "front": "a squirrel",
        "back": "белка (/ˈskwɪr.əl/)",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Сложное для произношения слово: 'skwir-rel'.",
        "example": "A fluffy squirrel was collecting acorns in the garden."
    },
    {
        "front": "stroke one's ego",
        "back": "льстить кому-то / тешить чье-то самолюбие (поглаживать эго)",
        "type": "vocab",
        "explanation": "Идиома: хвалить человека исключительно ради того, чтобы поднять его самооценку и сделать приятное.",
        "example": "I didn't give him that compliment just to stroke his ego."
    },
    {
        "front": "feed one's ego",
        "back": "подкармливать эго / подпитывать самолюбие",
        "type": "vocab",
        "explanation": "Идиома: совершать поступки ради удовлетворения собственного тщеславия и гордости.",
        "example": "Winning that minor award was just a way to feed his ego."
    },

    # ----------------------------------------------------
    # Изображение 14: Доска 28.09.26 (media_1794166369137_08329f78.jpg)
    # ----------------------------------------------------
    {
        "front": "get salary",
        "back": "получать зарплату",
        "type": "good_language",
        "explanation": "Salary — фиксированная ежемесячная зарплата (в отличие от wage — почасовой оплаты).",
        "example": "Employees get their salary on the last Friday of each month."
    },
    {
        "front": "it means that",
        "back": "это значит / означает, что...",
        "type": "good_language",
        "explanation": "Отличная вводная связка для формулирования выводов в речи.",
        "example": "If the test passes, it means that the bug has been resolved."
    },
    {
        "front": "with weight",
        "back": "с весом / весомо",
        "type": "good_language",
        "explanation": "Выражение используется для тренировок с отягощениями (exercise with weight) или весомых аргументов.",
        "example": "He prefers training with weights rather than cardio exercises."
    },
    {
        "front": "manage my time",
        "back": "управлять своим временем",
        "type": "good_language",
        "explanation": "Фраза тайм-менеджмента: manage one's time effectively.",
        "example": "Working from home taught me how to manage my time much better."
    },
    {
        "front": "include me",
        "back": "включить меня (в список/команду)",
        "type": "good_language",
        "explanation": "Глагол include (включать, содержать в себе).",
        "example": "Please include me in the email thread about the new release."
    },
    {
        "front": "improve this situation",
        "back": "улучшить эту ситуацию",
        "type": "good_language",
        "explanation": "Устойчивая сильная коллокация: improve the situation.",
        "example": "We need immediate measures to improve this situation."
    },
    {
        "front": "crash place",
        "back": "место аварии / место крушения",
        "type": "good_language",
        "explanation": "Crash site / crash place — локация, где произошло ДТП или падение.",
        "example": "Police officers cordoned off the entire crash place."
    },
    {
        "front": "thesis",
        "back": "диссертация / дипломная работа / тезис",
        "type": "good_language",
        "explanation": "Ударение на первый слог: /ˈθiː.sɪs/. Множественное число: theses (/ˈθiː.siːz/).",
        "example": "She is writing her doctoral thesis on artificial intelligence."
    },
    {
        "front": "without joke ➔ jokes aside",
        "back": "шутки в сторону / кроме шуток",
        "type": "suggestion",
        "explanation": "Калька 'without joke' звучит неестественно. Носители всегда говорят 'jokes aside' или 'all joking aside'.",
        "example": "Jokes aside, we really need to finish this feature before tomorrow."
    },
    {
        "front": "discus (a noun) ➔ discussion",
        "back": "обсуждение / дискуссия",
        "type": "correction",
        "explanation": "ОШИБКА: Discus — это легкоатлетический спортивный снаряд (диск для метания!). Существительное от discuss — DISCUSSION.",
        "example": "We had a long and productive discussion about the architecture."
    },
    {
        "front": "it should be happen ➔ it should have happened",
        "back": "это должно было произойти (в прошлом)",
        "type": "correction",
        "explanation": "ОШИБКА: Для действия, которое должно было случиться в прошлом, используется модальная конструкция should + have + V3.",
        "example": "The fix was urgent; it should have happened weeks ago."
    },
    {
        "front": "try earn ➔ try TO earn",
        "back": "пытаться заработать",
        "type": "correction",
        "explanation": "ОШИБКА: После try инфинитив обязательно требует частицы TO: try to earn.",
        "example": "They try to earn extra income by freelancing on weekends."
    },
    {
        "front": "it's not protect ➔ it doesn't protect me",
        "back": "это меня не защищает",
        "type": "correction",
        "explanation": "ОШИБКА: Отрицание в Present Simple для обычных смысловых глаголов строится через doesn't + V1 (не через is not).",
        "example": "This cheap antivirus software doesn't protect your computer against modern malware."
    },
    {
        "front": "rarely ill ➔ rare illness",
        "back": "редкая болезнь / редкое заболевание",
        "type": "correction",
        "explanation": "ОШИБКА: Ill — это предикативное прилагательное ('больной'), rarely — наречие. Существительное — illness с прилагательным: a rare illness.",
        "example": "He was diagnosed with a very rare illness."
    },
    {
        "front": "in next week ➔ next week",
        "back": "на следующей неделе",
        "type": "correction",
        "explanation": "ОШИБКА: Перед словами next / last / this / every предлоги времени (in, on, at) НЕ ставятся!",
        "example": "Our team will release the update next week."
    },
    {
        "front": "break through the wall",
        "back": "пробить стену / преодолеть преграду",
        "type": "vocab",
        "explanation": "Метафорическое или буквальное преодоление непреодолимого барьера.",
        "example": "With persistent effort, you will finally break through the wall of difficulties."
    },
    {
        "front": "for ages",
        "back": "целую вечность / очень долго",
        "type": "vocab",
        "explanation": "Идиоматическое выражение: haven't seen you for ages (сто лет тебя не видел!).",
        "example": "I have been waiting for the bus for ages."
    },
    {
        "front": "to plant",
        "back": "подбросить (улику, вещь) / сажать (растение)",
        "type": "vocab",
        "explanation": "В детективном и юридическом контексте 'plant evidence' означает тайно подбросить ложную улику.",
        "example": "The corrupt officer tried to plant false evidence in his car."
    },
    {
        "front": "outerwear",
        "back": "верхняя одежда (куртки, пальто, пуховики)",
        "type": "vocab",
        "explanation": "Собирательное понятие: coats, jackets, parkas, puffers.",
        "example": "Don't forget warm outerwear, the wind outside is freezing."
    },
    {
        "front": "stomachache",
        "back": "боль в животе / в желудке (/ˈstʌm.ək.eɪk/)",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Сочетание ache произносится как [eɪk].",
        "example": "Eating too much spicy food gave him a terrible stomachache."
    },
    {
        "front": "stomach",
        "back": "живот / желудок (/ˈstʌm.ək/)",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Окончание -ch произносится как глухой [k] (/ˈstʌm.ək/), а не 'ч'.",
        "example": "Lie down on your stomach and relax your back."
    },

    # ----------------------------------------------------
    # Изображение 15: Доска (media_1794166388444_b6bb1e4e.jpg)
    # ----------------------------------------------------
    {
        "front": "set up your server",
        "back": "настроить свой сервер",
        "type": "good_language",
        "explanation": "Фразовый глагол set up — настраивать, устанавливать конфигурацию.",
        "example": "It took him only an hour to set up a Linux server for the web app."
    },
    {
        "front": "achievement",
        "back": "достижение / успех",
        "type": "good_language",
        "explanation": "Существительное от achieve (/əˈtʃiːv.mənt/).",
        "example": "Graduating with honors was a major achievement for her."
    },
    {
        "front": "upload",
        "back": "загрузить (в интернет / на сервер)",
        "type": "good_language",
        "explanation": "Upload — загрузка ОТ пользователя на сервер (в отличие от download — скачивание К пользователю).",
        "example": "You can upload your homework directly to the classroom portal."
    },
    {
        "front": "social engineering",
        "back": "социальная инженерия (психологическое манипулирование)",
        "type": "good_language",
        "explanation": "Термин из кибербезопасности: атака через манипулирование людьми.",
        "example": "Phishing is the most widespread form of social engineering today."
    },
    {
        "front": "sad ➔ frustrated, upset, disappointed",
        "back": "расстроенный, подавленный, разочарованный (альтернативы sad)",
        "type": "suggestion",
        "explanation": "Слово sad слишком общее. Frustrated — когда злишься из-за препятствий; upset — расстроен эмоционально; disappointed — неоправдавшиеся ожидания.",
        "example": "He wasn't just sad, he felt extremely frustrated with the system."
    },
    {
        "front": "she said OK ➔ she agreed",
        "back": "она согласилась",
        "type": "suggestion",
        "explanation": "Глагол agree делает письменную и устную речь более лаконичной и стильной.",
        "example": "After a brief conversation, she agreed to our terms."
    },
    {
        "front": "'let's do it!' ➔ to suggest",
        "back": "предложить (сделать что-то)",
        "type": "suggestion",
        "explanation": "В косвенной речи фразу 'let's...' передают глаголом suggest: He suggested doing it.",
        "example": "She suggested taking a short break before the next meeting."
    },
    {
        "front": "I'm feel ➔ I feel / I'm feeling",
        "back": "я чувствую / чувствую себя",
        "type": "correction",
        "explanation": "ОШИБКА: Нельзя соединять глагол to be (am) с базовой формой глагола. Либо Present Simple: I feel, либо Continuous: I am feeling.",
        "example": "I feel confident about tomorrow's presentation."
    },
    {
        "front": "win some time ➔ buy some time",
        "back": "выиграть немного времени (оттянуть срок)",
        "type": "correction",
        "explanation": "ОШИБКА: Русское 'выиграть время' в английском передается идиомой BUY TIME (дословно 'купить время').",
        "example": "We asked for extra documentation to buy some time until the fix is ready."
    },
    {
        "front": "my header ➔ head of..., CEO, boss",
        "back": "мой руководитель / начальник / босс",
        "type": "correction",
        "explanation": "ОШИБКА: Header — это заголовок в документе или удар головой в футболе. Руководитель — это Head of Department, boss или CEO.",
        "example": "I need to discuss this proposal with the head of our department."
    },
    {
        "front": "abroad friend ➔ foreign friend / friend from abroad",
        "back": "друг из-за границы / иностранный друг",
        "type": "correction",
        "explanation": "ОШИБКА: Abroad — это наречие ('за границей'). Перед существительным friend используется либо foreign friend, либо friend from abroad.",
        "example": "A foreign friend of mine is coming to visit St. Petersburg next month."
    },
    {
        "front": "show for ➔ show to sb / explain",
        "back": "показать кому-то",
        "type": "correction",
        "explanation": "ОШИБКА: Глагол show сочетается с предлогом TO: show something TO somebody.",
        "example": "Can you please show the new dashboard to our client?"
    },
    {
        "front": "sit out",
        "back": "переждать (неприятность, бурю, скучную лекцию до конца)",
        "type": "vocab",
        "explanation": "Фразовый глагол: пересидеть или остаться в стороне, пока ситуация не успокоится.",
        "example": "We decided to sit out the storm inside a roadside diner."
    },
    {
        "front": "hole up",
        "back": "спрятаться в укрытии / отсиживаться",
        "type": "vocab",
        "explanation": "Фразовый глагол: закрыться в безопасном месте, пережидая опасность или пристальное внимание.",
        "example": "The author holed up in a mountain cabin to finish his book."
    },
    {
        "front": "lay low",
        "back": "залечь на дно / затаиться, не высовываться",
        "type": "vocab",
        "explanation": "Идиома: вести себя крайне тихо и незаметно, избегая внимания публики или полиции.",
        "example": "He was advised to lay low until the media scandal blew over."
    },
    {
        "front": "sit tight",
        "back": "сидеть тихо / ждать развития событий, не предпринимая резких действий",
        "type": "vocab",
        "explanation": "Идиома: выжидать в спокойствии: Just sit tight and wait for instructions.",
        "example": "Just sit tight, the rescue team will arrive in ten minutes."
    },
    {
        "front": "increased scholarship",
        "back": "повышенная / увеличенная стипендия",
        "type": "vocab",
        "explanation": "Выплата студентам в увеличенном размере.",
        "example": "Students with top grades are eligible for an increased scholarship."
    },
    {
        "front": "enhanced scholarship",
        "back": "стипендия с повышенным размером или расширенными условиями",
        "type": "vocab",
        "explanation": "Специальная программа стипендиальной поддержки.",
        "example": "The university introduced an enhanced scholarship for research assistants."
    },
    {
        "front": "academic excellence scholarship",
        "back": "стипендия за особые успехи в учебе (для отличников)",
        "type": "vocab",
        "explanation": "Стипендия за выдающиеся академические достижения.",
        "example": "He was awarded an academic excellence scholarship during his junior year."
    },
    {
        "front": "digest",
        "back": "дайджест / краткий сборник / переваривать (/daɪˈdʒest/)",
        "type": "vocab",
        "explanation": "Как существительное /ˈdaɪ.dʒest/ — краткая выжимка новостей; как глагол /daɪˈdʒest/ — усваивать пищу или информацию.",
        "example": "Here is a quick weekly digest of the tech news."
    },
    {
        "front": "eligibility / permission",
        "back": "право на участие, соответствие требованиям / допуск",
        "type": "vocab",
        "explanation": "Eligibility — соответствие критериям для участия: eligibility to take an exam.",
        "example": "Check your eligibility before applying for this government grant."
    },
    {
        "front": "color match",
        "back": "подбор цвета / гармоничное сочетание цветов",
        "type": "vocab",
        "explanation": "Термин из дизайна и моды для идеального сочетания оттенков.",
        "example": "The curtain and sofa color match is simply perfect."
    },

    # ----------------------------------------------------
    # Изображение 16: Доска 18.10.26 (media_1794166418025_dc470aaa.jpg)
    # ----------------------------------------------------
    {
        "front": "collecting trash",
        "back": "сбор мусора",
        "type": "good_language",
        "explanation": "Герундий collecting + существительное trash (мусор).",
        "example": "Volunteers spent Sunday collecting trash along the river bank."
    },
    {
        "front": "scary and strange",
        "back": "страшно и странно",
        "type": "good_language",
        "explanation": "Живая пара качественных прилагательных: scary (пугающий) and strange (странный).",
        "example": "The abandoned mansion looked scary and strange in the mist."
    },
    {
        "front": "on the road",
        "back": "на дороге / в пути",
        "type": "good_language",
        "explanation": "Устойчивая фраза с предлогом ON (on the road).",
        "example": "Be extra careful when driving on the road at night."
    },
    {
        "front": "accident happened",
        "back": "произошла авария / несчастный случай",
        "type": "good_language",
        "explanation": "Обратите внимание: с глаголом happen не используется пассивный залог (нельзя сказать 'was happened').",
        "example": "The accident happened just around the corner."
    },
    {
        "front": "he don't believe ➔ he doesn't believe",
        "back": "он не верит",
        "type": "correction",
        "explanation": "ОШИБКА: В Present Simple для местоимений he/she/it отрицание строится строго через DOESN'T (he doesn't believe).",
        "example": "He doesn't believe everything he reads on social media."
    },
    {
        "front": "was finding his son ➔ was looking for his son",
        "back": "искал своего сына",
        "type": "correction",
        "explanation": "ОШИБКА: Find — это мгновенный результат ('найти'). Сам процесс поиска — это глагол LOOK FOR (was looking for).",
        "example": "The worried father was looking for his son in the crowded mall."
    },
    {
        "front": "hurry up ➔ BE in a hurry",
        "back": "спешить / торопиться (состояние)",
        "type": "correction",
        "explanation": "Разница: 'Hurry up!' — это повелительный приказ ('поторопись!'). Описание состояния спешки — 'be in a hurry' (I am in a hurry).",
        "example": "I can't talk right now because I am in a hurry."
    },
    {
        "front": "to ask him 'could you change' ➔ to ask him IF he could change the music",
        "back": "спросить его, может ли он переключить музыку",
        "type": "correction",
        "explanation": "ОШИБКА: Косвенный вопрос без вопросительного слова требует союза IF или WHETHER, а порядок слов становится прямым (if he could change).",
        "example": "She politely asked the driver if he could change the radio station."
    },
    {
        "front": "much tasks (plural) ➔ many tasks",
        "back": "много задач",
        "type": "correction",
        "explanation": "ОШИБКА: С исчисляемыми существительными во множественном числе (tasks, books, people) используется MANY. Much — только для неисчисляемых.",
        "example": "We have too many tasks to complete before this Friday."
    },
    {
        "front": "anglerfish",
        "back": "рыба-удильщик (глубоководный удильщик)",
        "type": "vocab",
        "explanation": "Глубоководная хищная рыба с биолюминесцентной 'удочкой' на голове для приманивания добычи.",
        "example": "The anglerfish uses a glowing lure in the deep, dark ocean."
    },
    {
        "front": "recognize",
        "back": "узнавать (в лицо, по голосу) / признавать (/ˈrek.əɡ.naɪz/)",
        "type": "vocab",
        "explanation": "Знать кого-то, потому что уже видел или слышал раньше.",
        "example": "I hadn't seen her for twenty years, but I recognized her immediately."
    },
    {
        "front": "encounter",
        "back": "неожиданная встреча / столкновение / сталкиваться (/ɪnˈkaʊn.tər/)",
        "type": "vocab",
        "explanation": "Случайная встреча (encounter with a wild pig / encounter between leaders).",
        "example": "We had an unexpected encounter with our former teacher at the airport."
    },
    {
        "front": "escape",
        "back": "сбежать, спастись бегством (/ɪˈskeɪp/)",
        "type": "vocab",
        "explanation": "Уйти от опасности или из заключения.",
        "example": "The prisoners managed to escape through a secret tunnel."
    },
    {
        "front": "surround",
        "back": "окружать / брать в кольцо (/səˈraʊnd/)",
        "type": "vocab",
        "explanation": "Находиться вокруг чего-то со всех сторон (be surrounded by police).",
        "example": "The building was quickly surrounded by armed police officers."
    },
    {
        "front": "get well soon",
        "back": "выздоравливай скорее! / поправляйся!",
        "type": "vocab",
        "explanation": "Стандартное доброе пожелание заболевшему человеку (часто на открытках с мишкой).",
        "example": "We sent our sick colleague a box of fruit with a 'get well soon' card."
    },

    # ----------------------------------------------------
    # Изображение 17: Доска 23.10.26 (media_1794166435994_a5baad1f.jpg)
    # ----------------------------------------------------
    {
        "front": "a priest",
        "back": "священник",
        "type": "good_language",
        "explanation": "Священнослужитель (/priːst/).",
        "example": "They spoke to the village priest before making the final vow."
    },
    {
        "front": "what I should do",
        "back": "что мне следует сделать",
        "type": "good_language",
        "explanation": "Косвенный вопрос: модальный глагол should после подлежащего I (прямой порядок слов).",
        "example": "I was really confused and asked my mentor what I should do."
    },
    {
        "front": "go into your religion",
        "back": "углубляться в религию",
        "type": "good_language",
        "explanation": "Фразовый глагол go into — вдаваться в детали, глубоко погружаться в сферу.",
        "example": "He didn't want to go into his religious beliefs during the interview."
    },
    {
        "front": "for your knowledge",
        "back": "к твоему сведению / для твоих знаний",
        "type": "good_language",
        "explanation": "Knowledge — неисчисляемое существительное (всегда в единственном числе).",
        "example": "I shared those research materials purely for your knowledge."
    },
    {
        "front": "beliefs",
        "back": "убеждения, верования",
        "type": "good_language",
        "explanation": "Множественное число от belief (убеждение, вера).",
        "example": "People with different philosophical beliefs can still work well together."
    },
    {
        "front": "gain weight",
        "back": "набрать вес",
        "type": "good_language",
        "explanation": "Устойчивая фраза: gain weight (набрать) vs lose weight (сбросить).",
        "example": "It is easy to gain weight during winter holidays."
    },
    {
        "front": "build muscles",
        "back": "накачать / нарастить мышцы",
        "type": "good_language",
        "explanation": "Коллокация с глаголом build (build muscles).",
        "example": "Consistent gym workouts help you build lean muscles."
    },
    {
        "front": "gain muscle weight",
        "back": "набрать мышечную массу",
        "type": "good_language",
        "explanation": "Более точный спортивный термин для набора массы за счет мышц.",
        "example": "His diet was formulated specifically to gain muscle weight."
    },
    {
        "front": "about yourself",
        "back": "о себе",
        "type": "good_language",
        "explanation": "Возвратное местоимение yourself после предлога about.",
        "example": "Could you please tell us a little bit about yourself?"
    },
    {
        "front": "have no bf ➔ single",
        "back": "свободный, без отношений (не иметь парня)",
        "type": "suggestion",
        "explanation": "Вместо длинной фразы 'have no boyfriend' статус отношений лаконично обозначается словом 'single'.",
        "example": "She is currently single and focusing on her startup career."
    },
    {
        "front": "be married",
        "back": "быть в браке / женатым / замужем",
        "type": "suggestion",
        "explanation": "Состояние брака: They are married (они женаты) / They aren't married (они не женаты).",
        "example": "They have been married for more than fifteen years."
    },
    {
        "front": "bad words ➔ swear words",
        "back": "ругательства, нецензурные слова, мат",
        "type": "correction",
        "explanation": "ОШИБКА: 'Bad words' звучит по-детски. Во взрослом английском мат и ругань называют SWEAR WORDS (или profanity, curse words).",
        "example": "Using swear words is strictly prohibited in our company chat."
    },
    {
        "front": "bad time ➔ hard time",
        "back": "трудный период / тяжелые времена",
        "type": "correction",
        "explanation": "ОШИБКА: Трудный жизненный период — это 'a hard time' или 'tough times' (have a hard time).",
        "example": "He went through a really hard time after losing his job."
    },
    {
        "front": "how this do ➔ how TO do this",
        "back": "как это делать",
        "type": "correction",
        "explanation": "ОШИБКА: Инфинитивная конструкция: вопросительное слово + TO + глагол (how to do this, where to go, what to say).",
        "example": "Show me please how to do this correctly."
    },
    {
        "front": "have mistakes ➔ make mistakes",
        "back": "делать / совершать ошибки",
        "type": "correction",
        "explanation": "ОШИБКА: В английском совершать ошибки — устойчиво MAKE mistakes (не have mistakes и не do mistakes!).",
        "example": "It is completely normal to make mistakes when learning a foreign language."
    },
    {
        "front": "we more understand ➔ we understand more",
        "back": "мы понимаем больше",
        "type": "correction",
        "explanation": "ОШИБКА: Порядок слов: количественное наречие more ставится после глагола (we understand more).",
        "example": "With each lesson, we understand more about English grammar."
    },
    {
        "front": "I am sleeping (the match WAS boring) ➔ I WAS sleeping",
        "back": "я спал (матч был скучным)",
        "type": "correction",
        "explanation": "ОШИБКА: Согласование времен. Если контекст в прошлом ('the match was boring'), то и действие в процессе было в прошлом: Past Continuous (I WAS sleeping).",
        "example": "I was sleeping on the couch because the football match was so boring."
    },
    {
        "front": "I have girlfriend ➔ I have A girlfriend",
        "back": "у меня есть девушка",
        "type": "correction",
        "explanation": "ОШИБКА: Исчисляемое существительное в единственном числе в утверждении требует неопределенного артикля A: I have A girlfriend.",
        "example": "He mentioned that he has a girlfriend from Sweden."
    },
    {
        "front": "policeman ➔ police officer",
        "back": "сотрудник полиции / полицейский",
        "type": "correction",
        "explanation": "Современная гендерно-нейтральная норма в англоязычных странах — police officer (вместо policeman/policewoman).",
        "example": "A police officer stopped the car for speeding."
    },
    {
        "front": "enough money to rent a flat // for renting a flat",
        "back": "достаточно денег, чтобы снять квартиру",
        "type": "correction",
        "explanation": "Грамматика: существительное + to-infinitive (money to rent) ИЛИ предлог for + gerund (money for renting).",
        "example": "He saved enough money to rent a flat in the city center."
    },
    {
        "front": "to pray",
        "back": "молиться (/preɪ/)",
        "type": "vocab",
        "explanation": "Обращаться к богу с молитвой. (Омофон слова prey — добыча).",
        "example": "Many believers gather in the cathedral to pray."
    },
    {
        "front": "to sin / sinner",
        "back": "грешить / грешник",
        "type": "vocab",
        "explanation": "To sin — совершать грех; a sinner — человек, совершивший грех.",
        "example": "In theological ethics, even a sinner can seek redemption."
    },
    {
        "front": "a tab",
        "back": "вкладка (в веб-браузере)",
        "type": "vocab",
        "explanation": "Вкладка браузера: open a new tab / close the active tab.",
        "example": "I had over thirty tabs open in Google Chrome."
    },
    {
        "front": "fall out of love",
        "back": "разлюбить (перестать любить)",
        "type": "vocab",
        "explanation": "Противоположность фразы fall in love (влюбиться).",
        "example": "It was painful when they gradually fell out of love."
    },
    {
        "front": "werewolf",
        "back": "оборотень (/ˈwɪə.wʊlf/ или /ˈwer.wʊlf/)",
        "type": "vocab",
        "explanation": "Мифическое существо — человек, превращающийся в волка при полной луне.",
        "example": "In folklore, a werewolf transforms during a full moon."
    },
    {
        "front": "rose-colored glasses",
        "back": "розовые очки (видеть мир через розовые очки)",
        "type": "vocab",
        "explanation": "Идиома: наивно-идеалистичный взгляд на мир: see the world through rose-colored glasses.",
        "example": "Take off your rose-colored glasses and look at real facts."
    },
    {
        "front": "attractive",
        "back": "привлекательный, притягательный (/əˈtræk.tɪv/)",
        "type": "vocab",
        "explanation": "Прилагательное от attract (привлекать). О внешности или выгодном предложении.",
        "example": "The company made him a very attractive job offer."
    },
    {
        "front": "concussion",
        "back": "сотрясение мозга (/kənˈkʌʃ.ən/)",
        "type": "vocab",
        "explanation": "Медицинский термин травмы головы (сотрясение).",
        "example": "The hockey player suffered a mild concussion after the collision."
    },

    # ----------------------------------------------------
    # Изображение 18: Доска 04.11.26 (media_1794166455796_f9d72c84.jpg)
    # ----------------------------------------------------
    {
        "front": "for your soul",
        "back": "для души",
        "type": "good_language",
        "explanation": "Приятное выражение о хобби и любимых занятиях: something for your soul.",
        "example": "Playing piano in the evening is pure therapy for your soul."
    },
    {
        "front": "scheduling",
        "back": "составление расписания / планирование графика",
        "type": "good_language",
        "explanation": "Герундий от глагола schedule (/ˈʃedʒ.uːl/ UK, /ˈskedʒ.uːl/ US).",
        "example": "Effective scheduling is critical for meeting project deadlines."
    },
    {
        "front": "was banned",
        "back": "был забанен / запрещен",
        "type": "good_language",
        "explanation": "Пассивный залог от глагола ban (запрещать).",
        "example": "His account was banned for violating community guidelines."
    },
    {
        "front": "accommodation",
        "back": "жилье / размещение (в отеле, апартаментах)",
        "type": "good_language",
        "explanation": "Обратите внимание на правописание: с двумя 'c' и двумя 'm' (accommodation).",
        "example": "The university provides affordable accommodation for foreign students."
    },
    {
        "front": "it's not for me ➔ It's not my cup of tea",
        "back": "это не в моем вкусе / не мое",
        "type": "suggestion",
        "explanation": "Классическая английская вежливая идиома отказа или неприязни: 'It's not my cup of tea'.",
        "example": "Heavy metal is definitely not my cup of tea; I prefer classical music."
    },
    {
        "front": "it's not for me ➔ It's not my thing / I'm not really into it",
        "back": "это не мое / я этим особо не увлекаюсь",
        "type": "suggestion",
        "explanation": "Очень популярные современные разговорные фразы: 'It's not my thing' и 'I'm not into it'.",
        "example": "Skiing is not really my thing, I hate freezing cold."
    },
    {
        "front": "it's not for me ➔ It doesn't float my boat / It's not my scene",
        "back": "это меня не заводит / это не моя тусовка",
        "type": "suggestion",
        "explanation": "Колоритные идиомы: 'float one's boat' (приносить удовольствие) и 'not my scene' (не моя среда/атмосфера).",
        "example": "Clubbing until dawn just doesn't float my boat anymore."
    },
    {
        "front": "for your hands ➔ with your hands",
        "back": "своими руками (делать что-то руками)",
        "type": "correction",
        "explanation": "ОШИБКА: Инструмент или часть тела, которой совершается действие, требует предлога WITH (make something WITH your hands).",
        "example": "He loves crafting wooden furniture with his own hands."
    },
    {
        "front": "minimize your nerves ➔ calm your nerves",
        "back": "успокоить нервы",
        "type": "correction",
        "explanation": "ОШИБКА: 'Minimize nerves' звучит искусственно. Идиома носителей — CALM YOUR NERVES (или soothe your nerves).",
        "example": "Take a deep breath to calm your nerves before going on stage."
    },
    {
        "front": "more lazier ➔ lazier",
        "back": "более ленивый",
        "type": "correction",
        "explanation": "ОШИБКА: Двойная сравнительная степень (more + суффикс -er) — грубая ошибка! Правильно только LAZIER.",
        "example": "I feel much lazier on cold rainy Sundays."
    },
    {
        "front": "twice day ago ➔ two days ago",
        "back": "два дня назад",
        "type": "correction",
        "explanation": "ОШИБКА: Twice означает 'дважды' (о кратности). Временной промежуток назад — 'two days ago'.",
        "example": "I saw him at the office two days ago."
    },
    {
        "front": "alcohol",
        "back": "алкоголь [произношение: UK /ˈæl.kə.hɒl/, US /ˈæl.kə.hɑːl/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Ударение строго на первый слог /ˈæl.kə.hɒl/ (не на последний, как в русском!).",
        "example": "He completely cut out alcohol while training for the marathon."
    },
    {
        "front": "theme",
        "back": "тема [произношение: /θiːm/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Межзубный звук [θ] и долгий гласный [iː] (не 'тем'!).",
        "example": "The main theme of this year's conference is cybersecurity."
    },
    {
        "front": "version",
        "back": "версия [произношение: UK /ˈvɜː.ʃən/, US /ˈvɝː.ʒən/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: В британском варианте звук [ʃ] (/ˈvɜː.ʃən/), в американском чаще [ʒ] (/ˈvɝː.ʒən/).",
        "example": "Make sure you install the latest stable version of the app."
    },
    {
        "front": "download",
        "back": "скачивать [произношение: глагол UK /ˌdaʊnˈləʊd/, US /ˈdaʊn.loʊd/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Дифтонг [aʊ] в первом слоге (down) и [əʊ] во втором (load).",
        "example": "You can download the full database backup from our web server."
    },
    {
        "front": "support",
        "back": "поддержка / поддерживать [произношение: UK /səˈpɔːt/, US /səˈpɔːrt/]",
        "type": "vocab",
        "explanation": "ФОНЕТИКА: Безударный первый слог со звуком шва [sə-] и долгий ударный [pɔːt].",
        "example": "Thank you so much for your continuous help and support."
    },
    {
        "front": "dried flowers",
        "back": "сухоцветы (засушенные цветы)",
        "type": "vocab",
        "explanation": "Dried — причастие 'засушенный' (dried flowers, dried fruit).",
        "example": "She arranged a beautiful vase of dried flowers on the dining table."
    },
    {
        "front": "feminine",
        "back": "женственный, женский (/ˈfem.ɪ.nɪn/)",
        "type": "vocab",
        "explanation": "Прилагательное: feminine qualities / feminine clothing.",
        "example": "She wore an elegant and very feminine dress to the gala."
    },
    {
        "front": "opportunity / reason / chance",
        "back": "повод / возможность / шанс",
        "type": "vocab",
        "explanation": "Разница: opportunity — удобная возможность; reason — причина/повод; chance — случайный шанс.",
        "example": "His birthday was a wonderful opportunity for the whole family to gather."
    },
    {
        "front": "take a nap / have a nap",
        "back": "вздремнуть (короткий дневной сон)",
        "type": "vocab",
        "explanation": "Идиома: поспать 15-30 минут днем для восстановления сил.",
        "example": "I always feel refreshed after taking a 20-minute power nap."
    }
]

def main():
    added = 0
    by_type = {}
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        for item in BATCH_3_CARDS:
            cursor.execute(
                "SELECT id FROM cards WHERE user_id = 0 AND front = ? AND type = ?",
                (item["front"], item["type"])
            )
            exists = cursor.fetchone()
            if not exists:
                db.add_card(item, user_id=0)
                added += 1
                by_type[item["type"]] = by_type.get(item["type"], 0) + 1

    print(f"[✓] Успешно добавлено новых карточек партии 3: {added}")
    print("По категориям третьей партии:")
    for t, cnt in by_type.items():
        print(f"  • {t}: {cnt}")
        
    stats = db.get_stats(user_id=0)
    print("\nИтоговое общее состояние базы данных тренажера:")
    print(f"  📚 Всего карточек в базе: {stats['total']}")
    print(f"  ⏰ Ждут повторения: {stats['due']}")
    print(f"  Разбивка: {stats['by_type']}")

if __name__ == "__main__":
    main()
