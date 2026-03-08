
import Link from 'next/link';
import styles from './NavBar.module.css';

import Image from 'next/image';

const Navbar = () => {
    return (
        <nav className={styles.navbar}>
            <div className={styles.left}>
                <Image src={'/logo.png'} alt={'logo'} height={44} width={44} priority/>
                <h1>Graph NEU</h1>
            </div>

            <ul>
                <li><Link href="/">About</Link></li>
                <li><Link href="/explore">Explore</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
