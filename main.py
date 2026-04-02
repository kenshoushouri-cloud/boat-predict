# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import requests
from datetime import datetime, timedelta

# ============================

# 設定

# ============================

SUPABASE_URL = ‘https://xjccczavddenpcdrzywi.supabase.co’
SUPABASE_KEY = os.environ.get(‘SUPABASE_KEY’, ‘’)
LINE_TOKEN = os.environ.get(‘LINE_TOKEN’, ‘’)
LINE_API_URL = ‘https://api.line.me/v2/bot/message/broadcast’

TARGET_VENUES = [1, 6, 12, 18, 24]
VENUE_NAMES = {‘01’: ‘桐生’, ‘06’: ‘常滑’, ‘12’: ‘住之江’, ‘18’: ‘下関’, ‘24’: ‘大村’}
BASE_URL = ‘https://boatraceopenapi.github.io’

# ============================

# ログ

# ============================

def log_info(msg):
print(’[INFO] ’ + datetime.now().strftime(’%Y-%m-%d %H:%M:%S’) + ’ ’ + str(msg))

def log_error(msg):
print(’[ERROR] ’ + datetime.now().strftime(’%Y-%m-%d %H:%M:%S’) + ’ ’ + str(msg))

# ============================

# 日付

# ============================

def today_str():
return datetime.now().strftime(’%Y-%m-%d’)

def get_date_str():
return datetime.now().strftime(’%Y%m%d’)

def get_year_str():
return datetime.now().strftime(’%Y’)

def get_yesterday():
return (datetime.now() - timedelta(days=1)).strftime(’%Y-%m-%d’)

def get_yesterday_str():
return (datetime.now() - timedelta(days=1)).strftime(’%Y%m%d’)

# ============================

# Supabase

# ============================

class SupabaseTable:
def **init**(self, base_url, headers, table_name):
self.base_url = base_url
self.table_name = table_name
self.url = base_url + ‘/’ + table_name
self.headers = headers
self.query = ‘’
self._body = None
self._method = ‘GET’

```
def select(self, query='*'):
    self._method = 'GET'
    self.query = '?select=' + query
    return self

def eq(self, column, value):
    connector = '&' if '?' in self.query else '?'
    self.query += connector + column + '=eq.' + str(value)
    return self

def order(self, column, desc=False):
    connector = '&' if '?' in self.query else '?'
    direction = 'desc' if desc else 'asc'
    self.query += connector + 'order=' + column + '.' + direction
    return self

def limit(self, n):
    connector = '&' if '?' in self.query else '?'
    self.query += connector + 'limit=' + str(n)
    return self

def single(self):
    connector = '&' if '?' in self.query else '?'
    self.query += connector + 'limit=1'
    return self

def insert(self, data):
    self._method = 'POST'
    self._body = data
    return self

def update(self, data):
    self._method = 'PATCH'
    self._body = data
    return self

def delete(self):
    self._method = 'DELETE'
    return self

def execute(self):
    url = self.url + self.query
    try:
        if self._method == 'GET':
            res = requests.get(url, headers=self.headers, timeout=15)
        elif self._method == 'POST':
            h = dict(self.headers)
            h['Prefer'] = 'return=representation'
            res = requests.post(url, headers=h, json=self._body, timeout=15)
        elif self._method == 'PATCH':
            h = dict(self.headers)
            h['Prefer'] = 'return=representation'
            res = requests.patch(url, headers=h, json=self._body, timeout=15)
        elif self._method == 'DELETE':
            h = dict(self.headers)
            h['Prefer'] = 'return=representation'
            res = requests.delete(url, headers=h, timeout=15)
        else:
            res = requests.get(url, headers=self.headers, timeout=15)
        try:
            data = res.json()
        except Exception:
            data = []
        if isinstance(data, list):
            return type('Response', (), {'data': data})()
        elif isinstance(data, dict):
            return type('Response', (), {'data': [data]})()
        return type('Response', (), {'data': []})()
    except Exception as e:
        log_error('Supabase error: ' + str(e))
        return type('Response', (), {'data': []})()
```

