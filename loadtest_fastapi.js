import http from "k6/http";
import { check, sleep } from "k6";
import { randomItem } from "https://jslib.k6.io/k6-utils/1.2.0/index.js";

export const options = {
  vus: 10,  // Number of virtual users
  duration: "1m",  // Test duration
};

const texts = [
  "This is a sample input",
  "Another test sentence",
  "BERT inference test"
];
const url = "http://0.0.0.0:8080/infer";

export default function () {
  const payload = JSON.stringify({
    texts: [randomItem(texts), randomItem(texts)] 
  });

  const headers = { "Content-Type": "application/json" };
  const res = http.post(url, payload, { headers });

  check(res, {
    "is status 200": (r) => r.status === 200,
  });

  sleep(1); 
}
