import { useNavigate } from "react-router-dom";
import styles from "./ProductBox.module.css";

interface ProductBoxProps {
  id: number;
  name: string;
  price: number;
  image: string;
  description?: string;
}

const ProductBox = ({ id, name, price, image, description }: ProductBoxProps) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/product/${id}`);
  };

  return (
    <div className={styles.productBox}>
      <img src={image} alt={name} className={styles.productImage} />
      <h3 className={styles.productName}>
        {name}
      </h3>
      {description && <p className={styles.productDescription}>{description}</p>}
      <p className={styles.productPrice}>
        R$ {price.toFixed(2)}
      </p>
      <button className={styles.button} onClick={handleClick}>
        Ver detalhes
      </button>
    </div>
  );
};

export default ProductBox;
