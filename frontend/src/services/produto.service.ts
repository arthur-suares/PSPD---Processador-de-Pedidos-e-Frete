import axios from "axios";

const API_URL = "http://localhost:4000";

export interface Produto {
  id?: string;
  nome: string;
  descricao: string;
  preco: string;
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
