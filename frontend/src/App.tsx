import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import Product from "./pages/Product/Product";
import celular from "./assets/images/celular.jpg";


const products = [
  { 
    id: 1, 
    name: "Produto A", 
    price: 49.9, 
    image: celular, 
    description: "Descrição do Produto A", 
    stock: 12 
  },
  { 
    id: 2, 
    name: "Produto B", 
    price: 79.9, 
    image: celular, 
    description: "Descrição do Produto B", 
    stock: 0 
  },
  { 
    id: 3, 
    name: "Produto C", 
    price: 29.9, 
    image: celular, 
    description: "Descrição do Produto C", 
    stock: 5 
  },
  { 
    id: 4, 
    name: "Produto D", 
    price: 29.9, 
    image: celular, 
    description: "Descrição do Produto D", 
    stock: 3 
  },
  { 
    id: 5, 
    name: "Produto E", 
    price: 29.9, 
    image: celular, 
    description: "Descrição do Produto E", 
    stock: 0 
  },
  { 
    id: 6, 
    name: "Produto F", 
    price: 29.9, 
    image: celular, 
    description: "Descrição do Produto F", 
    stock: 8 
  },
];

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home products={products} />} />
        <Route path="/product/:id" element={<Product products={products} />} />
      </Routes>
    </Router>
  );
}

export default App;