class SupabaseClient:
def **init**(self):
self.base_url = SUPABASE_URL + ‘/rest/v1’
self.headers = {
‘apikey’: SUPABASE_KEY,
‘Authorization’: ’Bearer ’ + SUPABASE_KEY,
‘Content-Type’: ‘application/json’
}

```
def table(self, table_name):
    return SupabaseTable(self.base_url, self.headers, table_name)
```

def get_supabase():
return SupabaseClient()

# ============================

# LINE送信

# ============================

def send_line_message(message):
try:
headers = {
‘Authorization’: ’Bearer ’ + LINE_TOKEN,
‘Content-Type’: ‘application/json’
}
data = {‘messages’: [{‘type’: ‘text’, ‘text’: message[:4999]}]}
res = requests.post(LINE_API_URL, headers=headers, json=data, timeout=15)
if res.status_code == 200:
log_info(‘LINE送信成功’)
else:
log_error(’LINE送信失敗: ’ + str(res.status_code) + ’ ’ + res.text)
except Exception as e:
log_error(’LINE送信エラー: ’ + str(e))

# ============================

# データ取得 (Boatrace Open API)

# ============================

def fetch_programs():
url = BASE_URL + ‘/programs/v2/’ + get_year_str() + ‘/’ + get_date_str() + ‘.json’
try:
res = requests.get(url, timeout=15)
if res.status_code != 200:
return []
return [p for p in res.json().get(‘programs’, []) if p.get(‘race_stadium_number’) in TARGET_VENUES]
except Exception as e:
log_error(’出走表取得エラー: ’ + str(e))
return []

def fetch_results_api(date_str=None, year_str=None):
if not date_str:
date_str = get_yesterday_str()
if not year_str:
year_str = date_str[:4]
url = BASE_URL + ‘/results/v2/’ + year_str + ‘/’ + date_str + ‘.json’
try:
res = requests.get(url, timeout=15)
if res.status_code != 200:
return []
return [r for r in res.json().get(‘results’, []) if r.get(‘race_stadium_number’) in TARGET_VENUES]
except Exception as e:
log_error(’結果取得エラー: ’ + str(e))
return []

def fetch_previews_api(date_str=None, year_str=None):
if not date_str:
date_str = get_yesterday_str()
if not year_str:
year_str = date_str[:4]
url = BASE_URL + ‘/previews/v2/’ + year_str + ‘/’ + date_str + ‘.json’
try:
res = requests.get(url, timeout=15)
if res.status_code != 200:
return []
return [p for p in res.json().get(‘previews’, []) if p.get(‘race_stadium_number’) in TARGET_VENUES]
except Exception as e:
log_error(’直前情報取得エラー: ’ + str(e))
return []

# ============================

# 気象庁API

# ============================

VENUE_JMA_CODES = {
‘01’: ‘100000’, ‘06’: ‘230000’, ‘12’: ‘270000’, ‘18’: ‘350000’, ‘24’: ‘420000’
}
WIND_DIR_MAP = {
‘北’: ‘N’, ‘北東’: ‘NE’, ‘東’: ‘E’, ‘南東’: ‘SE’,
‘南’: ‘S’, ‘南西’: ‘SW’, ‘西’: ‘W’, ‘北西’: ‘NW’, ‘静穏’: ‘無風’
}

