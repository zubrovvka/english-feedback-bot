"""
Batch import of cards from Miro board session dated 16.11.26
Sources:
  - img1: Airport vocabulary with definitions
  - img2: Airport words with numbers (order exercise)
  - img3: Miro feedback board (good_language, corrections, suggestions, pronunciation, new_vocab)
  - img4: Pink sticky notes (give a talk, look forward)
  - img5/6: Pink stickies (arrive vs arrival, prefer having)
  - img7: Collocation card (wait FOR)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db

db.init_db()

cards = [
    # ── IMG 1: Airport vocab with definitions ─────────────────────────────────
    {
        "type": "vocab",
        "front": "stopover",
        "back": "/ˈstɒpəʊvə/ = a short stay somewhere between two parts of a journey",
        "raw_original": "stopover /ˈstɒpəʊvə/ = a short stay somewhere between two parts of a journey",
    },
    {
        "type": "vocab",
        "front": "connecting flight",
        "back": "/kəˈnektɪŋ flaɪt/ = a second flight where you have had to change planes",
        "raw_original": "connecting flight /kəˈnektɪŋ flaɪt/ = a second flight where you have had to change planes",
    },
    {
        "type": "vocab",
        "front": "departure lounge",
        "back": "/dɪˈpɑːtʃə laʊndʒ/ = the place at an airport where you wait for your flight",
        "raw_original": "departure lounge /dɪˈpɑːtʃə laʊndʒ/ = the place at an airport where you wait for your flight",
    },
    {
        "type": "vocab",
        "front": "duty-free shop",
        "back": "/ˌdjuːti ˈfriː ʃɒp/ = a shop at an airport or on a ship that sells things like cigarettes, alcohol, perfume, etc. without tax on them",
        "raw_original": "duty-free shop /ˌdjuːti ˈfriː ʃɒp/ = a shop at an airport or on a ship, etc. that sells things like cigarettes, alcohol, perfume, etc. without tax on them",
    },
    {
        "type": "vocab",
        "front": "air traveller",
        "back": "/eə ˈtrævələ/ = a passenger on a plane",
        "raw_original": "air traveller /eə ˈtrævələ/ = a passenger on a plane",
    },

    # ── IMG 2: Airport places (numbered order exercise) ───────────────────────
    {
        "type": "vocab",
        "front": "arrivals",
        "back": "The area in an airport where passengers arrive after landing",
        "raw_original": "arrivals (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "bag drop",
        "back": "The place at an airport where you leave your checked luggage before going through security",
        "raw_original": "bag drop (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "baggage reclaim",
        "back": "The area in an airport where you collect your luggage after a flight",
        "raw_original": "baggage reclaim (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "check-in",
        "back": "The process of registering for your flight and leaving your luggage at the airport",
        "raw_original": "check-in (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "customs",
        "back": "The place at an airport or port where your bags are checked for illegal goods",
        "raw_original": "customs (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "departures",
        "back": "The area in an airport where passengers go before boarding their flights",
        "raw_original": "departures (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "gates",
        "back": "The numbered doors at an airport where you board your flight",
        "raw_original": "gates (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "passport control",
        "back": "The area at an airport where officials check your passport before you enter or leave a country",
        "raw_original": "passport control (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "security check",
        "back": "The process at an airport where passengers and their bags are checked for dangerous items",
        "raw_original": "security check (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "terminal",
        "back": "A large building at an airport where passengers arrive and depart",
        "raw_original": "terminal (airport vocabulary)",
    },
    {
        "type": "vocab",
        "front": "trolley",
        "back": "A metal frame on wheels used to carry luggage at an airport or supermarket",
        "raw_original": "trolley (airport vocabulary)",
    },

    # ── IMG 3: Miro feedback board 16.11.26 ───────────────────────────────────
    # good_language
    {
        "type": "good_language",
        "front": "lost your time",
        "back": "Good expression: 'lost your time' (wasted time)",
        "raw_original": "lost your time",
    },
    {
        "type": "good_language",
        "front": "wonderful environment",
        "back": "Good expression: 'wonderful environment'",
        "raw_original": "wonderful environment",
    },
    {
        "type": "good_language",
        "front": "price can be different",
        "back": "Good expression: 'price can be different'",
        "raw_original": "price can be different",
    },
    {
        "type": "good_language",
        "front": "another level",
        "back": "Good expression: 'another level'",
        "raw_original": "another level",
    },
    {
        "type": "good_language",
        "front": "look around",
        "back": "Good expression: 'look around' (explore a place)",
        "raw_original": "look around",
    },
    {
        "type": "good_language",
        "front": "main thing",
        "back": "Good expression: 'the main thing'",
        "raw_original": "main thing",
    },
    {
        "type": "good_language",
        "front": "what you should do",
        "back": "Good expression: 'what you should do'",
        "raw_original": "what you should do",
    },
    # corrections
    {
        "type": "corrections",
        "front": "what is mean",
        "back": "❌ what is mean → ✅ what does it mean",
        "raw_original": "what is mean",
    },
    {
        "type": "corrections",
        "front": "prefer just sit",
        "back": "❌ prefer just sit → ✅ prefer just sitting without moving / prefer TO stay",
        "raw_original": "prefer just sit -> prefer sitting without moving / prefer TO stay",
    },
    {
        "type": "corrections",
        "front": "possibility",
        "back": "❌ possibility → ✅ opportunity (возможность, a chance)",
        "raw_original": "possibility -> opportunity (возможность, a chance)",
    },
    {
        "type": "corrections",
        "front": "it is not matter",
        "back": "❌ it is not matter → ✅ it doesn't matter",
        "raw_original": "it is not matter -> it doesn't matter",
    },
    {
        "type": "corrections",
        "front": "connection flight",
        "back": "❌ connection flight → ✅ connecting flight",
        "raw_original": "connection flight -> connecting flight",
    },
    {
        "type": "corrections",
        "front": "comfortable walk",
        "back": "❌ comfortable walk → ✅ it's not convenient/conf TO walk",
        "raw_original": "comfortable walk -> it's not convenient/conf TO walk",
    },
    {
        "type": "corrections",
        "front": "more cheap",
        "back": "❌ more cheap → ✅ cheaper",
        "raw_original": "more cheap -> cheaper",
    },
    {
        "type": "corrections",
        "front": "really many handbag",
        "back": "❌ really many handbag → ✅ a lot of handbags",
        "raw_original": "really many handbag -> a lot of handbags",
    },
    {
        "type": "corrections",
        "front": "go to something",
        "back": "❌ go to something → ✅ go somewhere",
        "raw_original": "go to something -> go somewhere",
    },
    # suggestions
    {
        "type": "suggestions",
        "front": "nervous",
        "back": "nervous → anxious (more formal/stronger alternative)",
        "raw_original": "nervous -> anxious",
    },
    {
        "type": "suggestions",
        "front": "my tasks",
        "back": "my tasks → personal tasks / affairs (more natural)",
        "raw_original": "my tasks -> personal tasks / affairs",
    },
    # pronunciation
    {
        "type": "vocab",
        "front": "aisle /aɪl/ pronunciation",
        "back": "Aisle sounds like 'ile' — the 's' is silent! /aɪl/\nAmerican English IPA: /preɪ si dʒeɪ/\nBritish English IPA: /preɪ si dʒeɪ/ (Cambridge Dictionary)",
        "raw_original": "Aisle — sounds like 'ile' (pronunciation note from board)",
    },
    # new_vocab
    {
        "type": "vocab",
        "front": "aisle seat",
        "back": "A seat next to the aisle (walkway) on a plane or in a theatre — not a window seat",
        "raw_original": "aisle seat (new vocab 16.11.26)",
    },
    {
        "type": "vocab",
        "front": "long-haul flight",
        "back": "A very long flight, typically over 6–7 hours (e.g. London → New York)",
        "raw_original": "long-haul flight (new vocab 16.11.26)",
    },
    {
        "type": "vocab",
        "front": "arrive vs arrival",
        "back": "ARRIVE (verb) = to reach a place. Example: 'We will arrive at noon.'\nARRIVAL (noun) = the act of coming to a place, or someone/something that has come. Example: 'Everyone waited for his arrival.'",
        "raw_original": "arrive vs arrival — Arrive is a verb (action): to reach a place. Arrival is a noun (thing, event, or person).",
    },
    {
        "type": "vocab",
        "front": "look (verb uses)",
        "back": "look = to direct your eyes in a particular direction\nCommon collocations: look around, look forward to, look at, look for",
        "raw_original": "look (new vocab 16.11.26)",
    },
    {
        "type": "vocab",
        "front": "visa-requiring zone / Schengen Area",
        "back": "The Schengen Area is a zone consisting of 29 countries that have eliminated internal border controls between them",
        "raw_original": "visa-requiring zone / Schengen Area (new vocab 16.11.26)",
    },

    # ── IMG 4: Pink stickies ──────────────────────────────────────────────────
    {
        "type": "vocab",
        "front": "give a talk",
        "back": "To give a talk = to make a speech or presentation to an audience\nExample: 'She gave a talk about climate change.'",
        "raw_original": "give a talk (pink sticky)",
    },
    {
        "type": "vocab",
        "front": "look forward (to)",
        "back": "look forward to + noun/gerund = to feel excited and pleased about something that is going to happen\nExample: 'I look forward to seeing you.' (NOT: look forward to see)",
        "raw_original": "look forward (pink sticky)",
    },

    # ── IMG 5/6: Partial stickies ──────────────────────────────────────────────
    {
        "type": "vocab",
        "front": "prefer having",
        "back": "prefer + -ing = to like something more than something else\nExample: 'I prefer having a window seat.'\nNote: prefer TO + infinitive is also correct: 'I prefer to sit by the window.'",
        "raw_original": "prefer having (pink sticky)",
    },

    # ── IMG 7: Collocation card ───────────────────────────────────────────────
    {
        "type": "vocab",
        "front": "wait FOR",
        "back": "wait FOR + noun/pronoun = to stay until something or someone arrives\nExample: 'I'll wait for you at the gate.'\n❌ Don't say: wait someone (without FOR)",
        "raw_original": "wait FOR (collocation card)",
    },
]

added = 0
skipped = 0

for card in cards:
    result = db.add_card(card, user_id=0)
    if result:
        added += 1
        print(f"  ✅ Added [{card['type']}]: {card['front']}")
    else:
        skipped += 1
        print(f"  ⚠️  Skipped (duplicate?): {card['front']}")

print(f"\n{'='*50}")
print(f"Done! Added: {added}, Skipped: {skipped}")

# Count total
all_cards = db.get_all_cards(limit=9999)
print(f"Total cards in DB: {len(all_cards)}")
