const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({ region: 'ap-southeast-1' });
const dynamo = DynamoDBDocumentClient.from(client);

const TABLE_NAME = 'Edumanesia_Dashboard';

const dataToInsertPoso = {
    'kecamatanData': [
        { name: 'Poso Kota', sekolah: 48, guru: 96, siswa: 91, status: 'Baik' },
        { name: 'Poso Pesisir', sekolah: 32, guru: 94, siswa: 89, status: 'Baik' },
        { name: 'Pamona Puselemba', sekolah: 41, guru: 91, siswa: 87, status: 'Cukup' },
        { name: 'Lore Utara', sekolah: 28, guru: 89, siswa: 84, status: 'Cukup' },
        { name: 'Lage', sekolah: 22, guru: 86, siswa: 80, status: 'Cukup' },
        { name: 'Poso Kota Selatan', sekolah: 18, guru: 74, siswa: 71, status: 'Kritis' },
        { name: 'Pamona Utara', sekolah: 15, guru: 78, siswa: 69, status: 'Kritis' }
    ],
    'alertSchools': [
        { name: 'SMPN 1 Pamona Utara', kec: 'Pamona Utara', guru: 62, siswa: 58, type: 'critical' },
        { name: 'SDN 3 Poso Kota Selatan', kec: 'Poso Kota Selatan', guru: 70, siswa: 65, type: 'critical' },
        { name: 'SDN 7 Lage', kec: 'Lage', guru: 75, siswa: 72, type: 'warning' },
        { name: 'SMPN 2 Lore Utara', kec: 'Lore Utara', guru: 78, siswa: 76, type: 'warning' },
        { name: 'SDN 12 Pamona Puselemba', kec: 'Pamona Puselemba', guru: 80, siswa: 79, type: 'warning' }
    ],
    'dakData': [
        { name: 'Pengadaan Furnitur Sekolah', pct: 92, color: '#10B981', anggaran: 'Rp 8.4M', status: 'Selesai' },
        { name: 'Renovasi Ruang Kelas', pct: 75, color: '#4F46E5', anggaran: 'Rp 22.6M', status: 'Berjalan' },
        { name: 'Laboratorium IPA', pct: 60, color: '#3B82F6', anggaran: 'Rp 14.2M', status: 'Berjalan' },
        { name: 'Sanitasi & Toilet Sekolah', pct: 48, color: '#F59E0B', anggaran: 'Rp 9.8M', status: 'Proses' },
        { name: 'Perpustakaan Digital', pct: 30, color: '#EC4899', anggaran: 'Rp 7.4M', status: 'Proses' }
    ],
    'stuntingData': [
        { kec: 'Poso Kota Selatan', pct: 5.2, count: 94, color: '#EF4444' },
        { kec: 'Pamona Utara', pct: 4.1, count: 76, color: '#F59E0B' },
        { kec: 'Lage', pct: 3.0, count: 58, color: '#F59E0B' },
        { kec: 'Lore Utara', pct: 2.1, count: 42, color: '#3B82F6' },
        { kec: 'Pamona Puselemba', pct: 1.4, count: 28, color: '#10B981' },
        { kec: 'Poso Kota', pct: 0.8, count: 14, color: '#10B981' }
    ],
    'kesehatanPrograms': [
        { title: 'UKS Aktif', value: '382 Sekolah', pct: 83, color: '#10B981', icon: 'local_hospital', desc: 'Termasuk 12 yang baru diaktifkan' },
        { title: 'PMT Berjalan', value: '210 Sekolah', pct: 46, color: '#3B82F6', icon: 'restaurant', desc: 'Makanan Tambahan Bergizi' },
        { title: 'Siswa Tervaksin', value: '117.420', pct: 82, color: '#8B5CF6', icon: 'vaccines', desc: 'Dari target 143.000 siswa' }
    ]
};

