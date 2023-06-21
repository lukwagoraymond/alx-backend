import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();

const port = 1245;

const listProducts = [
  {Id: 1, name: 'Suitcase 250', price: 50, stock: 4},
  {Id: 2, name: 'Suitcase 450', price: 100, stock: 10},
  {'Id': 3, 'name': 'Suitcase 650', 'price': 350, 'stock': 2},
  {'Id': 4, 'name': 'Suitcase 1050', 'price': 550, 'stock': 5},
]

const getItemById = (id) => {
  for (let i in listProducts) {
    for (let obj in listProducts[i]) {
      if (id === listProducts.i.Id) {
        return listProducts[i];
      }
    }
  }
}

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
});
