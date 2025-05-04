// components/ClientSelect.tsx
'use client';

import dynamic from 'next/dynamic';
export default dynamic(() => import('react-select'), { ssr: false });
