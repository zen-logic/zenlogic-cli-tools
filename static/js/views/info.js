import * as zen from '../lib/zen.js';

export class Info {

	constructor (app, el) {
		this.endpoint = 'data/info';
		this.app = app;
		this.el = el;
	}

	
	populateFile (data) {
		console.log(data);
		console.log(data.name);
		console.log(data.rootname);
		console.log(data.fullpath);
		console.log(data.hash);
		console.log(new Date(data.created * 1000).toLocaleString());
		console.log(new Date(data.modified * 1000).toLocaleString());
		console.log(zen.util.formatBytes(data.size));
	}


	populateFolder (data) {
		console.log(data);
		console.log(data.name);
		console.log(data.fullpath);
		console.log(data.rootname);
		console.log(data.filecount);
		console.log(data.foldercount);
	}

	
	async showFile (item) {
		try {
			const response = await fetch(`${this.endpoint}/file/${item.dataset.id}`);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.populateFile(data);
		} catch (error) {
			console.error(error.message);
		}
	}


	async showFolder (item) {
		try {
			const response = await fetch(`${this.endpoint}/folder/${item.dataset.id}`);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.populateFolder(data);
		} catch (error) {
			console.error(error.message);
		}
	}
	
	
}

