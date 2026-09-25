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

# 메인 트윅 선택
main_tweak = None
if is_true('INPUT_YTKACE'):
    main_tweak = 'YTKACE'
elif is_true('INPUT_YOUMOD'):
    main_tweak = 'YouMod'
elif is_true('INPUT_YTPLUS'):
    main_tweak = f"YTPlus v{os.environ.get('TWEAK_VERSION_OVERRIDE', version)}"

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
    ('YTHoldForSpeed',          'INPUT_YTHOLD'),
]

included = []
if main_tweak:
    included.append(main_tweak)
included += [name for name, flag in TWEAK_FLAGS if is_true(flag)]

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

full_notes = (notes + '\n\n' + footer).strip() if notes else footer

with open('release_notes.md', 'w') as f:
    f.write(full_notes)

print('TWEAK_VERSION:', version)
print('release_notes.md written (' + str(len(full_notes)) + ' chars)')
