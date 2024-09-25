import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

const data = [
  {
    key: 'Portland',
    value: 50,
  },
  {
    key: 'Seattle',
    value: 80,
  },
  {
    key: 'New York',
    value: 20,
  },
  {
    key: 'Bogota',
    value: 20,
  },
  {
    key: 'Cali',
    value: 40,
  },
  {
    key: 'Paris',
    value: 2,
  },
];

client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const setHolbertonSchools = () => {
  for (const item of data) {
    client.hset('HolbertonSchools', item.key, item.value, redis.print);
  }
};

const displayHolbertonSchools = () => {
  client.hgetall('HolbertonSchools', (err, result) => {
    if (!err) console.log(result);
  });
};

(() => {
  setHolbertonSchools();
  displayHolbertonSchools();
})();
