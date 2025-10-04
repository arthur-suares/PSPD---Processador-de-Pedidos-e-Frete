import ProductBox from "./ProductBox";
import styles from "./ProductGrid.module.css";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  description?: string;
}

interface ProductGridProps {
  products: Product[];
}

const ProductGrid = ({ products }: ProductGridProps) => {
  return (
    <div className={styles.grid}>
      {products.map((product) => (
        <ProductBox
          key={product.id}
          id={product.id}
          name={product.name}
          price={product.price}
          image={product.image}
          description={product.description}
        />
      ))}
    </div>
  );
};

export default ProductGrid;
