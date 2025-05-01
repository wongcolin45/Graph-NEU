import React from 'react';
import styles from './Loader.module.css';


const Loader = () => {
    return (
        <div className={styles.loaderWrapper}>
            <svg viewBox="25 25 50 50" className={styles.spinner}>
                <circle r="20" cy="50" cx="50" className={styles.circle} />
            </svg>
        </div>
    );
};

export default Loader;

