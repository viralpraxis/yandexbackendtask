# !/bin/sh

for i in {1..100}; do
  curl -X POST -H "Content-Type: application/json" --data "{'data': [{'courier_id': $i, 'courier_type': 'foot', 'regions': [1, 2, 3], 'working_hours': ['10:00-12:00']}]}" \
    "http://127.0.0.1:8000/couriers"
done
