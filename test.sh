#!/bin/bash


#curl -j -b cookies.txt -c cookies.txt http://127.0.0.1:5000/
#curl -b cookies.txt -c cookies.txt -d '{"message": ""}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat
#curl -b cookies.txt -c cookies.txt http://127.0.0.1:5000/dropsession


curl -j -b cookies.txt -c cookies.txt http://127.0.0.1:5000/

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"message": "initialize"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "name", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "Samanvay Kumar"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "name", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "Samanvay Kumar"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "is_nickname", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "is_nickname", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"


echo "curl -b cookies.txt -c cookies.txt -d '{"question": "nickname", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "Samanvay"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "nickname", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "Samanvay"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "birthday", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "17-07-1993"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"
curl -b cookies.txt -c cookies.txt -d '{"question": "birthday", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "17-07-1993"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "is_time_for_more", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "is_time_for_more", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "phone", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "9999999999"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "phone", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "9999999999"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "color", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "blue"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "color", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "blue"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "type_of_salon", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "type_of_salon", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "is_reservation_now", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "is_reservation_now", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "date", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "22-05-2019"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "date", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "22-05-2019"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

echo "curl -b cookies.txt -c cookies.txt -d '{"question": "service", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat"

printf "\n\n"

curl -b cookies.txt -c cookies.txt -d '{"question": "service", "token": "1", "user": "102", "ip":"w.x.y.z", "message": "1"}' -H "Content-Type: application/json" -X POST  http://127.0.0.1:5000/chat

printf "\n\n"

curl -b cookies.txt -c cookies.txt http://127.0.0.1:5000/dropsession

printf "\n\n"
