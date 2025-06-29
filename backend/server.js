const express = require('express');
const app = express();
const port = 5000;

app.get('/', (req, res) => {
  res.send('Backend running for Home Food Product App');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});


const reviewsRouter = require('./reviews');
app.use('/api/reviews', reviewsRouter);
