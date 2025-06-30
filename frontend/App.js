const API = "https://homeproduct-backend.onrender.com/";
const token = localStorage.getItem("token");

const headers = {
  "Content-Type": "application/json",
  ...(token ? { Authorization: token } : {})
};

const loadProducts = async () => {
  const res = await fetch(API);
  const data = await res.json();
  document.getElementById("products").innerHTML =
    data.map(p =>
      `<div class="product">
         <b>${p.name}</b> – ₹${p.price}
         <button onclick="editProduct('${p._id}', '${p.name}', ${p.price})">✏️</button>
         <button onclick="deleteProduct('${p._id}')">🗑️</button>
       </div>`
    ).join("");
};

const form = document.getElementById("productForm");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = document.getElementById("productId").value;
  const payload = {
    name: document.getElementById("name").value,
    price: Number(document.getElementById("price").value)
  };
  const method = id ? "PUT" : "POST";
  const url = id ? `${API}/${id}` : API;

  await fetch(url, {
    method,
    headers,
    body: JSON.stringify(payload)
  });
  form.reset();
  loadProducts();
});

const editProduct = (id, name, price) => {
  document.getElementById("productId").value = id;
  document.getElementById("name").value = name;
  document.getElementById("price").value = price;
};

const deleteProduct = async (id) => {
  await fetch(`${API}/${id}`, {
    method: "DELETE",
    headers
  });
  loadProducts();
};

loadProducts();
