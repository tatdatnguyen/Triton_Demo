import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
    vus: 5, // Number of Virtual Users
    duration: '30s', // Duration of the test
};

export default function () {
    const url = 'http://localhost:8000/v2/models/bert/infer';

    // Payload for batch input texts
    const payload = JSON.stringify({
        inputs: [
            {
                name: 'text_input',
                shape: [4], // Batch size of 4
                datatype: 'BYTES',
                data: [
                    'What is your name?',
                    'How is the weather today?',
                    'Tell me about Triton server.',
                    'hello',
                ],
            },
        ],
        outputs: [
            {
                name: 'output',
            },
        ],
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Send POST request to the Triton server
    const response = http.post(url, payload, params);

    // Validate response status
    check(response, {
        'status is 200': (r) => r.status === 200,
    });

    if (response.status === 200) {
        const result = response.json();
        if (result.outputs) {
            console.log('Predicted labels:', result.outputs[0].data);
        } else {
            console.error('Error in response:', result.error || 'Unknown error');
        }
    } else {
        console.error('Request failed with status code:', response.status);
    }

    sleep(1); // Wait for 1 second between iterations
}
