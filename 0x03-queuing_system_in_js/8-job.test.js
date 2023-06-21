import { createQueue } from "kue";
import { expect } from "chai";
import createPushNotificationsJobs from "./8-job";
import sinon from "sinon";

const queue = createQueue();

describe('createPushNotificationsJobs', () => {
  //const consoleClone = sinon.spy(console);

  before(function() {
    queue.testMode.enter();
  });

  afterEach(function() {
    //consoleClone.log.resetHistory();
    queue.testMode.clear();
  });

  after(function() {
    //queue.testMode.clear();
    queue.testMode.exit()
  });

  it('display a error message if jobs is not an array', () => {
    const list = 'Hello world';
    expect(function(){createPushNotificationsJobs(list, queue);}).to.throw('Jobs is not an array');
    expect(queue.testMode.jobs.length).to.equal(0);
  });

  it('create two new jobs to the queue', function() {
    //this.timeout(5000);
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4109875780',
        message: 'This is the code 2457 to verify your account'
      }
    ];
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(list[0]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data.message).to.equal('This is the code 2457 to verify your account');
    /*queue.process('push_notification_code_3', () => {
      expect(
        consoleClone.log
          .calledWith('Notification job created:', queue.testMode.jobs[0].id)
      ).to.be.true;
      done();
    }); */
  });
/*
  it('registers the progress event handler for a job', (done) => {
    queue.testMode.jobs[0].addListener('progress', () => {
      expect(
        consoleClone.log
          .calledWith('Notification job', queue.testMode.jobs[0].id, '25% complete')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('progress', 25);
  });

  it('registers the failed event handler for a job', (done) => {
    queue.testMode.jobs[0].addListener('failed', () => {
      expect(
        consoleClone.log
          .calledWith('Notification job', queue.testMode.jobs[0].id, 'failed:', 'Failed to send')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('registers the complete event handler for a job', (done) => {
    queue.testMode.jobs[0].addListener('complete', () => {
      expect(
        consoleClone.log
          .calledWith('Notification job', queue.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('complete');
  }); */
});
