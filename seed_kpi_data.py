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

ALL_DATA = {
    'poso': {
        'statistik_kpi': {
            'bupati_name': s('Roy A. Pesudo'), 'region_name': s('Kab. Poso'),
            'initials': s('PS'), 'greeting': s('Selamat Pagi, Roy A. Pesudo'),
            'region_desc': s('Monitoring data agregat pendidikan Kabupaten Poso secara komprehensif melalui Edumanesia Intelligence.'),
            'health_score': s('88.2'), 'health_grade': s('A'),
            'guru_pct': n(94), 'guru_abs': s('7.842 / 8.350'),
            'siswa_pct': n(88), 'siswa_abs': s('142.500'),
            'tu_pct': n(96), 'tu_abs': s('1.240'),
            'total_sekolah': n(460), 'sekolah_lapor': n(452),
            'ai_rek': s('Alokasikan DAK Sisa Semester 1 sebesar Rp 8.2 Miliar untuk 3 sekolah zona kritis di Kec. Poso Kota Selatan dan Pamona Utara.')
        },
        'sarpras_kpi': {
            'rusak_berat': n(45), 'rusak_sedang': n(112),
            'serapan_dak': n(68.4), 'proyek_count': n(28),
            'proyek_nilai': s('Rp 42.6 Miliar'), 'total_dak': s('Rp 62.4 Miliar')
        },
        'sdm_kpi': {
            'total_ptk': n(8350), 'asn_count': n(5120), 'asn_pct': s('61.3%'),
            'honor_count': n(3230), 'honor_pct': s('38.7%'), 'pensiun': n(184)
        },
        'kesehatan_kpi': {
            'bias': n(94.2), 'stunting': n(312), 'kek': n(128),
            'uks_aktif': n(382), 'uks_pct': s('83%')
        },
        'bos_kpi': {
            'bos_total': n(186), 'bos_salur': n(138), 'bos_gauge': n(74.2),
            'bos_serapat': s('74.2%'), 'bos_lapor': n(8), 'bos_audit': n(3),
            'bos_rp_salur': s('Rp 138M'), 'bos_rp_sisa': s('Rp 48M')
        },
        'insiden_kpi': {
            'ins_kritis': n(3), 'ins_waspada': n(7),
            'ins_info': n(12), 'sla_avg': n(42)
        },
        'redZone': {'data': l([
            m({'name':s('SDN 4 Poso Kota Selatan'),'kec':s('Poso Kota Selatan'),'kondisi':s('Kritis'),'kerusakan':s('Atap ambruk 3 ruang kelas'),'est':s('Rp 2.1M')}),
            m({'name':s('SDN 7 Lage'),'kec':s('Lage'),'kondisi':s('Kritis'),'kerusakan':s('Pondasi retak, berbahaya'),'est':s('Rp 3.4M')}),
            m({'name':s('SMPN 2 Pamona Utara'),'kec':s('Pamona Utara'),'kondisi':s('Berat'),'kerusakan':s('Dinding luar rusak parah'),'est':s('Rp 1.8M')}),
            m({'name':s('SDN 12 Pamona Puselemba'),'kec':s('Pamona Puselemba'),'kondisi':s('Berat'),'kerusakan':s('Rangka atap karatan'),'est':s('Rp 1.2M')}),
        ])},
        'sdmDistricts': {'data': l([
            m({'name':s('Poso Kota'),'asn':n(520),'honor':n(80)}),
            m({'name':s('Poso Pesisir'),'asn':n(420),'honor':n(120)}),
            m({'name':s('Pamona Puselemba'),'asn':n(380),'honor':n(210)}),
            m({'name':s('Lore Utara'),'asn':n(290),'honor':n(180)}),
            m({'name':s('Lage'),'asn':n(210),'honor':n(220)}),
            m({'name':s('Pamona Utara'),'asn':n(160),'honor':n(280)}),
            m({'name':s('Poso Kota Sel.'),'asn':n(120),'honor':n(310)}),
        ])},
        'bosCompliance': {'data': l([
            m({'kec':s('Poso Kota'),'pct':n(100),'lapor':n(48),'total':n(48)}),
            m({'kec':s('Poso Pesisir'),'pct':n(97),'lapor':n(31),'total':n(32)}),
            m({'kec':s('Pamona Puselemba'),'pct':n(95),'lapor':n(39),'total':n(41)}),
            m({'kec':s('Lore Utara'),'pct':n(93),'lapor':n(26),'total':n(28)}),
            m({'kec':s('Lage'),'pct':n(86),'lapor':n(19),'total':n(22)}),
            m({'kec':s('Pamona Utara'),'pct':n(80),'lapor':n(12),'total':n(15)}),
            m({'kec':s('Poso Kota Sel.'),'pct':n(72),'lapor':n(13),'total':n(18)}),
        ])},
    },
    'banggai_laut': {
        'statistik_kpi': {
            'bupati_name': s('Moh. Rivai'), 'region_name': s('Kab. Banggai Laut'),
            'initials': s('BL'), 'greeting': s('Selamat Pagi, Moh. Rivai'),
            'region_desc': s('Monitoring data agregat pendidikan Kabupaten Banggai Laut secara komprehensif melalui Edumanesia Intelligence.'),
            'health_score': s('81.5'), 'health_grade': s('B'),
            'guru_pct': n(82), 'guru_abs': s('4.510 / 5.500'),
            'siswa_pct': n(79), 'siswa_abs': s('67.200'),
            'tu_pct': n(91), 'tu_abs': s('680'),
            'total_sekolah': n(333), 'sekolah_lapor': n(298),
            'ai_rek': s('Alokasikan DAK Sisa Semester 1 sebesar Rp 4.2 Miliar untuk 2 sekolah zona kritis di Kec. Labobo dan Bangkurung.')
        },
        'sarpras_kpi': {
            'rusak_berat': n(28), 'rusak_sedang': n(76),
            'serapan_dak': n(47), 'proyek_count': n(5),
            'proyek_nilai': s('Rp 45.5 Miliar'), 'total_dak': s('Rp 45.5 Miliar')
        },
        'sdm_kpi': {
            'total_ptk': n(5500), 'asn_count': n(2800), 'asn_pct': s('50.9%'),
            'honor_count': n(2700), 'honor_pct': s('49.1%'), 'pensiun': n(96)
        },
        'kesehatan_kpi': {
            'bias': n(88.0), 'stunting': n(357), 'kek': n(84),
            'uks_aktif': n(250), 'uks_pct': s('75%')
        },
        'bos_kpi': {
            'bos_total': n(124), 'bos_salur': n(74), 'bos_gauge': n(59.7),
            'bos_serapat': s('59.7%'), 'bos_lapor': n(14), 'bos_audit': n(5),
            'bos_rp_salur': s('Rp 74M'), 'bos_rp_sisa': s('Rp 50M')
        },
        'insiden_kpi': {
            'ins_kritis': n(2), 'ins_waspada': n(5),
            'ins_info': n(8), 'sla_avg': n(48)
        },
        'redZone': {'data': l([
            m({'name':s('SDN 2 Labobo'),'kec':s('Labobo'),'kondisi':s('Kritis'),'kerusakan':s('Ruang kelas ambruk 2 unit'),'est':s('Rp 1.8M')}),
            m({'name':s('SDN 5 Bangkurung'),'kec':s('Bangkurung'),'kondisi':s('Kritis'),'kerusakan':s('Pondasi tidak layak huni'),'est':s('Rp 2.4M')}),
            m({'name':s('SMPN 1 Bokan Kepulauan'),'kec':s('Bokan Kepulauan'),'kondisi':s('Berat'),'kerusakan':s('Dinding luar rusak parah'),'est':s('Rp 1.5M')}),
            m({'name':s('SDN 3 Banggai Selatan'),'kec':s('Banggai Selatan'),'kondisi':s('Berat'),'kerusakan':s('Rangka atap berkarat'),'est':s('Rp 0.9M')}),
        ])},
        'sdmDistricts': {'data': l([
            m({'name':s('Banggai'),'asn':n(420),'honor':n(80)}),
            m({'name':s('Banggai Utara'),'asn':n(380),'honor':n(120)}),
            m({'name':s('Banggai Tengah'),'asn':n(320),'honor':n(180)}),
            m({'name':s('Banggai Selatan'),'asn':n(280),'honor':n(220)}),
            m({'name':s('Bokan Kep.'),'asn':n(180),'honor':n(320)}),
            m({'name':s('Labobo'),'asn':n(120),'honor':n(380)}),
            m({'name':s('Bangkurung'),'asn':n(80),'honor':n(420)}),
        ])},
        'bosCompliance': {'data': l([
            m({'kec':s('Banggai'),'pct':n(100),'lapor':n(42),'total':n(42)}),
            m({'kec':s('Banggai Utara'),'pct':n(96),'lapor':n(27),'total':n(28)}),
            m({'kec':s('Banggai Tengah'),'pct':n(88),'lapor':n(22),'total':n(25)}),
            m({'kec':s('Banggai Selatan'),'pct':n(83),'lapor':n(29),'total':n(35)}),
            m({'kec':s('Bokan Kepulauan'),'pct':n(67),'lapor':n(12),'total':n(18)}),
            m({'kec':s('Labobo'),'pct':n(60),'lapor':n(9),'total':n(15)}),
            m({'kec':s('Bangkurung'),'pct':n(58),'lapor':n(7),'total':n(12)}),
        ])},
    }
}

print("Seeding DynamoDB...")
total = 0
for region, data_types in ALL_DATA.items():
    print(f"\n[{region}]")
    for data_type, fields in data_types.items():
        item = {'regency_id': s(region), 'data_type': s(data_type)}
        item.update(fields)
        put(item)
        total += 1

print(f"\nSelesai! Total {total} item di-seed.")
