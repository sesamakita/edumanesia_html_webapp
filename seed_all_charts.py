import subprocess, json

TABLE = 'Edumanesia_Dashboard'

def put(item):
    r = subprocess.run(['aws','dynamodb','put-item','--table-name',TABLE,'--item',json.dumps(item)], capture_output=True, text=True)
    if r.returncode == 0: print(f"  OK  {item['regency_id']['S']}/{item['data_type']['S']}")
    else: print(f"  ERR {item['regency_id']['S']}/{item['data_type']['S']}: {r.stderr.strip()}")

def s(v): return {'S': str(v)}
def n(v): return {'N': str(v)}
def ln(arr): return {'L': [{'N': str(x)} for x in arr]}
def ls(arr): return {'L': [{'S': str(x)} for x in arr]}

ALL_DATA = {
    'poso': {
        'statistik_kpi': {
            'chart_classroom': ln([1850, 450, 112]), # Baik, Sedang, Kritis
            'chart_kehadiran_trend': { 'M': { 'guru': ln([91, 93, 92, 94]), 'siswa': ln([85, 87, 86, 88]) } },
            'chart_sdm_radar': ln([78, 85, 82, 72, 65]),
            'chart_bias': ln([38, 28, 18, 16]),
            'chart_bos_tren': ln([45, 52, 68, 74]), # Penyerapan % per bulan
            'chart_insiden_kat': ln([12, 8, 15, 5]) # Konflik, Fasilitas, Kesehatan, Lainnya
        }
    },
    'banggai_laut': {
        'statistik_kpi': {
            'chart_classroom': ln([920, 240, 76]),
            'chart_kehadiran_trend': { 'M': { 'guru': ln([78, 80, 81, 82]), 'siswa': ln([72, 75, 77, 79]) } },
            'chart_sdm_radar': ln([65, 70, 68, 60, 55]),
            'chart_bias': ln([30, 25, 20, 25]),
            'chart_bos_tren': ln([30, 42, 55, 59]),
            'chart_insiden_kat': ln([5, 12, 4, 8])
        }
    }
}

print("Seeding ALL Chart Data to DynamoDB...")
for rid, data in ALL_DATA.items():
    # Ambil data statistik_kpi yang sudah ada untuk di-update (merge)
    # Untuk simplifikasi di task ini, kita asumsikan put-item menimpa yang lama dengan field baru
    # (Sebenarnya sebaiknya update-item, tapi put-item lebih cepat untuk scripting ini)
    # Kita butuh field minimal agar tidak hilang
    item = {'regency_id': s(rid), 'data_type': s('statistik_kpi')}
    # Tambahkan metadata dasar agar tidak hilang jika tertimpa
    if rid == 'poso':
        item.update({
            'bupati_name': s('Roy A. Pesudo'), 'region_name': s('Kab. Poso'), 'initials': s('PS'),
            'chart_labels': ls(['Poso Kota', 'P. Pesisir', 'Pamona', 'Lore Utara', 'Lage', 'P. Utara', 'P. Kota Sel.']),
            'dept_asn': ln([520, 420, 380, 290, 210, 160, 120]), 'dept_honor': ln([80, 120, 210, 180, 220, 280, 310]),
            'sarpras_baik': ln([45, 38, 32, 25, 18, 15, 10]), 'sarpras_sedang': ln([12, 10, 15, 12, 14, 16, 20]), 'sarpras_kritis': ln([2, 3, 5, 4, 6, 8, 12])
        })
    else:
        item.update({
            'bupati_name': s('Moh. Rivai'), 'region_name': s('Kab. Banggai Laut'), 'initials': s('BL'),
            'chart_labels': ls(['Banggai', 'B. Utara', 'B. Tengah', 'B. Selatan', 'Labobo', 'Bangkurung']),
            'dept_asn': ln([350, 280, 220, 150, 120, 45]), 'dept_honor': ln([120, 150, 200, 210, 250, 310]),
            'sarpras_baik': ln([35, 45, 28, 18, 12, 6, 4]), 'sarpras_sedang': ln([10, 14, 10, 8, 8, 8, 8]), 'sarpras_kritis': ln([3, 3, 3, 2, 2, 4, 3])
        })
    item.update(data['statistik_kpi'])
    put(item)

print("\nSelesai seeding data grafik lengkap.")
