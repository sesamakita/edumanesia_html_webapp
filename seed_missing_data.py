import subprocess, json

TABLE = 'Edumanesia_Dashboard'

def put(item):
    r = subprocess.run(
        ['aws', 'dynamodb', 'put-item', '--table-name', TABLE, '--item', json.dumps(item)],
        capture_output=True, text=True
    )
    dt = item.get('data_type', {}).get('S', '?')
    rid = item.get('regency_id', {}).get('S', '?')
    if r.returncode == 0:
        print(f"  OK  {rid}/{dt}")
    else:
        print(f"  ERR {rid}/{dt}: {r.stderr.strip()}")

def s(v): return {'S': str(v)}
def n(v): return {'N': str(v)}
def l(arr): return {'L': arr}
def m(d): return {'M': d}

# ============================================================
# DATA POSO
# ============================================================
POSO_KECAMATAN = l([
    m({'name': s('Poso Kota'),          'sekolah': n(48),  'guru': n(96), 'siswa': n(92), 'status': s('Baik')}),
    m({'name': s('Poso Pesisir'),       'sekolah': n(32),  'guru': n(93), 'siswa': n(89), 'status': s('Baik')}),
    m({'name': s('Pamona Puselemba'),   'sekolah': n(41),  'guru': n(91), 'siswa': n(87), 'status': s('Baik')}),
    m({'name': s('Lore Utara'),         'sekolah': n(28),  'guru': n(88), 'siswa': n(84), 'status': s('Cukup')}),
    m({'name': s('Lage'),               'sekolah': n(22),  'guru': n(85), 'siswa': n(81), 'status': s('Cukup')}),
    m({'name': s('Pamona Utara'),       'sekolah': n(15),  'guru': n(79), 'siswa': n(74), 'status': s('Kritis')}),
    m({'name': s('Poso Kota Selatan'),  'sekolah': n(18),  'guru': n(76), 'siswa': n(71), 'status': s('Kritis')}),
])

POSO_ALERT_SCHOOLS = l([
    m({'name': s('SDN 7 Lage'),            'kec': s('Lage'),              'type': s('critical'), 'guru': n(62), 'siswa': n(58)}),
    m({'name': s('SDN 4 Poso Kota Sel.'),  'kec': s('Poso Kota Selatan'),'type': s('critical'), 'guru': n(65), 'siswa': n(61)}),
    m({'name': s('SMPN 2 Pamona Utara'),   'kec': s('Pamona Utara'),      'type': s('warning'),  'guru': n(74), 'siswa': n(70)}),
    m({'name': s('SDN 12 Pamona Puselb.'), 'kec': s('Pamona Puselemba'), 'type': s('warning'),  'guru': n(76), 'siswa': n(72)}),
    m({'name': s('SDN 9 Lore Utara'),      'kec': s('Lore Utara'),        'type': s('warning'),  'guru': n(78), 'siswa': n(75)}),
])

POSO_DAK_DATA = l([
    m({'name': s('Rehab Ruang Kelas SDN 4 Poso Kota Sel.'), 'anggaran': s('Rp 2.1 M'),  'pct': n(82), 'status': s('Berjalan'), 'color': s('#10B981')}),
    m({'name': s('Rehab Gedung SMPN 2 Pamona Utara'),       'anggaran': s('Rp 1.8 M'),  'pct': n(45), 'status': s('Berjalan'), 'color': s('#F59E0B')}),
    m({'name': s('Pembangunan RKB SDN 7 Lage'),              'anggaran': s('Rp 3.4 M'),  'pct': n(18), 'status': s('Berjalan'), 'color': s('#EF4444')}),
    m({'name': s('Sanitasi & Air Bersih Kec. Lore Utara'),  'anggaran': s('Rp 1.2 M'),  'pct': n(95), 'status': s('Selesai'),  'color': s('#6366F1')}),
    m({'name': s('Mebeler & Perlengkapan Kec. Pamona'),     'anggaran': s('Rp 0.9 M'),  'pct': n(100),'status': s('Selesai'),  'color': s('#6366F1')}),
])

POSO_STUNTING_DATA = l([
    m({'kec': s('Poso Kota'),          'count': n(28),  'pct': n(1.8), 'color': s('#10B981')}),
    m({'kec': s('Poso Pesisir'),       'count': n(42),  'pct': n(2.4), 'color': s('#10B981')}),
    m({'kec': s('Pamona Puselemba'),   'count': n(67),  'pct': n(3.1), 'color': s('#F59E0B')}),
    m({'kec': s('Lore Utara'),         'count': n(58),  'pct': n(3.8), 'color': s('#F59E0B')}),
    m({'kec': s('Lage'),               'count': n(52),  'pct': n(4.2), 'color': s('#EF4444')}),
    m({'kec': s('Pamona Utara'),       'count': n(45),  'pct': n(4.8), 'color': s('#EF4444')}),
    m({'kec': s('Poso Kota Selatan'),  'count': n(20),  'pct': n(2.1), 'color': s('#10B981')}),
])