def fetch_jma_weather(venue_id):
vid = str(venue_id).zfill(2)
code = VENUE_JMA_CODES.get(vid)
if not code:
return {}
try:
url = ‘https://www.jma.go.jp/bosai/forecast/data/forecast/’ + code + ‘.json’
res = requests.get(url, timeout=10)
if res.status_code != 200:
return {}
data = res.json()
result = {‘wind’: 0, ‘wind_direction’: ‘不明’, ‘temperature’: 0, ‘wave’: 0}
for ts in data[0].get(‘timeSeries’, []):
areas = ts.get(‘areas’, [])
if not areas:
continue
area = areas[0]
if ‘winds’ in area and area[‘winds’]:
wind_str = area[‘winds’][0]
for jp, en in WIND_DIR_MAP.items():
if jp in wind_str:
result[‘wind_direction’] = en
break
if ‘temps’ in area and area[‘temps’]:
try:
result[‘temperature’] = float(area[‘temps’][0])
except Exception:
pass
return result
except Exception as e:
log_error(’気象庁API エラー: ’ + str(e))
return {}

# ============================

# データ保存

# ============================

def save_today_races(programs):
supabase = get_supabase()
today = today_str()
try:
supabase.table(‘today_races’).delete().eq(‘date’, today).execute()
except Exception as e:
log_error(’today_races削除エラー: ’ + str(e))
for p in programs:
venue_id = str(p[‘race_stadium_number’]).zfill(2)
try:
supabase.table(‘today_races’).insert({
‘venue_id’: venue_id,
‘venue_name’: VENUE_NAMES.get(venue_id, venue_id),
‘race_no’: p[‘race_number’],
‘start_time’: str(p.get(‘race_closed_at’, ‘’))[:16],
‘date’: today
}).execute()
except Exception as e:
log_error(’today_races保存エラー: ’ + str(e))

def save_players(programs):
supabase = get_supabase()
today = today_str()
try:
supabase.table(‘players’).delete().eq(‘date’, today).execute()
except Exception as e:
log_error(’players削除エラー: ’ + str(e))
for p in programs:
venue_id = int(p[‘race_stadium_number’])
for boat in p.get(‘boats’, []):
try:
supabase.table(‘players’).insert({
‘venue_id’: venue_id,
‘race_no’: p[‘race_number’],
‘lane’: boat.get(‘racer_boat_number’),
‘name’: boat.get(‘racer_name’, ‘’),
‘racer_number’: boat.get(‘racer_number’),
‘class’: boat.get(‘racer_class_number’),
‘branch’: boat.get(‘racer_branch_number’),
‘date’: today
}).execute()
except Exception as e:
log_error(’players保存エラー: ’ + str(e))

def save_weather_records(programs):
supabase = get_supabase()
today = today_str()
done = set()
for p in programs:
vid = int(p[‘race_stadium_number’])
if vid in done:
continue
done.add(vid)
try:
supabase.table(‘weather’).delete().eq(‘venue_id’, vid).eq(‘date’, today).execute()
supabase.table(‘weather’).insert({‘venue_id’: vid, ‘date’: today}).execute()
except Exception as e:
log_error(’weather初期化エラー: ’ + str(e))
weather = fetch_jma_weather(vid)
if weather:
try:
supabase.table(‘weather’).update({
‘wind’: weather.get(‘wind’, 0),
‘wind_direction’: weather.get(‘wind_direction’),
‘temperature’: weather.get(‘temperature’, 0),
‘wave’: 0,
}).eq(‘venue_id’, vid).eq(‘date’, today).execute()
except Exception as e:
log_error(’weather更新エラー: ’ + str(e))

def save_results(results):
supabase = get_supabase()
yesterday = get_yesterday()
for r in results:
venue_id = str(r[‘race_stadium_number’]).zfill(2)
race_no = r[‘race_number’]
boats = r.get(‘boats’, [])
if not boats:
continue
existing = supabase.table(‘results’).select(‘id’).eq(‘venue_id’, venue_id).eq(‘race_no’, race_no).eq(‘date’, yesterday).execute()
if existing.data:
continue
def get_boat(place):
for b in boats:
if (b.get(‘racer_place_number’) or 99) == place:
return b.get(‘racer_boat_number’)
return None
try:
supabase.table(‘results’).insert({
‘venue_id’: venue_id,
‘place’: VENUE_NAMES.get(venue_id, venue_id),
‘race_no’: race_no,
‘date’: yesterday,
‘first’: get_boat(1),
‘second’: get_boat(2),
‘third’: get_boat(3),
‘fourth’: get_boat(4),
‘fifth’: get_boat(5),
‘sixth’: get_boat(6),
}).execute()
except Exception as e:
log_error(’results保存エラー: ’ + str(e))

