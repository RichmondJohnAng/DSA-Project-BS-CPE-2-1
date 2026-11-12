import re
from datetime import date

def get_profile_level_data(today=None):
    if today is None:
        today = date.today()
    birth_year = 2006
    birth_month = 5
    birth_day = 29

    this_year_bday = date(today.year, birth_month, birth_day)
    if today >= this_year_bday:
        prev_bday = this_year_bday
        next_bday = date(today.year + 1, birth_month, birth_day)
        level = today.year - birth_year
    else:
        prev_bday = date(today.year - 1, birth_month, birth_day)
        next_bday = this_year_bday
        level = today.year - 1 - birth_year

    days_passed = (today - prev_bday).days
    total_days = (next_bday - prev_bday).days
    percent = round((days_passed / total_days) * 100, 1)

    return {
        'level': level,
        'days_passed': days_passed,
        'total_days': total_days,
        'percent': percent,
        'prev_bday': prev_bday.strftime('%B %d, %Y'),
        'next_bday': next_bday.strftime('%B %d, %Y')
    }

def get_melo_library_data():
    data = {
        'title': 'Ako ang Bagyo',
        'artist': 'SHEAN',
        'start_at': 108.81,
        'end_at': 148.17,
        'audio_url': '/static/audio/ako_ang_bagyo.webm',
        'credits': 'ivanhr_r',
        'credits_url': 'https://github.com/ivanhr-r',
        'lines': [],
        'keywords': {
            "bagyo": {"color": "#FFF1A8", "glow": "#5b7fe0", "scale": 2.1, "event": "strike"},
            "ako": {"color": "#BFD9FF", "glow": "#3558a8", "scale": 1.45, "event": None},
            "yero": {"color": "#DDE6F2", "glow": "#6a7a90", "scale": 1.9, "event": "yero"},
            "matakot": {"color": "#FFB09C", "glow": "#a8321f", "scale": 1.5, "event": None},
            "tatangayin": {"color": "#9FE3FF", "glow": "#2a7fa8", "scale": 1.5, "event": "gust"},
            "kulimlim": {"color": "#C9D3E6", "glow": "#3b4a68", "scale": 1.4, "event": None},
            "masaya": {"color": "#FF9DB4", "glow": "#a82a4a", "scale": 1.4, "event": None},
            "kayo": {"color": "#FF9DB4", "glow": "#a82a4a", "scale": 1.2, "event": None},
            "dalawa": {"color": "#FF9DB4", "glow": "#a82a4a", "scale": 1.3, "event": None}
        }
    }

    content = None
    for candidate_path in ('import/ako ang bagyo - SHEAN.py', '../import/ako ang bagyo - SHEAN.py'):
        try:
            with open(candidate_path, 'r', encoding='utf-8') as f:
                content = f.read()
            break
        except Exception:
            continue

    if content:
        try:
            lrc_m = re.search(r'lrc\s*=\s*"""(.*?)"""', content, re.DOTALL)
            if lrc_m:
                stamp = re.compile(r"^\s*\[(\d+):(\d+(?:\.\d+)?)\](.*)$")
                entries = []
                for raw in lrc_m.group(1).splitlines():
                    m = stamp.match(raw)
                    if m:
                        sec = int(m.group(1)) * 60 + float(m.group(2))
                        entries.append((sec, m.group(3).strip()))
                entries.sort(key=lambda e: e[0])
                for i, (ts, text) in enumerate(entries):
                    nxt = entries[i + 1][0] if i + 1 < len(entries) else ts + 8.0
                    data['lines'].append({
                        'time': round(ts, 2),
                        'text': text.replace('sainyong', 'sa inyong'),
                        'duration': round(max(2.0, nxt - ts), 2)
                    })

            start_m = re.search(r'start_at\s*=\s*([0-9\.]+)', content)
            if start_m:
                data['start_at'] = float(start_m.group(1))

            end_m = re.search(r'end_at\s*=\s*([0-9\.]+)', content)
            if end_m:
                data['end_at'] = float(end_m.group(1))
        except Exception as e:
            print("Error parsing lyrics from ako ang bagyo - SHEAN.py:", e)

    return data
