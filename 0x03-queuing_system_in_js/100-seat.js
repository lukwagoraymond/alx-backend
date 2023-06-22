import express from 'express';
import { createClient } from "redis";
import { createQueue } from "kue";
import { promisify } from 'util';

const app = express();
const port = 1245;
const client = createClient();
const queue = createQueue();
let reservationEnabled = true;

const reserveSeat = (number) => {
  client.SET('available_seats', number);
}

const clientGet = promisify(client.get).bind(client);
const getCurrentAvailableSeats = async() => {
  try {
    const data = await clientGet('available_seats');
    return data;
  } catch(err) {
    throw err;
  }
}

app.get('/available_seats', async(req, res) => {
  const seatsAvail = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: `${seatsAvail}` });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
  } else {
    let job = queue.create('reserve_seat');
    job.save((err) => {
      if(!err) {
        res.json({ status: "Reservation in process" });
      } else {
        res.json({ status: "Reservation failed" });
      }
    });
    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });
    job.on('failed', (errMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errMessage}`);
    });
  }
});

app.get('/process', (req, res) => {
  res.json({ status: "Queue processing" });
  queue.process('reserve_seat', async(job, done) => {
    const seatsAvail = await getCurrentAvailableSeats();
    const seatsCurrent = (Number.parseInt(seatsAvail) || 0) - 1;
    reserveSeat(seatsCurrent);

    if (seatsCurrent === 0) {
      reservationEnabled = false;
    }
    if (seatsCurrent > 0) {
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(port, () => {
  console.log(`Project app listening on port ${port}`);
  reserveSeat(50);
});