def save_exhibition(previews):
supabase = get_supabase()
yesterday = get_yesterday()
for p in previews:
venue_id = str(p[‘race_stadium_number’]).zfill(2)
boats = p.get(‘boats’, {})
if isinstance(boats, dict):
boats = boats.values()
for boat in boats:
try:
supabase.table(‘exhibition_history’).insert({
‘venue_id’: venue_id,
‘place’: VENUE_NAMES.get(venue_id, venue_id),
‘race_no’: p[‘race_number’],
‘lane’: boat.get(‘racer_boat_number’),
‘exhibition_time’: boat.get(‘racer_exhibition_time’),
‘start_timing’: boat.get(‘racer_start_timing’),
‘date’: yesterday
}).execute()
except Exception as e:
log_error(’exhibition保存エラー: ’ + str(e))

# ============================

# データ読み込み

# ============================

def load_players(venue_id, race_no):
supabase = get_supabase()
res = supabase.table(‘players’).select(’*’).eq(‘date’, today_str()).eq(‘venue_id’, int(venue_id)).eq(‘race_no’, int(race_no)).execute()
seen = {}
for p in (res.data or []):
lane = str(p.get(‘lane’, ‘’))
if lane and lane not in seen:
seen[lane] = p
return seen

def load_weather(venue_id):
supabase = get_supabase()
res = supabase.table(‘weather’).select(’*’).eq(‘venue_id’, int(venue_id)).eq(‘date’, today_str()).execute()
return res.data[0] if res.data else {}

def load_track_bias(venue_id):
supabase = get_supabase()
res = supabase.table(‘track_bias’).select(’*’).eq(‘venue_id’, int(venue_id)).execute()
return res.data[0] if res.data else {}

def load_weights():
supabase = get_supabase()
res = supabase.table(‘weights’).select(’*’).eq(‘id’, 1).execute()
if res.data:
return res.data[0]
return {‘player_weight’: 1.0, ‘motor_weight’: 1.0, ‘weather_weight’: 0.5, ‘track_weight’: 0.5, ‘scenario_weight’: 1.0}

# ============================

# 予想ロジック

# ============================

def analyze_scenario(player, motor, weather, bias):
def safe(d, key, default=0):
v = d.get(key) if d else None
return float(v) if v is not None else float(default)

```
course = player.get('course', 1) or 1
nige_score = sashi_score = makuri_score = makurizashi_score = sotonobi_score = 0

if course == 1:
    nige_score = safe(player, 'start_quality', 50) + safe(motor, 'torque', 50)
elif course == 2:
    sashi_score = safe(player, 'turn_skill', 50) + safe(weather, 'wind_power', 0)
elif course == 3:
    makuri_score = safe(player, 'aggressive', 50) + safe(motor, 'straight_speed', 50)
elif course == 4:
    makurizashi_score = safe(player, 'turn_skill', 50) + safe(motor, 'accel', 50)
elif course in [5, 6]:
    sotonobi_score = safe(motor, 'stretch', 50)

scenario_total = nige_score + sashi_score + makuri_score + makurizashi_score + sotonobi_score
return {'nige': nige_score, 'sashi': sashi_score, 'makuri': makuri_score,
        'makurizashi': makurizashi_score, 'sotonobi': sotonobi_score, 'scenario_total': scenario_total}
```

