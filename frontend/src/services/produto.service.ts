import axios from "axios";

const API_URL = "http://localhost:4000";

export interface Produto {
  id?: string;
  nome: string;
  descricao: string;
  preco: string;
  estoque?: {
    quantidade: number;
    localizacoes: string;
  };
}

const produtoService = {
  // Criar novo produto
  postProduto: async (produto: Produto) => {
    const response = await axios.post(`${API_URL}/criarProduto`, produto);
    return response.data;
  },

  // Buscar todos os produtos
  getProdutos: async () => {
    const response = await axios.get(`${API_URL}/produtos`);
    return response.data;
  },

  // Buscar todos os produtos com estoque
  getProdutosComEstoque: async () => {
    const produtosResponse = await axios.get(`${API_URL}/produtos`);
    const produtos = produtosResponse.data;
    
    // Buscar estoque para cada produto
    const produtosComEstoque = await Promise.all(
      produtos.map(async (produto: any) => {
        try {
          const produtoComEstoque = await axios.get(`${API_URL}/produto/${produto.id}`);
          return produtoComEstoque.data;
        } catch (error) {
          // Se falhar ao buscar estoque, retorna produto sem estoque
          return { ...produto, estoque: null };
        }
      })
    );
    
    return produtosComEstoque;
  },

  // Buscar produto por ID
  getProdutoById: async (id: number | string) => {
    const response = await axios.get(`${API_URL}/produto/${id}`);
    return response.data;
  },

  // Deletar produto por ID
  deleteProduto: async (id: number | string) => {
    const response = await axios.delete(`${API_URL}/produto/${id}`);
    return response.data;
  },
};

export default produtoService;
