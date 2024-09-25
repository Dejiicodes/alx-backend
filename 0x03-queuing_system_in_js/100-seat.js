const express = require('express');
const kue = require('kue');
const { promisify } = require('util');
const redis = require('redis');

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

const queue = kue.createQueue();
const app = express();
const PORT = 1245;

let reservationEnabled = true;

// Function to reserve a seat
const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

// Function to get current available seats
const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return parseInt(seats, 10);
};

// Initialize the number of available seats
const initializeSeats = async () => {
    await reserveSeat(50);
};

// Express routes
app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }

    const job = queue.create('reserve_seat', {}).save((err) => {
        if (err) return res.json({ status: "Reservation failed" });
        res.json({ status: "Reservation in process" });
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

app.get('/process', async (req, res) => {
    res.json({ status: "Queue processing" });
    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();
        if (availableSeats > 0) {
            await reserveSeat(availableSeats - 1);
            if (availableSeats - 1 === 0) {
                reservationEnabled = false;
            }
            done();
        } else {
            done(new Error('Not enough seats available'));
        }
    });
});

// Start the server
initializeSeats().then(() => {
    app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}`);
    });
});
