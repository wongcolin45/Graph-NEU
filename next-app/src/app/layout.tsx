import Navbar from "@/app/components/NavBar/NavBar";
import styles from './layout.module.css';


const RootLayout = ({ children }: { children: React.ReactNode }) => {
    return (
        <html lang="en">
        <body>
        <div className={styles.layout}>
            <div className={styles.mainContent}>
                <Navbar/>
                <main>{children}</main>
            </div>
        </div>

        </body>

        </html>
    );
};

export default RootLayout;
