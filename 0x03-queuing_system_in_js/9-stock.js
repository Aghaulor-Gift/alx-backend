import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Array of products
const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

// Create Redis client
const redisClient = createClient();
const reserveStockAsync = promisify(redisClient.set).bind(redisClient);
const getStockAsync = promisify(redisClient.get).bind(redisClient);

// Handle Redis connection errors
redisClient.on('error', (err) => {
    console.error(`Error: ${err}`);
});

// Data access function to get item by ID
function getItemById(id) {
    return listProducts.find(item => item.id === id);
}

// Route to get all products
app.get('/list_products', (req, res) => {
    const productsResponse = listProducts.map(({ id, name, price, stock }) => ({
        itemId: id,
        itemName: name,
        price: price,
        initialAvailableQuantity: stock
    }));
    res.json(productsResponse);
});

// Route to get product details by ID
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);

    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    }

    // Get current reserved stock
    const currentReservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = product.stock - currentReservedStock;

    res.json({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock,
        currentQuantity: currentQuantity
    });
});

// Function to reserve stock in Redis
async function reserveStockById(itemId, stock) {
    await reserveStockAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock
async function getCurrentReservedStockById(itemId) {
    const reservedStock = await getStockAsync(`item.${itemId}`);
    return reservedStock ? parseInt(reservedStock) : 0;
}

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const product = getItemById(itemId);

    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    }

    const currentReservedStock = await getCurrentReservedStockById(itemId);
    const availableStock = product.stock - currentReservedStock;

    if (availableStock <= 0) {
        return res.json({ status: 'Not enough stock available', itemId: itemId });
    }

    // Reserve the stock
    await reserveStockById(itemId, currentReservedStock + 1);
    res.json({ status: 'Reservation confirmed', itemId: itemId });
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
