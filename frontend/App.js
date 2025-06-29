const apiUrl = "https://homeproduct-backend.onrender.com/";

async function fetchProducts() {
  const res = await fetch(apiUrl);
  const products = await res.json();
  const container = document.getElementById('products');
  container.innerHTML = "";
  products.forEach(p => {
    const div = document.createElement('div');
    div.className = "product";
    div.innerHTML = `
      <strong>${p.name}</strong> - ₹${p.price} <br>
      <button onclick="editProduct(${p.id}, '${p.name}', ${p.price})">Edit</button>
      <button onclick="deleteProduct(${p.id})">Delete</button>
    `;
    container.appendChild(div);
  });
}

async function deleteProduct(id) {
  await fetch(`${apiUrl}/${id}`, { method: 'DELETE' });
  fetchProducts();
}

function editProduct(id, name, price) {
  document.getElementById('productId').value = id;
  document.getElementById('name').value = name;
  document.getElementById('price').value = price;
}

document.getElementById('productForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const id = document.getElementById('productId').value;
  const name = document.getElementById('name').value;
  const price = document.getElementById('price').value;
  const payload = { name, price: parseInt(price) };

  if (id) {
    await fetch(`${apiUrl}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } else {
    await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  document.getElementById('productForm').reset();
  fetchProducts();
});

fetchProducts();
