import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const setNewSchool = (schoolName, value) => {
  client.SET(schoolName, value, print);
}

const clientGet = promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
  try {
    const data = await clientGet(schoolName);
    console.log(data);
  } catch (err) {
    throw err;
  }
}

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
