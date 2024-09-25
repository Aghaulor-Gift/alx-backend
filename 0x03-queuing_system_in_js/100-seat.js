import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';
import kue from 'kue';

// Initialize the Express app
const app = express();
const port = 1245;

// Initialize Redis client
const redisClient = createClient();
const reserveSeatAsync = promisify(redisClient.set).bind(redisClient);
const getAvailableSeatsAsync = promisify(redisClient.get).bind(redisClient);

// Initialize Kue queue
const queue = kue.createQueue();

// Set initial available seats to 50
const INITIAL_SEATS = 50;
let reservationEnabled = true;

(async () => {
    await reserveSeatAsync('available_seats', INITIAL_SEATS);
})();

// Function to get current available seats
async function getCurrentAvailableSeats() {
    const availableSeats = await getAvailableSeatsAsync('available_seats');
    return availableSeats ? parseInt(availableSeats) : 0;
}

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }

    const job = queue.create('reserve_seat', {}).save((err) => {
        if (!err) {
            return res.json({ status: 'Reservation in process' });
        } else {
            return res.json({ status: 'Reservation failed' });
        }
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

// Process the queue for seat reservations
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        try {
            const availableSeats = await getCurrentAvailableSeats();
            const newAvailableSeats = availableSeats - 1;

            await reserveSeatAsync('available_seats', newAvailableSeats);

            if (newAvailableSeats === 0) {
                reservationEnabled = false;
            }

            done(); // Job successful
        } catch (error) {
            done(new Error('Not enough seats available')); // Job failed
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
