import React, { useState, type FormEvent } from "react";
// import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { PuffLoader } from "react-spinners";
import produtoService from "../../services/produto.service";

import { 
    Form,
    Title,
    Label,
    Input,
    TextArea,
    Button,
} from "./style";

interface Formulario {
  nome: string;
  descricao: string;
  preco: string;
}

const CardCadastro: React.FC = () => {
    const [nome, setNome] = useState<string>("");
    const [descricao, setDescricao] = useState<string>("");
    const [preco, setPreco] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);

    // const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);

        const Formulario_JSON: Formulario = { nome, descricao, preco};

        try {
            await produtoService.postProduto(Formulario_JSON);
            toast.success("Produto cadastrado com sucesso!");
        } catch (error) {
            console.error("Erro ao cadastrar o produto:", error);
            toast.error("Erro ao cadastrar o produto.");
        } finally {
            setIsLoading(false);
            // navigate("/listarProdutos");
        }
    };

    return (
        <div style={{ display: "grid", placeItems:"center" }}>
            <Form onSubmit={handleSubmit}>
                <ToastContainer /> 
                <Title>Cadastro</Title>
                <h5 style={{color: "#BE6E46", marginTop: 0}}>
                    Coloque abaixo as informações do produto a ser cadastrado!
                </h5>
                
                <Label htmlFor="name" style={{color: "#BE6E46"}}>Nome do produto</Label>
                <Input
                    type="text"
                    id="name"
                    placeholder="Nome do produto"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                />

                <Label htmlFor="message" style={{color: "#BE6E46"}}>Descrição:</Label>
                <TextArea 
                    id="message" 
                    rows={5} 
                    placeholder="Descrição" 
                    value={descricao} 
                    onChange={(e) => setDescricao(e.target.value)}
                />

                <Label htmlFor="preco" style={{color: "#BE6E46"}}>preco do produto:</Label>
                <Input
                    type="text"
                    id="preco"
                    placeholder="preço do produto"
                    inputMode="decimal"
                    pattern="^\d*\.?\d*$"
                    value={preco}
                    onChange={(e) => {
                        const val = e.target.value;
                        if (/^\d*\.?\d*$/.test(val)) setPreco(val);
                    }}
                />

                <Button type="submit" disabled={isLoading}>
                    {isLoading ? "Cadastrando..." : "Cadastrar"}
                </Button>
                
                {isLoading && (
                    <div style={{ textAlign: "center", marginTop: "1rem" }}>
                        <PuffLoader color="#BE6E46" />
                    </div>
                )}
            </Form>
        </div>
    );
};

export default CardCadastro;