const dataToInsertBanggai = {
    'kecamatanData': [
        { name: 'Banggai', sekolah: 42, guru: 95, siswa: 92, status: 'Baik' },
        { name: 'Banggai Utara', sekolah: 28, guru: 92, siswa: 88, status: 'Baik' },
        { name: 'Banggai Selatan', sekolah: 35, guru: 88, siswa: 85, status: 'Cukup' },
        { name: 'Banggai Tengah', sekolah: 25, guru: 85, siswa: 82, status: 'Cukup' },
        { name: 'Bokan Kepulauan', sekolah: 18, guru: 75, siswa: 70, status: 'Kritis' },
        { name: 'Labobo', sekolah: 15, guru: 72, siswa: 68, status: 'Kritis' },
        { name: 'Bangkurung', sekolah: 12, guru: 68, siswa: 65, status: 'Kritis' }
    ],
    'alertSchools': [
        { name: 'SMPN 1 Bokan Kepulauan', kec: 'Bokan Kepulauan', guru: 65, siswa: 60, type: 'critical' },
        { name: 'SDN 2 Labobo', kec: 'Labobo', guru: 68, siswa: 62, type: 'critical' },
        { name: 'SDN 5 Bangkurung', kec: 'Bangkurung', guru: 70, siswa: 68, type: 'warning' },
        { name: 'SMPN 3 Banggai Selatan', kec: 'Banggai Selatan', guru: 75, siswa: 72, type: 'warning' },
        { name: 'SDN 1 Banggai Tengah', kec: 'Banggai Tengah', guru: 78, siswa: 75, type: 'warning' }
    ],
    'dakData': [
        { name: 'Pembangunan Ruang Kelas Baru', pct: 85, color: '#10B981', anggaran: 'Rp 12.5M', status: 'Selesai' },
        { name: 'Rehabilitasi Perpustakaan', pct: 60, color: '#4F46E5', anggaran: 'Rp 5.2M', status: 'Berjalan' },
        { name: 'Pengadaan TIK Sekolah', pct: 45, color: '#3B82F6', anggaran: 'Rp 8.8M', status: 'Berjalan' },
        { name: 'Pembangunan Laboratorium IPA', pct: 30, color: '#F59E0B', anggaran: 'Rp 15.4M', status: 'Proses' },
        { name: 'Pengadaan Alat Peraga Edukatif', pct: 15, color: '#EC4899', anggaran: 'Rp 3.6M', status: 'Proses' }
    ],
    'stuntingData': [
        { kec: 'Bokan Kepulauan', pct: 6.5, count: 120, color: '#EF4444' },
        { kec: 'Bangkurung', pct: 5.2, count: 85, color: '#F59E0B' },
        { kec: 'Labobo', pct: 4.8, count: 72, color: '#F59E0B' },
        { kec: 'Banggai Selatan', pct: 3.5, count: 60, color: '#3B82F6' },
        { kec: 'Banggai Tengah', pct: 2.2, count: 45, color: '#10B981' },
        { kec: 'Banggai Utara', pct: 1.5, count: 25, color: '#10B981' },
        { kec: 'Banggai', pct: 0.8, count: 15, color: '#10B981' }
    ],
    'kesehatanPrograms': [
        { title: 'UKS Aktif', value: '250 Sekolah', pct: 75, color: '#10B981', icon: 'local_hospital', desc: 'Dari total 333 sekolah' },
        { title: 'PMT Berjalan', value: '180 Sekolah', pct: 54, color: '#3B82F6', icon: 'restaurant', desc: 'Program Makanan Tambahan' },
        { title: 'Siswa Tervaksin', value: '85.200', pct: 88, color: '#8B5CF6', icon: 'vaccines', desc: 'Dari target 96.800 siswa' }
    ]
};

async function seed(regency, data) {
    for (const [key, value] of Object.entries(data)) {
        console.log(`Inserting ${key} for ${regency}...`);
        const command = new PutCommand({
            TableName: TABLE_NAME,
            Item: {
                regency_id: regency,
                data_type: key,
                data: value
            }
        });
        await dynamo.send(command);
    }
}

async function run() {
    await seed('poso', dataToInsertPoso);
    await seed('banggai', dataToInsertBanggai);
    console.log('All dummy data inserted successfully!');
}

run().catch(console.error);