def build_features(player, motor, weather, bias):
scenario = analyze_scenario(player, motor, weather, bias)
course = player.get(‘course’, 1)
course_score = {1: 100, 2: 60, 3: 55, 4: 50, 5: 30, 6: 20}.get(course, 30)
class_num = player.get(‘class’) or 3
class_bonus = {1: 20, 2: 10, 3: 0, 4: -10}.get(class_num, 0)
motor_score = motor.get(‘motor_score’, 50) or 50
wind_power = weather.get(‘wind’, 0) or 0
wind_score = max(0, 10 - wind_power)
bias_value = bias.get(‘bias_value’, 0) or 0
return {
‘ability’: course_score + class_bonus,
‘start_quality’: 0, ‘turn_skill’: course_score * 0.5,
‘aggressive’: course_score * 0.3, ‘motor_score’: motor_score,
‘torque’: motor_score, ‘straight_speed’: motor_score,
‘accel’: motor_score, ‘stretch’: motor_score,
‘wind_power’: wind_score, ‘wind_direction’: 0,
‘bias_value’: bias_value, ‘scenario_total’: scenario[‘scenario_total’],
‘exhibition_score’: 0,
}

def calculate_score(features):
weights = load_weights()
player_score = (features.get(‘ability’, 50) + features.get(‘start_quality’, 0) +
features.get(‘turn_skill’, 40) + features.get(‘aggressive’, 35)) * weights.get(‘player_weight’, 1.0)
motor_score = features.get(‘motor_score’, 50) * weights.get(‘motor_weight’, 1.0)
weather_score = features.get(‘wind_power’, 0) * weights.get(‘weather_weight’, 0.5)
track_score = features.get(‘bias_value’, 0) * weights.get(‘track_weight’, 0.5)
scenario_score = features.get(‘scenario_total’, 0) * weights.get(‘scenario_weight’, 1.0)
total = player_score + motor_score + weather_score + track_score + scenario_score
return {‘player_score’: player_score, ‘motor_score’: motor_score,
‘weather_score’: weather_score, ‘track_score’: track_score,
‘scenario_score’: scenario_score, ‘total_score’: total}

def label_score(total_score):
if total_score >= 290:
return ‘鉄板’
elif total_score >= 260:
return ‘買い’
elif total_score >= 220:
return ‘穴’
return ‘スルー’

def predict_race(venue_id, race_no):
players = load_players(venue_id, race_no)
motors = {}
weather = load_weather(venue_id) or {}
bias = load_track_bias(venue_id) or {}
predictions = []
for lane in range(1, 7):
player = players.get(str(lane), {})
motor = motors.get(str(lane), {})
player[‘course’] = lane
features = build_features(player, motor, weather, bias)
score_dict = calculate_score(features)
total_score = score_dict[‘total_score’]
label = label_score(total_score)
predictions.append({
‘player_id’: player.get(‘racer_number’),
‘player_name’: player.get(‘name’, ‘unknown’),
‘course’: lane, ‘lane’: lane,
‘score’: total_score, ‘label’: label
})
return predictions

# ============================

# 買い目選定

# ============================

def calc_confidence(score, min_score, max_score, label):
score_range = max_score - min_score if max_score != min_score else 1
normalized = (score - min_score) / score_range
if label == ‘鉄板’:
return min(92, 70 + int(normalized * 22))
elif label == ‘買い’:
return min(82, 60 + int(normalized * 22))
return min(72, 50 + int(normalized * 22))

