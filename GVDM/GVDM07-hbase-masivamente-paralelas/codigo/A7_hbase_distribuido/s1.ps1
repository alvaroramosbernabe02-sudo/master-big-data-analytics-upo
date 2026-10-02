Clear-Host
Write-Host "PS> docker compose ps" -ForegroundColor Yellow
docker compose ps --format "table {{.Name}}`t{{.Status}}`t{{.Ports}}"
Write-Host "`nPS> docker compose exec namenode hdfs dfsadmin -report" -ForegroundColor Yellow
docker compose exec namenode hdfs dfsadmin -report 2>$null | Select-String -Pattern "Live datanodes|^Name:|Hostname|Configured Capacity:|DFS Used:" | Select-Object -First 12
