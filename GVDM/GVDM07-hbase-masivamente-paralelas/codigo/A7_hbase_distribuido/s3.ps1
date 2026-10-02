Clear-Host
Write-Host "PS> docker compose exec namenode hdfs dfs -ls -R /hbase/data/default" -ForegroundColor Yellow
docker compose exec namenode hdfs dfs -ls /hbase /hbase/data/default/clientes_dist 2>$null
Write-Host "`nPS> docker compose exec namenode hdfs dfs -du -s -h /hbase" -ForegroundColor Yellow
docker compose exec namenode hdfs dfs -du -s -h /hbase 2>$null
Write-Host "`nPS> docker compose exec zk1 zkCli.sh ls /hbase/rs" -ForegroundColor Yellow
docker compose exec zk1 zkCli.sh -server localhost:2181 ls /hbase/rs 2>$null | Select-Object -Last 1