def select_bets(predictions):
if not predictions:
return []
scores = [p.get(‘score’, 0) for p in predictions]
min_score, max_score = min(scores), max(scores)
tessan = [p for p in predictions if p.get(‘label’) == ‘鉄板’]
kai = [p for p in predictions if p.get(‘label’) == ‘買い’]
ana = [p for p in predictions if p.get(‘label’) == ‘穴’]
bets = []
if tessan:
best = max(tessan, key=lambda x: x.get(‘score’, 0))
bets.append({‘type’: ‘鉄板’, ‘course’: best[‘course’], ‘player_name’: best[‘player_name’],
‘score’: best[‘score’], ‘confidence’: calc_confidence(best[‘score’], min_score, max_score, ‘鉄板’)})
if kai and len(bets) < 2:
best_kai = max(kai, key=lambda x: x.get(‘score’, 0))
bets.append({‘type’: ‘買い’, ‘course’: best_kai[‘course’], ‘player_name’: best_kai[‘player_name’],
‘score’: best_kai[‘score’], ‘confidence’: calc_confidence(best_kai[‘score’], min_score, max_score, ‘買い’)})
if ana and tessan:
best_ana = max(ana, key=lambda x: x.get(‘score’, 0))
bets.append({‘type’: ‘穴’, ‘course’: best_ana[‘course’], ‘player_name’: best_ana[‘player_name’],
‘score’: best_ana[‘score’], ‘confidence’: calc_confidence(best_ana[‘score’], min_score, max_score, ‘穴’)})
filtered = []
for b in bets:
if b[‘type’] == ‘鉄板’ and b[‘confidence’] >= 85:
filtered.append(b)
elif b[‘type’] == ‘買い’ and b[‘confidence’] >= 75:
filtered.append(b)
elif b[‘type’] == ‘穴’ and b[‘confidence’] >= 70:
filtered.append(b)
if not any(b[‘type’] == ‘鉄板’ for b in filtered):
return []
sorted_scores = sorted(scores, reverse=True)
if len(sorted_scores) >= 2 and sorted_scores[0] - sorted_scores[1] < 80:
return []
return filtered

def build_sanrentan(bets, predictions):
if not bets:
return []
sorted_preds = sorted(predictions, key=lambda x: x.get(‘score’, 0), reverse=True)
top_courses = [str(p[‘course’]) for p in sorted_preds]
bet_courses = {b[‘type’]: str(b[‘course’]) for b in bets}
sanrentan = []
if ‘鉄板’ in bet_courses:
t = bet_courses[‘鉄板’]
others = [c for c in top_courses if c != t]
conf = next(b[‘confidence’] for b in bets if b[‘type’] == ‘鉄板’)
sanrentan.append({‘label’: ‘鉄板’, ‘line’: t + ‘-’ + others[0] + ‘-’ + others[1], ‘confidence’: conf})
if ‘買い’ in bet_courses:
t = bet_courses.get(‘鉄板’, top_courses[0])
others = [c for c in top_courses if c != t]
conf = next(b[‘confidence’] for b in bets if b[‘type’] == ‘買い’)
sanrentan.append({‘label’: ‘買い’, ‘line’: t + ‘-’ + others[1] + ‘-’ + others[0], ‘confidence’: conf})
if ‘穴’ in bet_courses:
a = bet_courses[‘穴’]
t = bet_courses.get(‘鉄板’, top_courses[0])
others = [c for c in top_courses if c != a and c != t]
conf = next(b[‘confidence’] for b in bets if b[‘type’] == ‘穴’)
sanrentan.append({‘label’: ‘穴’, ‘line’: a + ‘-’ + t + ‘-’ + (others[0] if others else top_courses[0]), ‘confidence’: conf})
return sanrentan

# ============================

# フォーマット

# ============================

def format_venue_prediction(venue_name, race_predictions, weather=None):
today = datetime.now().strftime(’%Y/%m/%d’)
header = ‘【’ + venue_name + ’ ’ + today + ‘の買い目】\n’
if weather and ((weather.get(‘wind’, 0) or 0) + (weather.get(‘temperature’, 0) or 0)) > 0:
header += ‘風向:’ + str(weather.get(‘wind_direction’, ‘不明’) or ‘不明’) + ‘\n’
header += ‘風速:’ + str(weather.get(‘wind’, 0) or 0) + ‘m\n’
header += ‘波高:’ + str(weather.get(‘wave’, 0) or 0) + ‘cm\n’
header += ‘気温:’ + str(weather.get(‘temperature’, 0) or 0) + ‘C\n’

