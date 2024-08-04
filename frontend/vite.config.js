import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import react from '@vitejs/plugin-react'

import proxyOptions from './proxyOptions';

import Components from 'unplugin-vue-components/vite';
import {PrimeVueResolver} from '@primevue/auto-import-resolver';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(), 
		react(),
		Components({
			resolvers: [
				PrimeVueResolver()
			]
		}),
	],
	server: {
		port: 8080,
		proxy: proxyOptions
	},
	define: {
		"process.env.IS_PREACT": JSON.stringify("true"),
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
			'vue': 'vue/dist/vue.esm-bundler.js',
			'react': 'react',
      		'react-dom': 'react-dom',
		}
	},
	build: {
		outDir: '../healthcare_doworks/public/frontend',
		emptyOutDir: true,
		target: 'es2015',
	}
});