POSO_KESEHATAN_PROGRAMS = l([
    m({'title': s('Program BIAS'),         'desc': s('Bulan Imunisasi Anak Sekolah'),        'icon': s('vaccines'),         'color': s('#10B981'), 'value': s('94.2%'),   'pct': n(94)}),
    m({'title': s('PMT Sekolah'),          'desc': s('Pemberian Makanan Tambahan'),          'icon': s('restaurant'),       'color': s('#3B82F6'), 'value': s('78%'),     'pct': n(78)}),
    m({'title': s('UKS Aktif'),            'desc': s('Unit Kesehatan Sekolah Berfungsi'),    'icon': s('local_hospital'),   'color': s('#8B5CF6'), 'value': s('382 UKS'), 'pct': n(83)}),
    m({'title': s('Penanganan Stunting'),  'desc': s('Intervensi Gizi Anak Bermasalah'),     'icon': s('child_care'),       'color': s('#F59E0B'), 'value': s('312 kasus'),'pct': n(68)}),
])

POSO_INCIDENTS = l([
    m({'id': n(1), 'type': s('kritis'),  'title': s('Akses Jalan Putus'),      'school': s('SDN 4 Poso Kota Selatan'), 'time': s('09:12'), 'date': s('Hari ini'), 'status': s('Ditangani'), 'icon': s('priority_high'), 'color': s('#EF4444')}),
    m({'id': n(2), 'type': s('kritis'),  'title': s('Atap Kelas Ambruk'),      'school': s('SDN 7 Lage'),              'time': s('08:45'), 'date': s('Hari ini'), 'status': s('Proses'),    'icon': s('domain_disabled'),'color': s('#EF4444')}),
    m({'id': n(3), 'type': s('kritis'),  'title': s('Gedung Kritis'),           'school': s('SMPN 2 Pamona Utara'),     'time': s('07:30'), 'date': s('Hari ini'), 'status': s('Evakuasi'),  'icon': s('warning'),       'color': s('#EF4444')}),
    m({'id': n(4), 'type': s('waspada'), 'title': s('Sengketa Lahan Sekolah'), 'school': s('SMPN 1 Poso Pesisir'),     'time': s('14:00'), 'date': s('Kemarin'),  'status': s('Investigasi'),'icon': s('gavel'),         'color': s('#F59E0B')}),
    m({'id': n(5), 'type': s('waspada'), 'title': s('Listrik Padam 4 Jam'),    'school': s('SDN 1 Poso Kota'),         'time': s('13:20'), 'date': s('Kemarin'),  'status': s('Selesai'),   'icon': s('bolt'),          'color': s('#F59E0B')}),
    m({'id': n(6), 'type': s('info'),    'title': s('Aktivasi CCTV Baru'),     'school': s('SDN 3 Pamona Puselemba'),  'time': s('08:00'), 'date': s('20 Apr'),   'status': s('Selesai'),   'icon': s('videocam'),      'color': s('#3B82F6')}),
])

POSO_SLAS = l([
    m({'type': s('Insiden Kritis'),    'target': n(30),  'actual': n(18), 'color': s('#EF4444')}),
    m({'type': s('Insiden Waspada'),   'target': n(60),  'actual': n(45), 'color': s('#F59E0B')}),
    m({'type': s('Insiden Informasi'), 'target': n(120), 'actual': n(68), 'color': s('#3B82F6')}),
])

POSO_RETIREMENT = l([
    m({'year': n(2026), 'count': n(42), 'color': s('#EF4444')}),
    m({'year': n(2027), 'count': n(58), 'color': s('#F59E0B')}),
    m({'year': n(2028), 'count': n(34), 'color': s('#F59E0B')}),
    m({'year': n(2029), 'count': n(28), 'color': s('#3B82F6')}),
    m({'year': n(2030), 'count': n(22), 'color': s('#10B981')}),
])

# ============================================================
# DATA BANGGAI LAUT
# ============================================================
BL_KECAMATAN = l([
    m({'name': s('Banggai'),             'sekolah': n(42),  'guru': n(90), 'siswa': n(86), 'status': s('Baik')}),
    m({'name': s('Banggai Utara'),       'sekolah': n(28),  'guru': n(86), 'siswa': n(82), 'status': s('Baik')}),
    m({'name': s('Banggai Tengah'),      'sekolah': n(25),  'guru': n(82), 'siswa': n(78), 'status': s('Cukup')}),
    m({'name': s('Banggai Selatan'),     'sekolah': n(35),  'guru': n(80), 'siswa': n(76), 'status': s('Cukup')}),
    m({'name': s('Bokan Kepulauan'),     'sekolah': n(18),  'guru': n(75), 'siswa': n(70), 'status': s('Kritis')}),
    m({'name': s('Labobo'),              'sekolah': n(15),  'guru': n(71), 'siswa': n(66), 'status': s('Kritis')}),
    m({'name': s('Bangkurung'),          'sekolah': n(12),  'guru': n(68), 'siswa': n(63), 'status': s('Kritis')}),
])