```
race_blocks = []
summary_lines = ['【買い目まとめ】']
has_any_bet = False

for race_no, predictions in race_predictions:
    bets = select_bets(predictions)
    sanrentan = build_sanrentan(bets, predictions)
    block = str(race_no) + 'R\n'
    sorted_preds = sorted(predictions, key=lambda x: x.get('score', 0), reverse=True)
    for rank, p in enumerate(sorted_preds[:3], 1):
        block += str(rank) + '位:' + str(p['course']) + '号艇 ' + p['player_name'] + '(' + str(round(p['score'], 1)) + ')\n'
    if sanrentan:
        has_any_bet = True
        for s in sanrentan:
            block += s['label'] + ':' + s['line'] + '(' + str(s['confidence']) + '%)\n'
            summary_lines.append(str(race_no) + 'R ' + s['label'] + ':' + s['line'])
    else:
        block += 'スルー\n'
    race_blocks.append(block)

# 6R単位で分割
messages = []
chunk_size = 6
for i in range(0, len(race_blocks), chunk_size):
    chunk = race_blocks[i:i + chunk_size]
    if i == 0:
        msg = header + '\n' + '\n'.join(chunk)
    else:
        msg = '【' + venue_name + ' 続き(' + str(i + 1) + 'R～)】\n\n' + '\n'.join(chunk)
    if msg.strip():
        messages.append(msg.strip())

if has_any_bet and messages:
    summary = '\n'.join(summary_lines)
    if len(messages[-1]) + len(summary) < 4800:
        messages[-1] += '\n\n' + summary
    else:
        messages.append(summary)

return messages
```

# ============================

# 前日成績通知

# ============================

def build_daily_report():
supabase = get_supabase()
yesterday = get_yesterday()
res = supabase.table(‘results’).select(’*’).eq(‘date’, yesterday).execute()
results = res.data or []
if not results:
return ‘【前日成績】\nデータなし’
total = len(results)
lines = [’【前日成績 ’ + yesterday + ‘】’, ‘対象: ’ + str(total) + ‘R\n’]
venue_data = {}
all_first = {}
for r in results:
place = r.get(‘place’, ‘不明’)
if place not in venue_data:
venue_data[place] = {‘total’: 0, ‘first_count’: {}}
venue_data[place][‘total’] += 1
first = r.get(‘first’)
if first:
venue_data[place][‘first_count’][first] = venue_data[place][‘first_count’].get(first, 0) + 1
all_first[first] = all_first.get(first, 0) + 1
for place, data in sorted(venue_data.items()):
lines.append(place + ‘: ’ + str(data[‘total’]) + ‘R’)
for course in sorted(data[‘first_count’].keys()):
cnt = data[‘first_count’][course]
pct = round(cnt / data[‘total’] * 100, 1)
lines.append(’  ’ + str(course) + ‘号艇: ’ + str(cnt) + ‘回(’ + str(pct) + ‘%)’)
lines.append(’\n全体1着:’)
for course in sorted(all_first.keys()):
pct = round(all_first[course] / total * 100, 1)
lines.append(str(course) + ’号艇: ’ + str(all_first[course]) + ‘回(’ + str(pct) + ‘%)’)
return ‘\n’.join(lines)

# ============================

# system_status管理

# ============================

def get_system_status():
supabase = get_supabase()
res = supabase.table(‘system_status’).select(’*’).eq(‘id’, 1).execute()
return res.data[0] if res.data else None

def update_status(is_active=None, current_task=None, progress=None):
supabase = get_supabase()
data = {}
if is_active is not None:
data[‘is_active’] = is_active
if current_task is not None:
data[‘current_task’] = current_task
if progress is not None:
data[‘progress’] = progress
if data:
supabase.table(‘system_status’).update(data).eq(‘id’, 1).execute()

# ============================

# タスク処理

# ============================

