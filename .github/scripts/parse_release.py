import json, os, re

with open('release.json', 'r') as f:
    data = json.load(f)

print('tag_name:', data.get('tag_name', '(없음)'))
print('message:', data.get('message', '(없음)'))

version = os.environ.get('TWEAK_VERSION_OVERRIDE') or data.get('tag_name', 'unknown').lstrip('v')
notes = data.get('body', '') or ''

# 'YouTube X.XX requires iOS ~' 줄부터 아래 전체 제거
notes = re.split(r'YouTube\s+[\d.]+\s+requires\s+iOS', notes)[0].rstrip()

with open(os.environ['GITHUB_ENV'], 'a') as f:
    f.write('TWEAK_VERSION=' + version + '\n')

# ── Included Tweaks / Plugins 푸터 생성 ──────────────────────────────
def is_true(name):
    return os.environ.get(name, '').strip().lower() == 'true'

yt_version = os.environ.get('YT_VERSION', 'unknown')

# Included Tweaks 맨 위 항목: YTKACE 또는 YouMod 중 선택된 것
main_tweak = None
if is_true('INPUT_YTKACE'):
    main_tweak = 'YTKACE'
elif is_true('INPUT_YOUMOD'):
    main_tweak = 'YouMod'

# (표시 이름, 토글 env 변수) — buildyoumod.yml에 실제 노출된 입력만 포함
# YTUHD / YouLoop는 이 워크플로에서 사용자 토글이 아니라 내부적으로 항상
# false로 고정돼 있어 목록에서 자연히 빠짐
TWEAK_FLAGS = [
    ('YTABConfig',              'INPUT_YTABCONFIG'),
    ('YouQuality',              'INPUT_YOUQUALITY'),
    ('YouChooseQuality',        'INPUT_YOUCHOOSEQUALITY'),
    ('Return YouTube Dislikes', 'INPUT_RYD'),
    ('DontEatMyContent',        'INPUT_DONTEATMYCONTENT'),
    ('YouPiP',                  'INPUT_YOUPIP'),
    ('YouSpeed',                'INPUT_YOUSPEED'),
    ('YouSlider',               'INPUT_YOUSLIDER'),
    ('YTSilentVote',            'INPUT_YTSILENTVOTE'),
    ('YTweaks',                 'INPUT_YTWEAKS'),
    ('Gonerino',                'INPUT_GONERINO'),
    ('YouGetCaption',           'INPUT_YOUGETCAPTION'),
    ('iSponsorBlock',           'INPUT_ISPONSORBLOCK'),
    ('Alderis',                 'INPUT_ALDERIS'),
]

included = []
if main_tweak:
    included.append(main_tweak)
included += [name for name, flag in TWEAK_FLAGS if is_true(flag)]

# Inject_Plugins가 켜지면 항상 Plugins/ 폴더 전체가 그대로 주입되므로
# 실제 파일 목록과 1:1로 고정
PLUGIN_NAMES = [
    'OpenYoutubeSafariExtension',
    'NotificationContentExtension',
    'NotificationServiceExtension',
    'WidgetKitExtension',
    'IntentsExtension',
    'ShareExtension',
]

footer_lines = [f'Updated to YouTube v{yt_version}', '']
if included:
    footer_lines.append('Included Tweaks :')
    footer_lines.extend(included)
    footer_lines.append('')
if is_true('INPUT_INJECT_PLUGINS'):
    footer_lines.append('Plugins :')
    footer_lines.extend(PLUGIN_NAMES)

footer = '\n'.join(footer_lines).rstrip()

# 업스트림(YTKACE 등)에서 가져온 노트가 있으면 그 아래에 이어 붙이고,
# 없으면(YouMod/YouTube 단독) 푸터만 사용
full_notes = (notes + '\n\n' + footer).strip() if notes else footer

with open('release_notes.md', 'w') as f:
    f.write(full_notes)

print('TWEAK_VERSION:', version)
print('release_notes.md written (' + str(len(full_notes)) + ' chars)')
