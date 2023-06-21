const createPushNotificationsJobs = (jobs, queue) => {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  } else {
    for (let i = 0; i < jobs.length; i++) {
      let job = queue.create('push_notification_code_3', jobs[i]);
      job.save((err) => {
        if(!err) console.log(`Notification job created: ${job.id}`);
      });
      
      job.on('complete', (result) => {
        console.log(`Notification ${job.id} completed`);
      }).on('failed', (errMessage) => {
        console.log(`Notification job ${job.id} failed: ${errMessage}`);
      }).on('progress', (progress, result) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
    }
  }
}

export default createPushNotificationsJobs;
