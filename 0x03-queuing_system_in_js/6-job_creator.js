import { createQueue } from "kue";

const queue = createQueue();

const jobObject = {
  'phoneNumber': "4153518780",
  'message': "This is the code to verify your account",
}

let job = queue.create('push_notification_code', jobObject).save((err) => {
  if(!err) console.log(`Notification job created: ${job.id}`);
});

job.on('complete', (result) => {
  console.log('Notification job completed');
}).on('failed', (errMessage) => {
  console.log('Notification job failed');
});