BL_ALERT_SCHOOLS = l([
    m({'name': s('SDN 2 Labobo'),              'kec': s('Labobo'),           'type': s('critical'), 'guru': n(58), 'siswa': n(54)}),
    m({'name': s('SDN 5 Bangkurung'),          'kec': s('Bangkurung'),       'type': s('critical'), 'guru': n(61), 'siswa': n(57)}),
    m({'name': s('SMPN 1 Bokan Kepulauan'),    'kec': s('Bokan Kepulauan'), 'type': s('warning'),  'guru': n(72), 'siswa': n(68)}),
    m({'name': s('SDN 3 Banggai Selatan'),     'kec': s('Banggai Selatan'),  'type': s('warning'),  'guru': n(75), 'siswa': n(71)}),
])

BL_DAK_DATA = l([
    m({'name': s('Rehab Ruang Kelas SDN 2 Labobo'),         'anggaran': s('Rp 1.8 M'), 'pct': n(35), 'status': s('Berjalan'), 'color': s('#EF4444')}),
    m({'name': s('Rekonstruksi SDN 5 Bangkurung'),          'anggaran': s('Rp 2.4 M'), 'pct': n(20), 'status': s('Berjalan'), 'color': s('#EF4444')}),
    m({'name': s('Rehab Dinding SMPN 1 Bokan Kep.'),        'anggaran': s('Rp 1.5 M'), 'pct': n(55), 'status': s('Berjalan'), 'color': s('#F59E0B')}),
    m({'name': s('Sanitasi Sekolah Kec. Banggai Selatan'),  'anggaran': s('Rp 0.9 M'), 'pct': n(88), 'status': s('Berjalan'), 'color': s('#10B981')}),
    m({'name': s('Perlengkapan Kelas Kec. Banggai'),        'anggaran': s('Rp 0.8 M'), 'pct': n(100),'status': s('Selesai'),  'color': s('#6366F1')}),
])

BL_STUNTING_DATA = l([
    m({'kec': s('Banggai'),           'count': n(35),  'pct': n(2.1), 'color': s('#10B981')}),
    m({'kec': s('Banggai Utara'),     'count': n(48),  'pct': n(2.8), 'color': s('#10B981')}),
    m({'kec': s('Banggai Tengah'),    'count': n(62),  'pct': n(3.5), 'color': s('#F59E0B')}),
    m({'kec': s('Banggai Selatan'),   'count': n(74),  'pct': n(4.1), 'color': s('#F59E0B')}),
    m({'kec': s('Bokan Kepulauan'),   'count': n(58),  'pct': n(4.8), 'color': s('#EF4444')}),
    m({'kec': s('Labobo'),            'count': n(52),  'pct': n(5.2), 'color': s('#EF4444')}),
    m({'kec': s('Bangkurung'),        'count': n(28),  'pct': n(4.5), 'color': s('#EF4444')}),
])

BL_KESEHATAN_PROGRAMS = l([
    m({'title': s('Program BIAS'),         'desc': s('Bulan Imunisasi Anak Sekolah'),       'icon': s('vaccines'),         'color': s('#10B981'), 'value': s('88.0%'),   'pct': n(88)}),
    m({'title': s('PMT Sekolah'),          'desc': s('Pemberian Makanan Tambahan'),         'icon': s('restaurant'),       'color': s('#3B82F6'), 'value': s('65%'),     'pct': n(65)}),
    m({'title': s('UKS Aktif'),            'desc': s('Unit Kesehatan Sekolah Berfungsi'),   'icon': s('local_hospital'),   'color': s('#8B5CF6'), 'value': s('250 UKS'), 'pct': n(75)}),
    m({'title': s('Penanganan Stunting'),  'desc': s('Intervensi Gizi Anak Bermasalah'),    'icon': s('child_care'),       'color': s('#F59E0B'), 'value': s('357 kasus'),'pct': n(54)}),
])

