const express = require('express');
const router = express.Router();

const reviews = [
  { user: 'Ravi', comment: 'Very tasty and fresh!', rating: 5 },
  { user: 'Seema', comment: 'Loved the homemade taste.', rating: 4 },
];

router.get('/', (req, res) => {
  res.json(reviews);
});

module.exports = router;
