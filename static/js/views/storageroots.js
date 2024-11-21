import * as zen from '../lib/zen.js';

export class StorageRoots {

	constructor (app, el) {
		this.endpoint = 'data/roots';
		this.app = app;
		this.root = null;
		this.el = el;
		this.setup();
		this.getRoots();
	}


	setup () {
		this.rescan = zen.dom.getElement('*[data-action="rescan"]');
		this.addstorage = zen.dom.getElement('*[data-action="addstorage"]');
		this.addstorage.classList.add('enabled');

		if (this.rescan) {
			this.rescan.addEventListener('click', ev => {
				if (this.root && this.rescan.classList.contains('enabled')) {
					this.runScan(this.root.item);
				}
			});
		}
		
	}


	runScan (root) {
		let indicator = zen.dom.getElement(':scope .indicator', this.root);
		indicator.classList.remove('online', 'offline');
		indicator.classList.add('busy');
		indicator.innerHTML = 'scanning';
		this.rescan.classList.remove('enabled');
		this.app.createProcess('actions/scan', {root: root.id});
	}
	

	deselect () {
		this.rescan.classList.remove('enabled');
		this.root = null;
		zen.dom.getElements(':scope>div', this.el).forEach(el => {
			el.classList.remove('selected');
		});
	}
	

	populateRoots (data) {
		this.el.innerHTML = '';
		console.log(data);
		data.forEach(o => {
			const item = zen.dom.createElement({
				parent: this.el,
				cls: 'list-item'
			});

			item.dataset.id = o.id;
			item.dataset.path = o.path;
			item.dataset.name = o.name;
			item.item = o;
			
			const icon = zen.dom.createElement({
				parent: item,
				tag: 'img',
				cls: 'icon'
			});

			icon.src = `img/feather/hard-drive.svg`;
			const label = zen.dom.createElement({
				parent: item,
				tag: 'span',
				content: o.name
			});

			zen.dom.createElement({parent: item, cls: 'spacer'});
			
			zen.dom.createElement({
				parent: item,
				tag: 'span',
				cls: ['indicator', o.status],
				content: o.status
			});
			
			item.addEventListener('click', ev => {
				this.selectRoot(item);
			});
		});
	}

	
	async selectRoot (item) {
		this.app.search.search.value = '';
		const selected = zen.dom.getElement(`:scope>div[data-id="${item.dataset.id}"]`, this.el);
		this.deselect();
		if (selected) {
			selected.classList.add('selected');
		}
		this.app.breadcrumb.setRoot(item);
		const url = `${this.endpoint}/${item.dataset.id}`;
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.app.folders.populateItems(data);
			this.root = item;

			let indicator = zen.dom.getElement(':scope .indicator', this.root);
			if (indicator.classList.contains('online')) {
				this.rescan.classList.add('enabled');
			}
		} catch (error) {
			console.error(error.message);
		}
	}
	
	
	async getRoots () {
		this.rescan.classList.remove('enabled');
		try {
			const response = await fetch(this.endpoint);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.populateRoots(data);
		} catch (error) {
			console.error(error.message);
		}
	}
	
}

