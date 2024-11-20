import * as zen from '../lib/zen.js';

export class StorageRoots {

	constructor (app, el) {
		this.endpoint = 'data/roots';
		this.app = app;
		this.el = el;
		this.getRoots();
	}


	deselect () {
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
				cls: o.status,
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
		if (selected) selected.classList.add('selected');
		this.app.breadcrumb.setRoot(item);
		const url = `${this.endpoint}/${item.dataset.id}`;
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.app.folders.populateItems(data);
		} catch (error) {
			console.error(error.message);
		}
	}
	
	
	async getRoots () {
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

