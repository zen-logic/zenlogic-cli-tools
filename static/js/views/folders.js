import * as zen from '../lib/zen.js';

export class Folders {

	constructor (app, el) {
		this.endpoint = 'data/folders';
		this.app = app;
		this.el = el;
	}


	deselect () {
		const panel = zen.dom.getElement('#main-panel');
		zen.dom.getElements(':scope>div', panel).forEach(el => {
			el.classList.remove('selected');
		});
	}
	
	populateItems (data) {
		const panel = zen.dom.getElement('#main-panel');
		panel.innerHTML = '';

		data.forEach(o => {
			const item = zen.dom.createElement({
				parent: panel,
				cls: 'list-item'
			});

			const icon = zen.dom.createElement({
				parent: item,
				tag: 'img',
				cls: 'icon'
			});

			icon.src = `img/feather/${o.type}.svg`;
			const label = zen.dom.createElement({
				parent: item,
				tag: 'span',
				content: o.name
			});

			item.dataset.id = o.id;
			item.dataset.type = o.type;
			item.dataset.path = o.path;
			item.dataset.name = o.name;
			
			item.addEventListener('click', ev => {
				this.selectItem(item);
			});
		});
		
	}


	selectFile (item) {
		
	}

	selectFolder (item) {
		
	}

	
	selectItem (item) {
		this.app.search.search.value = '';
		
		if (item.classList.contains('selected') && item.dataset.type === 'folder') {
			this.getFolder(item);
		} else {
			let sel = `:scope *[data-id="${item.dataset.id}"][data-type="${item.dataset.type}"]`;
			const panel = zen.dom.getElement('#main-panel'),
				  selected = zen.dom.getElement(sel, panel);
			this.deselect();
			if (selected) selected.classList.add('selected');
			switch (item.dataset.type) {
			case 'file':
				this.selectFile(item);
				break;
			case 'folder':
				this.selectFolder(item);
				break;
			}
		}
	}

	
	async getFolder (item) {
		this.app.breadcrumb.addFolder(item);
		const url = `${this.endpoint}/${item.dataset.id}`;
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.populateItems(data);
		} catch (error) {
			console.error(error.message);
		}
	}
	
}

