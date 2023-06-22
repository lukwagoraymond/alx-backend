import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();

const port = 1245;

const client = createClient();
client
.on('error', err => {
  console.log(`Redis client not connected to the server: ${err}`);
})
.on('connect', () => {
  console.log('Redis client connected to the server');
});

const listProducts = [
  {Id: 1, name: 'Suitcase 250', price: 50, stock: 4},
  {Id: 2, name: 'Suitcase 450', price: 100, stock: 10},
  {Id: 3, name: 'Suitcase 650', price: 350, stock: 2},
  {Id: 4, name: 'Suitcase 1050', price: 550, stock: 5},
]

const getItemById = (id) => {
  const productItem = listProducts.find((product) => product.Id === id);
  return productItem;
}

const reserveStockById = (itemId, stock) => {
  client.SET(`item.${itemId}`, stock);
}

const clientGet = promisify(client.get).bind(client);

const getCurrentReservedStockById = async (itemId) => {
  try {
    const data = await clientGet(`item.${itemId}`);
    return data;
  } catch (err) {
    throw new Error(err);
  }
}

app.get('/list_products', (req, res) => {
  const modifiedArr = listProducts.map((obj) => {
    const arr=  {
      itemId: obj.Id,
      itemName: obj.name,
      price: obj.price,
      initialAvailableQuantity: obj.stock,
    }
    return arr;
  });
  res.send(JSON.stringify(modifiedArr));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const productItem = getItemById(Number.parseInt(itemId));
  if (!productItem) {
    res.json({ status: "Product not found" });
    return;
  } else {
    const reservedStock = await getCurrentReservedStockById(itemId);
    const data =  {
      itemId: productItem.Id,
      itemName: productItem.name,
      price: productItem.price,
      initialAvailableQuantity: productItem.stock,
      currentQuantity: productItem.stock - (Number.parseInt(reservedStock) || 0)
    }
    res.json(data);
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const productItem = getItemById(itemId);
  if (!productItem) {
    res.json({ status: "Product not found" });
    return;
  }
  if (productItem) {
    if (productItem.stock < 1) {
      res.json({ status: "Not enough stock available", itemId: `${itemId}` });
    } else {
      reserveStockById(itemId, 1);
      res.json({ status: "Reservation confirmed", itemId: `${itemId}` });
    }
  }
});

app.listen(port, () => {
  console.log(`Project app listening on port ${port}`)
});
