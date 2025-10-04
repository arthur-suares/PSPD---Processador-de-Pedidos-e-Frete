import { useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./Product.module.css";

interface ProductType {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
  stock: number;
}

interface ProductProps {
  products: ProductType[];
}

const Product = ({ products }: ProductProps) => {
  const { id } = useParams();
  const product = products.find((p) => p.id === Number(id));

  const [cep, setCep] = useState("");
  const [frete, setfrete] = useState<number | null>(null);

  const handleCalculatefrete = () => {
    if (cep.length === 8) {
      const valor = Math.floor(Math.random() * 50) + 10;
      setfrete(valor);
    } else {
      alert("Digite seu CEP");
    }
  };

  if (!product) return <p>Produto não encontrado</p>;

  return (
    <div className={styles.container}>
      <div className={styles.imageContainer}>
        <img src={product.image} alt={product.name} className={styles.productImage} />
      </div>
      <div className={styles.info}>
        <h1 className={styles.productName}>{product.name}</h1>
        <p className={styles.productDescription}>{product.description}</p>
        <p className={styles.productPrice}>R$ {product.price.toFixed(2)}</p>
        <p className={product.stock > 0 ? styles.emEstoque : styles.foraDeEstoque}>
          {product.stock > 0 ? "Em estoque" : "Produto indisponível"}
        </p>

        <div className={styles.frete}>
          <input
            type="text"
            placeholder="Digite seu CEP"
            value={cep}
            onChange={(e) => setCep(e.target.value.replace(/\D/, ""))}
            maxLength={8}
          />
          <button onClick={handleCalculatefrete}>Calcular frete</button>
        </div>

        {frete !== null && (
          <p className={styles.freteResultado}>Valor do frete: R$ {frete.toFixed(2)}</p>
        )}
      </div>
    </div>
  );
};

export default Product;
