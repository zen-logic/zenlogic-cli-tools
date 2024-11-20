import * as zen from '../lib/zen.js';

export class Info {

	constructor (app, el) {
		this.endpoint = 'data/info';
		this.app = app;
		this.el = el;
	}

	
	populateFile (data) {
		this.el.innerHTML = '';

		let item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Name'});
		zen.dom.createElement({parent: item, content: data.name});
		
		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Size'});
		zen.dom.createElement({parent: item, content: zen.util.formatBytes(data.size)});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Storage'});
		zen.dom.createElement({parent: item, content: data.rootname});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Path'});
		zen.dom.createElement({parent: item, content: data.fullpath});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Hash'});
		zen.dom.createElement({parent: item, content: data.hash});
		
		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Created'});
		zen.dom.createElement({parent: item, content: new Date(data.created * 1000).toLocaleString()});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Modified'});
		zen.dom.createElement({parent: item, content: new Date(data.modified * 1000).toLocaleString()});
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

