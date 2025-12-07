import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import Home from "./pages/Home/Home";
import Product from "./pages/Product/Product";
import Cadastro from "./pages/Cadastro/Cadastro";
import produtoService from "./services/produto.service";
import celular from "./assets/images/celular.jpg";

interface Produto {
  id: string;
  nome: string;
  descricao: string;
  preco: number;
  estoque?: {
    quantidade: number;
    localizacoes: string;
  } | null;
}

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  description: string; // Agora sempre string, não opcional
  stock: number;
}

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProdutos = async () => {
      try {
        // console.log("🔍 Buscando produtos da API...");
        const data = await produtoService.getProdutosComEstoque();
        // console.log("✅ Produtos recebidos:", data);
        
        // Mapear produtos do backend para o formato esperado pelo frontend
        const mappedProducts: Product[] = data.map((produto: Produto, index: number) => ({
          id: index + 1, // Usar index como ID numérico para o frontend
          name: produto.nome,
          price: produto.preco,
          image: celular, // Usar imagem padrão por enquanto
          description: produto.descricao || "Sem descrição", // Garantir que sempre tenha descrição
          stock: produto.estoque?.quantidade || 0, // Pegar quantidade real do estoque
          realId: produto.id, // Guardar ID real do banco
        }));
        
        console.log("📦 Produtos mapeados:", mappedProducts);
        setProducts(mappedProducts);
      } catch (error) {
        console.error("❌ Erro ao buscar produtos:", error);
        // Em caso de erro, usar produtos vazios
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchProdutos();
  }, []);

  if (loading) {
    return (
      <div style={{ 
        display: "flex", 
        justifyContent: "center", 
        alignItems: "center", 
        height: "100vh",
        fontSize: "20px",
        color: "#BE6E46"
      }}>
        Carregando produtos...
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home products={products} />} />
        <Route path="/product/:id" element={<Product products={products} />} />
        <Route path="/cadastro" element={<Cadastro />} />
      </Routes>
    </Router>
  );
}

export default App;
