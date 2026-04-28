import subprocess, json

TABLE = 'Edumanesia_Dashboard'

def put(item):
    r = subprocess.run(
        ['aws','dynamodb','put-item','--table-name',TABLE,'--item',json.dumps(item)],
        capture_output=True, text=True
    )
    dt = item.get('data_type',{}).get('S','?')
    rid = item.get('regency_id',{}).get('S','?')
    if r.returncode == 0:
        print(f"  OK  {rid}/{dt}")
    else:
        print(f"  ERR {rid}/{dt}: {r.stderr.strip()}")

def s(v): return {'S': str(v)}
def n(v): return {'N': str(v)}
def l(arr): return {'L': arr}
def m(d):  return {'M': d}

# Helper to convert list of numbers to DynamoDB List of Numbers
def ln(arr): return {'L': [{'N': str(x)} for x in arr]}
def ls(arr): return {'L': [{'S': str(x)} for x in arr]}

ALL_DATA = {
    'poso': {
        'statistik_kpi': {
            'bupati_name': s('Roy A. Pesudo'), 'region_name': s('Kab. Poso'),
            'initials': s('PS'), 'greeting': s('Selamat Pagi, Roy A. Pesudo'),
            'region_desc': s('Monitoring data agregat pendidikan Kabupaten Poso secara komprehensif melalui Edumanesia Intelligence.'),
            'chart_labels': ls(['Poso Kota', 'P. Pesisir', 'Pamona', 'Lore Utara', 'Lage', 'P. Utara', 'P. Kota Sel.']),
            'dept_asn': ln([520, 420, 380, 290, 210, 160, 120]),
            'dept_honor': ln([80, 120, 210, 180, 220, 280, 310]),
            'sarpras_baik': ln([45, 38, 32, 25, 18, 15, 10]),
            'sarpras_sedang': ln([12, 10, 15, 12, 14, 16, 20]),
            'sarpras_kritis': ln([2, 3, 5, 4, 6, 8, 12]),
            'health_score': s('88.2'), 'health_grade': s('A'),
            'guru_pct': n(94), 'guru_abs': s('7.842 / 8.350'),
            'siswa_pct': n(88), 'siswa_abs': s('142.500'),
            'tu_pct': n(96), 'tu_abs': s('1.240'),
            'total_sekolah': n(460), 'sekolah_lapor': n(452),
            'ai_rek': s('Alokasikan DAK Sisa Semester 1 sebesar Rp 8.2 Miliar untuk 3 sekolah zona kritis di Kec. Poso Kota Selatan dan Pamona Utara.')
        }
    },
    'banggai_laut': {
        'statistik_kpi': {
            'bupati_name': s('Moh. Rivai'), 'region_name': s('Kab. Banggai Laut'),
            'initials': s('BL'), 'greeting': s('Selamat Pagi, Moh. Rivai'),
            'region_desc': s('Monitoring data agregat pendidikan Kabupaten Banggai Laut secara komprehensif melalui Edumanesia Intelligence.'),
            'chart_labels': ls(['Banggai', 'B. Utara', 'B. Tengah', 'B. Selatan', 'Labobo', 'Bangkurung']),
            'dept_asn': ln([350, 280, 220, 150, 120, 45]),
            'dept_honor': ln([120, 150, 200, 210, 250, 310]),
            'sarpras_baik': ln([35, 45, 28, 18, 12, 6, 4]),
            'sarpras_sedang': ln([10, 14, 10, 8, 8, 8, 8]),
            'sarpras_kritis': ln([3, 3, 3, 2, 2, 4, 3]),
            'health_score': s('81.5'), 'health_grade': s('B'),
            'guru_pct': n(82), 'guru_abs': s('4.510 / 5.500'),
            'siswa_pct': n(79), 'siswa_abs': s('67.200'),
            'tu_pct': n(91), 'tu_abs': s('680'),
            'total_sekolah': n(333), 'sekolah_lapor': n(298),
            'ai_rek': s('Alokasikan DAK Sisa Semester 1 sebesar Rp 4.2 Miliar untuk 2 sekolah zona kritis di Kec. Labobo dan Bangkurung.')
        }
    }
}

print("Updating Chart Data in DynamoDB...")
for region, data_types in ALL_DATA.items():
    for data_type, fields in data_types.items():
        item = {'regency_id': s(region), 'data_type': s(data_type)}
        item.update(fields)
        put(item)

print("\nSelesai memperbarui data grafik.")
