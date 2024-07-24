import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Import the CSS file for styling

const App = () => {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");

  // Fetch items from the API on component mount
  useEffect(() => {
    fetchItems();
  }, []);

  // Function to fetch items from the API
  const fetchItems = async () => {
    try {
      const response = await axios.get("http://localhost:5000/items");
      console.log("Fetched items:", response.data); // Log fetched items for debugging

      // Assuming each item is an array with [id, name, quantity, price]
      const formattedItems = response.data.map(itemArray => ({
        id: itemArray[0],
        name: itemArray[1],
        quantity: itemArray[2],
        price: itemArray[3]
      }));

      setItems(formattedItems);
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

  // Function to add a new item
  const addItem = async () => {
    if (!name || !quantity || !price) {
      alert("Please fill in all fields.");
      return;
    }

    const newItem = { name, quantity: Number(quantity), price: Number(price) };
    try {
      await axios.post("http://localhost:5000/items", newItem);
      fetchItems();
      setName("");
      setQuantity("");
      setPrice("");
    } catch (error) {
      console.error("Error adding item:", error);
    }
  };

  // Function to delete an item
  const deleteItem = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/items/${id}`);
      fetchItems();
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src="logo.svg" className="App-logo" alt="logo" />
        <h1>Inventario</h1>
        <div className="form-container">
          <input
            className="form-input"
            type="text"
            placeholder="Nombre"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            className="form-input"
            type="number"
            placeholder="Cantidad"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          />
          <input
            className="form-input"
            type="number"
            placeholder="Precio"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
          <button className="form-button" onClick={addItem}>
            Agregar
          </button>
        </div>
        <ul className="item-list">
          {items.map((item) => (
            <li key={item.id} className="item-list-item">
              {item.name} - {item.quantity} - ${item.price}
              <button
                className="item-list-button"
                onClick={() => deleteItem(item.id)}
              >
                Eliminar
              </button>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
};

export default App;
