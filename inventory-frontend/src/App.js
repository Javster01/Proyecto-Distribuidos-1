import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Asegúrate de importar el archivo CSS

const App = () => {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const response = await axios.get("http://localhost:5000/items");
    setItems(response.data);
  };

  const addItem = async () => {
    const newItem = { name, quantity, price };
    await axios.post("http://localhost:5000/items", newItem);
    fetchItems();
    setName("");
    setQuantity("");
    setPrice("");
  };

  const deleteItem = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/items/${id}`);
      fetchItems();
    } catch (error) {
      console.error("Error al borrar el elemento:", error);
      // Aquí podrías mostrar un mensaje de error al usuario, si es necesario.
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
                onClick={async () => await deleteItem(item.id)}
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
