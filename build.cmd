docker rm -f ir_table
docker build . -t nikobraz/ir_table:develop
docker push nikobraz/ir_table:develop
docker compose up -d
echo http://127.0.0.1:5000