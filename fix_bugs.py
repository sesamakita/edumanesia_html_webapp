import subprocess, json

TABLE = 'Edumanesia_Dashboard'

def update(key, expr, names, values):
    r = subprocess.run([
        'aws', 'dynamodb', 'update-item',
        '--table-name', TABLE,
        '--key', json.dumps(key),
        '--update-expression', expr,
        '--expression-attribute-names', json.dumps(names),
        '--expression-attribute-values', json.dumps(values),
    ], capture_output=True, text=True)
    rid = key['regency_id']['S']
    dt  = key['data_type']['S']
    if r.returncode == 0:
        print(f"  OK  {rid}/{dt}")
    else:
        print(f"  ERR {rid}/{dt}: {r.stderr.strip()}")

def s(v): return {'S': str(v)}
def n(v): return {'N': str(v)}
def ln(arr): return {'L': [{'N': str(x)} for x in arr]}
def ls(arr): return {'L': [{'S': str(x)} for x in arr]}

print("=" * 55)
print("FIX BUG 1: sarpras_baik/sedang/kritis Banggai Laut")
print("  Masalah: 7 nilai tapi hanya 6 chart_labels")
print("  Fix: Tambah label 'Bokan Kep.' & sesuaikan data")
print("=" * 55)

# Banggai Laut chart_labels harus 7 (tambah Bokan Kepulauan)
# sarpras_baik/sedang/kritis sudah 7 nilai, tinggal fix labels + dept_asn/honor
update(
    key={'regency_id': s('banggai_laut'), 'data_type': s('statistik_kpi')},
    expr='SET #cl = :cl, #da = :da, #dh = :dh',
    names={
        '#cl': 'chart_labels',
        '#da': 'dept_asn',
        '#dh': 'dept_honor',
    },
    values={
        ':cl': ls(['Banggai', 'B. Utara', 'B. Tengah', 'B. Selatan', 'Bokan Kep.', 'Labobo', 'Bangkurung']),
        ':da': ln([420, 380, 320, 280, 180, 120, 80]),
        ':dh': ln([80, 120, 180, 220, 320, 380, 420]),
    }
)

print("\n" + "=" * 55)
print("FIX BUG 2: chart_bos_tren Poso tidak sinkron")
print("  Seed lama: [45,52,68,74]")
print("  JS fallback: [14,32,52,74.2]")
print("  Fix: Seragamkan ke nilai realistis [14,32,52,74]")
print("=" * 55)

update(
    key={'regency_id': s('poso'), 'data_type': s('statistik_kpi')},
    expr='SET #bt = :bt',
    names={'#bt': 'chart_bos_tren'},
    values={':bt': ln([14, 32, 52, 74])}
)

# Seragamkan juga BL agar konsisten (seed_all_charts vs REGION_CONFIG berbeda tipis)
update(
    key={'regency_id': s('banggai_laut'), 'data_type': s('statistik_kpi')},
    expr='SET #bt = :bt',
    names={'#bt': 'chart_bos_tren'},
    values={':bt': ln([30, 42, 55, 60])}
)

print("\nSelesai fix bug!")
