import json, os, re

with open('release.json', 'r') as f:
    data = json.load(f)

print('tag_name:', data.get('tag_name', '(없음)'))
print('message:', data.get('message', '(없음)'))

version = data.get('tag_name', 'unknown').lstrip('v')
notes = data.get('body', '') or ''

# 'YouTube X.XX requires iOS ~' 줄부터 아래 전체 제거
notes = re.split(r'YouTube\s+[\d.]+\s+requires\s+iOS', notes)[0].rstrip()

with open(os.environ['GITHUB_ENV'], 'a') as f:
    f.write('TWEAK_VERSION=' + version + '\n')

with open('release_notes.md', 'w') as f:
    f.write(notes)

print('TWEAK_VERSION:', version)
print('release_notes.md written (' + str(len(notes)) + ' chars)')
