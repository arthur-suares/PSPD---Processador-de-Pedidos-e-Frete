import styles from "./Home.module.css";
import ProductGrid from "../../components/ProductGrid";
import logo from "../../assets/images/online-shopping.png";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  description?: string;
  stock: number;
}

interface HomeProps {
  products: Product[];
}

const Home = ({ products }: HomeProps) => {
  return (
    <>
      <header className={styles.header}>
        <div className={styles.logo}>
          <img src={logo} alt="Logo" width={40} />
          comprAqui
        </div>
      </header>

      <div className={styles.container}>
        <div className={styles.wrapper}>
          <ProductGrid products={products} />
        </div>
      </div>
    </>
  );
};

export default Home;
