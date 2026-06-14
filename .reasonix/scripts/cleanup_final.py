import re

# storage.py - fix all remaining issues
with open('pydme/actions/storage.py') as f:
    text = f.read()

fixes = {
    'labelmaintenancet, maintenanceeece)': 'labelmaint, maintenance)',
    'controllerr': 'controller',
    'replication)replication)': 'replication), 6 (currently',
    '6rrently meaningless': '6 (currently meaningless), 7 (currently meaningless)',
    'ROCE和TCP': 'ROCE and TCP',
    'NAS与object': 'NAS and object',
    '的Failover group busi failover group': ' failover group',
    'associateVIP type': 'associate VIP type',
    'associateNAS': 'associate NAS',
    'associateKnowledgeBase': 'associate KnowledgeBase',
    '非Preferred path': 'non-preferred path',
}
for old, new in fixes.items():
    text = text.replace(old, new)
with open('pydme/actions/storage.py', 'w') as f:
    f.write(text)
print('storage.py fixed')

# nas.py
with open('pydme/actions/nas.py') as f:
    text = f.read()
fixes_nas = {
    '仅 OceanStor Pacific  support': 'OceanStor Pacific only',
    '非WORM': 'non-WORM',
    'shrink value和Filesystem capacity': 'shrink value and filesystem capacity',
    '的 resource': ' resource',
    '有 DataTurbo 系列': 'DataTurbo series',
    '维度': 'dimension',
    '为 Zone ID': 'is the zone ID',
    'quota warning onlyft quota reached, warning only': 'quota warning only when soft quota reached',
    'supportService provisioning的 device': 'support service provisioning. Devices',
    'g device的 resource': '. Devices without support',
    'Device without supportService provisioning的 device': 'Devices without service provisioning support include',
}
for old, new in fixes_nas.items():
    text = text.replace(old, new)
with open('pydme/actions/nas.py', 'w') as f:
    f.write(text)
print('nas.py fixed')

# protect.py
with open('pydme/actions/protect.py') as f:
    text = f.read()
fixes_protect = {
    'synccing': 'syncing',
    'syncc': 'sync',
    'forr': 'for',
    'beforre': 'before',
    '和新 Pair': 'and new pair',
    '直接Split': 'directly split',
    'tion pair creationtion pair creation': 'tion pair creation',
    'Replication pair creationtion pair creationtion pair creation mode为 auto effective when': 'Effective when replication pair creation mode is auto',
}
for old, new in fixes_protect.items():
    text = text.replace(old, new)
with open('pydme/actions/protect.py', 'w') as f:
    f.write(text)
print('protect.py fixed')

# san.py
with open('pydme/actions/san.py') as f:
    text = f.read()
fixes_san = {
    'prefetchixed': 'prefetch',
    'pathath': 'path',
    '非Preferred path': 'non-preferred path',
    '倍': ' times',
}
for old, new in fixes_san.items():
    text = text.replace(old, new)
with open('pydme/actions/san.py', 'w') as f:
    f.write(text)
print('san.py fixed')

# system.py
with open('pydme/actions/system.py') as f:
    text = f.read()
fixes_system = {
    'count字': ' digit',
    '转义 character': 'escaped character',
    '特殊 character': 'special character',
    'Username和Username': 'Username and username',
}
for old, new in fixes_system.items():
    text = text.replace(old, new)
with open('pydme/actions/system.py', 'w') as f:
    f.write(text)
print('system.py fixed')

print('All done!')
