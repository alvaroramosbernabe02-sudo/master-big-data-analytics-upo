Clear-Host
Write-Host "PS> docker compose exec hmaster hbase shell -n /work/prueba.hb" -ForegroundColor Yellow
docker compose exec hmaster hbase shell -n /work/prueba.hb 2>$null | Select-String -NotMatch -Pattern "SLF4J|^\s*$|WARN"
