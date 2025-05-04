import Navbar from "@/app/components/NavBar/NavBar";
import Sidebar from "@/app/components/Sidebar/Sidebar";
import styles from './layout.module.css';


const RootLayout = ({ children }: { children: React.ReactNode }) => {
    return (
        <html lang="en">
        <body>
        <div className={styles.layout}>
            <Sidebar/>
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
