import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';
import copy from 'rollup-plugin-copy';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		copy({
			targets: [
				{ src: 'src/assets/css', dest: 'dist/css' },
				{ src: 'src/assets/admin/css', dest: 'dist/admin/css' },
				{ src: 'src/assets/pharmacy/css', dest: 'dist/pharmacy/css' },
			],
		}),
	],
	server: {
		port: 8080,
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../healthcare_doworks/public/frontend',
		emptyOutDir: true,
		target: 'es2015',
	}
});
