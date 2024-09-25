import redis from 'redis';

const client = redis.createClient();

const CHANNEL = 'holberton school channel';

client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
  client.subscribe(CHANNEL);
});

client.on('message', (channel, message) => {
  if (channel === CHANNEL) console.log(message);

  if (message === 'KILL_SERVER') {
    client.unsubscribe(CHANNEL);
    client.quit();
  }
});
