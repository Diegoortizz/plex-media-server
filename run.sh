docker compose -f /home/diego/htpc-download-box/docker-compose.yml down 
docker compose -f /home/diego/htpc-download-box/docker-compose.yml up vpn -d
sleep 20
docker compose -f /home/diego/htpc-download-box/docker-compose.yml up flaresolverr -d
sleep 20
docker compose -f /home/diego/htpc-download-box/docker-compose.yml up jackett -d
sleep 60
docker compose -f /home/diego/htpc-download-box/docker-compose.yml up qbittorrent -d
sleep 30
docker compose -f /home/diego/htpc-download-box/docker-compose.yml up radarr sonarr plex-server overseerr -d
