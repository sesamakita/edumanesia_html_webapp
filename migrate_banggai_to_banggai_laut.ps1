# Script Migrasi DynamoDB: banggai -> banggai_laut (via file JSON)
$TABLE_NAME = "Edumanesia_Dashboard"
$OLD_KEY = "banggai"
$NEW_KEY = "banggai_laut"

Write-Host "========================================"
Write-Host "Migrasi DynamoDB: '$OLD_KEY' -> '$NEW_KEY'"
Write-Host "========================================"

# 1. Query via file JSON
Write-Host "`n[1/3] Membaca data dari DynamoDB..."
$queryResult = aws dynamodb query `
    --table-name $TABLE_NAME `
    --key-condition-expression "regency_id = :rid" `
    --expression-attribute-values file://query_expr.json | ConvertFrom-Json

$items = $queryResult.Items
Write-Host "  Ditemukan $($items.Count) item dengan regency_id='$OLD_KEY'"

if ($items.Count -eq 0) {
    Write-Host "  Tidak ada data. Selesai."
    exit 0
}

# 2. Tulis ulang setiap item dengan regency_id baru
Write-Host "`n[2/3] Menulis item baru dengan regency_id='$NEW_KEY'..."
$counter = 0
foreach ($item in $items) {
    $dataType = $item.data_type.S
    Write-Host "  -> Menulis: $NEW_KEY / $dataType"
    
    # Ganti nilai regency_id ke key baru
    $item.regency_id = [PSCustomObject]@{ S = $NEW_KEY }
    
    # Simpan ke file temp
    $tmpFile = "tmp_item_$counter.json"
    $item | ConvertTo-Json -Depth 30 -Compress | Set-Content -Path $tmpFile -Encoding UTF8
    
    aws dynamodb put-item --table-name $TABLE_NAME --item "file://$tmpFile"
    
    Remove-Item $tmpFile -Force
    Write-Host "     [OK] $dataType"
    $counter++
}

# 3. Hapus item lama
Write-Host "`n[3/3] Menghapus item lama dengan regency_id='$OLD_KEY'..."
foreach ($item in $items) {
    $dataType = $item.data_type.S
    $deleteKeyObj = @{
        regency_id = @{ S = $OLD_KEY }
        data_type  = @{ S = $dataType }
    }
    $deleteKeyFile = "tmp_delete_key.json"
    $deleteKeyObj | ConvertTo-Json -Compress | Set-Content -Path $deleteKeyFile -Encoding UTF8
    
    Write-Host "  -> Menghapus: $OLD_KEY / $dataType"
    aws dynamodb delete-item --table-name $TABLE_NAME --key "file://$deleteKeyFile"
    Remove-Item $deleteKeyFile -Force
    Write-Host "     [OK] Dihapus"
}

Write-Host "`n========================================"
Write-Host "Migrasi selesai! '$OLD_KEY' -> '$NEW_KEY'"
Write-Host "========================================"
