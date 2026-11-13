#!/bin/sh

PORT_FILE="/tmp/gluetun/forwarded_port"
LAST_PORT=""

while true; do
    if [ -s "$PORT_FILE" ]; then
        PORT="$(cat "$PORT_FILE")"

        if [ "$PORT" != "$LAST_PORT" ]; then
            echo "Trying to set qBittorrent listening port to $PORT on tun0"

            until wget -qO- \
                --post-data "json={\"listen_port\":${PORT},\"current_network_interface\":\"tun0\",\"current_interface_address\":\"\",\"random_port\":false,\"upnp\":false}" \
                http://127.0.0.1:8081/api/v2/app/setPreferences
            do
                echo "qBittorrent WebUI not ready yet, retrying..."
                sleep 3
            done

            echo "qBittorrent listening port set to $PORT on tun0"
            LAST_PORT="$PORT"
        fi
    fi

    sleep 10
done
