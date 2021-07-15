require "json"
require "httparty"

requests_count = 1_0000
http_endpoint = "http://127.0.0.1:8000/couriers"
http_headers = {
  "Content-Type": "application/json"
}

def http_body(id)
  body = {}
  body["courier_id"] = id
  body["courier_type"] = "foot"
  body["regions"] = [1, 2, 3]
  body["working_hours"] = ["10:00-11:00", "12:31-14:20"]

  { data: [body] }
end

(1..requests_count).each do |i|
  response = HTTParty.post(http_endpoint, headers: http_headers, body: JSON.dump(http_body(i)))

  puts "done: #{i}" if (i % 100).zero?
end