def task_fetch_results():
log_info(‘夜のデータ取得開始’)
results = fetch_results_api()
if results:
save_results(results)
log_info(’結果保存完了: ’ + str(len(results)) + ‘件’)
previews = fetch_previews_api()
if previews:
save_exhibition(previews)
log_info(‘展示タイム保存完了’)
log_info(‘夜のデータ取得完了’)

def task_nightly_learning():
log_info(‘夜の学習開始’)
send_line_message(build_daily_report())
log_info(‘夜の学習完了’)

def task_fetch_data():
log_info(‘出走表取得開始’)
programs = fetch_programs()
if not programs:
log_error(‘出走表データなし’)
return
save_today_races(programs)
save_players(programs)
save_weather_records(programs)
log_info(’出走表取得完了: ’ + str(len(programs)) + ‘件’)

def task_morning_prediction():
log_info(‘予想開始’)
status = get_system_status()
if not status or not status.get(‘is_active’):
log_info(‘システム停止中’)
return
supabase = get_supabase()
res = supabase.table(‘today_races’).select(’*’).eq(‘date’, today_str()).execute()
races = res.data or []
if not races:
send_line_message(’【予想なし】本日のレースはありません。’)
return
venues = {}
for r in races:
vid = str(r[‘venue_id’])
if vid not in venues:
venues[vid] = {‘venue_name’: r[‘venue_name’], ‘races’: []}
if r[‘race_no’] not in venues[vid][‘races’]:
venues[vid][‘races’].append(r[‘race_no’])
update_status(current_task=‘prediction’)
for venue_id, venue_data in venues.items():
venue_name = venue_data[‘venue_name’]
race_nos = sorted(venue_data[‘races’])
weather = load_weather(venue_id) or {}
race_predictions = []
for race_no in race_nos:
predictions = predict_race(venue_id, race_no)
race_predictions.append((race_no, predictions))
messages = format_venue_prediction(venue_name, race_predictions, weather)
for message in messages:
if message:
send_line_message(message)
log_info(venue_name + ’ 予想送信完了’)
send_line_message(’【予想完了】全場送信しました。’)
update_status(current_task=None, progress=0)
log_info(‘予想完了’)

# ============================

# スケジューラ

# ============================

SCHEDULE = [
{‘time’: ‘02:30’, ‘task’: ‘fetch_results’},
{‘time’: ‘03:00’, ‘task’: ‘nightly_learning’},
{‘time’: ‘12:00’, ‘task’: ‘fetch_data’},
{‘time’: ‘12:00’, ‘task’: ‘morning_prediction’},
]

TASK_MAP = {
‘fetch_results’: task_fetch_results,
‘nightly_learning’: task_nightly_learning,
‘fetch_data’: task_fetch_data,
‘morning_prediction’: task_morning_prediction,
}

def run_task(task_name):
log_info(’タスク開始: ’ + task_name)
try:
TASK_MAP[task_name]()
except Exception as e:
log_error(’タスクエラー ’ + task_name + ’: ’ + str(e))
log_info(’タスク完了: ’ + task_name)

def run_scheduler():
log_info(‘スケジューラ起動’)
log_info(‘スケジュール: ’ + str([s[‘time’] + ’ ’ + s[‘task’] for s in SCHEDULE]))
executed = set()
while True:
now = datetime.now().strftime(’%H:%M’)
for item in SCHEDULE:
key = item[‘time’] + ‘_’ + item[‘task’]
if now == item[‘time’] and key not in executed:
executed.add(key)
log_info(’実行: ’ + item[‘task’])
t = threading.Thread(target=run_task, args=(item[‘task’],))
t.daemon = True
t.start()
if now == ‘00:01’:
executed.clear()
time.sleep(30)

if **name** == ‘**main**’:
if len(sys.argv) > 1:
task = sys.argv[1]
if task in TASK_MAP:
run_task(task)
else:
print(’不明なタスク: ’ + task)
else:
run_scheduler()