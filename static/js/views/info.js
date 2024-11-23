import * as zen from '../lib/zen.js';

export class Info {

	constructor (app, el) {
		this.endpoint = 'data/info';
		this.app = app;
		this.el = el;
		this.file = null;
		this.folder = null;
		this.setup();
		
	}


	setup () {
		this.openFolder = zen.dom.getElement('*[data-action="openfolder"]');
		this.hashSearch = zen.dom.getElement('*[data-action="findhash"]');
		this.flag = zen.dom.getElement('*[data-action="flag"]');

		if (this.hashSearch) {
			this.hashSearch.addEventListener('click', ev => {
				if (this.file && this.hashSearch.classList.contains('enabled')) {
					this.app.search.runSearch(this.file.hash, data => {
						this.checkHashResults(data);
					});
				}
			});
		}

		if (this.flag) {
			this.flag.addEventListener('click', ev => {
				if (this.folder && this.flag.classList.contains('enabled')) {
					console.log('Flag folder');
				} 
			});
		}

		if (this.openFolder) {
			this.openFolder.addEventListener('click', ev => {
				if ((this.folder || this.file) && this.openFolder.classList.contains('enabled')) {
					if (this.folder) {
						this.openFileBrowser(this.folder.id);
					} else {
						this.openFileBrowser(this.file.id);
					}
				} 
			});
		}
		
	}


	async openFileBrowser (itemID) {
		let params = {};
		if (this.folder) {
			params['folder'] = itemID;
		} else if (this.file) {
			params['file'] = itemID;
		} else {
			// nothing actually selected
			return;
		}
		
		params = JSON.stringify(params);
		
		try {
			const request = new Request('actions/folder', {
				method: "POST",
				body: params,
			});
			const response = await fetch(request);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			console.log(data);
		} catch (error) {
			console.error(error);
		}
	}
	
	
	checkHashResults (data) {
		// reselect the original file in the search results list
		const results = zen.dom.getElements('#main-panel .search-results tr');
		for (let idx = 0; idx < results.length; idx++) {
			let row = results[idx];
			if (row.item && row.item.id === this.file.id) {
				row.click();
				break;
			}
		}
		
		// check if we've got duplicates then see if the user wants to do
		// something about it...
		if (data.length > 1) {
			let content = `
<h4>Identical files matching '${this.file.name}' found in ${data.length} locations</h4>
<p>Would you like to take action?</p>`;
			let action = {
				content: content,
				data: data,
				buttons: [
					{
						label: 'review folders',
						action: (data) => {
							alert('compare folders');
						}
					},
					{
						label: 'consolidate files',
						action: (data) => {
							alert('consolidate files');
						}
					}
				]
			};
			this.app.actions.addAction(action);
		} else {
			let content = `<h4>No other files matching '${this.file.name}'</h4>`;
			let action = {
				content: content,
				data: data,
				cls: 'ok'
			};
			this.app.actions.addAction(action);
		}
		
	}
	
	
	reset () {
		this.el.innerHTML = '';
		this.hashSearch.classList.remove('enabled');
		this.flag.classList.remove('enabled');
		this.openFolder.classList.remove('enabled');
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
		
		this.file = data;
		this.folder = null;
		this.hashSearch.classList.add('enabled');
		this.flag.classList.remove('enabled');
		this.openFolder.classList.add('enabled');
	}


	populateFolder (data) {
		this.el.innerHTML = '';

		let item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Name'});
		zen.dom.createElement({parent: item, content: data.name});
		
		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Storage'});
		zen.dom.createElement({parent: item, content: data.rootname});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Path'});
		zen.dom.createElement({parent: item, content: data.fullpath.replace(data.name, '')});
		
		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Files'});
		zen.dom.createElement({parent: item, content: data.filecount});

		item = zen.dom.createElement({parent: this.el, cls: 'info-item'});
		zen.dom.createElement({parent: item, cls: 'label', content: 'Folders'});
		zen.dom.createElement({parent: item, content: data.foldercount});

		this.file = null;
		this.folder = data;
		this.hashSearch.classList.remove('enabled');
		this.flag.classList.add('enabled');
		this.openFolder.classList.add('enabled');
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