BL_INCIDENTS = l([
    m({'id': n(1), 'type': s('kritis'),  'title': s('Perundungan Fisik'),          'school': s('SDN 1 Banggai'),          'time': s('09:12'), 'date': s('Hari ini'), 'status': s('Ditangani'), 'icon': s('priority_high'), 'color': s('#EF4444')}),
    m({'id': n(2), 'type': s('kritis'),  'title': s('Krisis Air Bersih'),          'school': s('SMPN 1 Bokan Kepulauan'),'time': s('08:45'), 'date': s('Hari ini'), 'status': s('Proses'),    'icon': s('water_drop'),    'color': s('#EF4444')}),
    m({'id': n(3), 'type': s('kritis'),  'title': s('Gedung Nyaris Ambruk'),       'school': s('SDN 3 Bangkurung'),       'time': s('07:30'), 'date': s('Hari ini'), 'status': s('Evakuasi'),  'icon': s('domain_disabled'),'color': s('#EF4444')}),
    m({'id': n(4), 'type': s('waspada'), 'title': s('Kehilangan Peralatan Lab'),   'school': s('SMP Banggai Utara'),      'time': s('14:00'), 'date': s('Kemarin'),  'status': s('Investigasi'),'icon': s('science'),       'color': s('#F59E0B')}),
    m({'id': n(5), 'type': s('waspada'), 'title': s('Listrik Padam 3 Jam'),        'school': s('SDN 5 Banggai Tengah'),   'time': s('13:20'), 'date': s('Kemarin'),  'status': s('Selesai'),   'icon': s('bolt'),          'color': s('#F59E0B')}),
    m({'id': n(6), 'type': s('info'),    'title': s('Aktivasi CCTV Baru'),         'school': s('SDN 4 Lade'),             'time': s('08:00'), 'date': s('19 Apr'),   'status': s('Selesai'),   'icon': s('videocam'),      'color': s('#3B82F6')}),
])

BL_SLAS = l([
    m({'type': s('Insiden Kritis'),    'target': n(30),  'actual': n(24), 'color': s('#EF4444')}),
    m({'type': s('Insiden Waspada'),   'target': n(60),  'actual': n(52), 'color': s('#F59E0B')}),
    m({'type': s('Insiden Informasi'), 'target': n(120), 'actual': n(95), 'color': s('#3B82F6')}),
])

BL_RETIREMENT = l([
    m({'year': n(2026), 'count': n(28), 'color': s('#EF4444')}),
    m({'year': n(2027), 'count': n(45), 'color': s('#F59E0B')}),
    m({'year': n(2028), 'count': n(21), 'color': s('#F59E0B')}),
    m({'year': n(2029), 'count': n(18), 'color': s('#3B82F6')}),
    m({'year': n(2030), 'count': n(12), 'color': s('#10B981')}),
])

# ============================================================
# SEED ALL ITEMS
# ============================================================
items = [
    # POSO — variabel yang belum ada
    {'regency_id': s('poso'), 'data_type': s('kecamatanData'),      'data': POSO_KECAMATAN},
    {'regency_id': s('poso'), 'data_type': s('alertSchools'),       'data': POSO_ALERT_SCHOOLS},
    {'regency_id': s('poso'), 'data_type': s('dakData'),            'data': POSO_DAK_DATA},
    {'regency_id': s('poso'), 'data_type': s('stuntingData'),       'data': POSO_STUNTING_DATA},
    {'regency_id': s('poso'), 'data_type': s('kesehatanPrograms'),  'data': POSO_KESEHATAN_PROGRAMS},
    {'regency_id': s('poso'), 'data_type': s('incidents'),          'data': POSO_INCIDENTS},
    {'regency_id': s('poso'), 'data_type': s('slas'),               'data': POSO_SLAS},
    {'regency_id': s('poso'), 'data_type': s('retirementYears'),    'data': POSO_RETIREMENT},

    # BANGGAI LAUT — variabel yang belum ada
    {'regency_id': s('banggai_laut'), 'data_type': s('kecamatanData'),      'data': BL_KECAMATAN},
    {'regency_id': s('banggai_laut'), 'data_type': s('alertSchools'),       'data': BL_ALERT_SCHOOLS},
    {'regency_id': s('banggai_laut'), 'data_type': s('dakData'),            'data': BL_DAK_DATA},
    {'regency_id': s('banggai_laut'), 'data_type': s('stuntingData'),       'data': BL_STUNTING_DATA},
    {'regency_id': s('banggai_laut'), 'data_type': s('kesehatanPrograms'),  'data': BL_KESEHATAN_PROGRAMS},
    {'regency_id': s('banggai_laut'), 'data_type': s('incidents'),          'data': BL_INCIDENTS},
    {'regency_id': s('banggai_laut'), 'data_type': s('slas'),               'data': BL_SLAS},
    {'regency_id': s('banggai_laut'), 'data_type': s('retirementYears'),    'data': BL_RETIREMENT},
]

print("Seeding missing DynamoDB data...\n")
for item in items:
    put(item)

print(f"\nSelesai! Total {len(items)} item baru di-seed.")
print("\nCatatan: Jalankan juga fix_bugs.py untuk memperbaiki inkonsistensi data yang ada.")
