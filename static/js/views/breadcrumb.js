import * as zen from '../lib/zen.js';

export class Breadcrumb {

	constructor (app, el) {
		this.app = app;
		this.el = el;
	}

	reset () {
		this.el.innerHTML = '';
	}
	
	setRoot (item) {
		this.el.innerHTML = '';
		this.app.info.reset();

		const button = zen.dom.createElement({
			parent: this.el,
			cls: 'item',
			content: item.dataset.name
		});

		button.addEventListener('click', ev => {
			this.app.storageRoots.selectRoot(item);
		});
	}

	addFolder (item) {
		this.app.info.reset();
		
		// delete items if this already exists in the breadcrumb
		let sel = `:scope *[data-id="${item.dataset.id}"][data-type="${item.dataset.type}"]`;
		let selected = zen.dom.getElement(sel, this.el);
		if (selected) {
			while (selected.nextElementSibling) {
				selected.nextElementSibling.remove();
			}
		} else {
			const button = zen.dom.createElement({
				parent: this.el,
				cls: 'item',
				content: item.dataset.name
			});

			button.dataset.id = item.dataset.id;
			button.dataset.type = item.dataset.type;
			button.dataset.path = item.dataset.path;
			button.dataset.name = item.dataset.name;
			
			button.addEventListener('click', ev => {
				this.app.folders.getFolder(button);
			});
		}
	}


	setPath (data) {
		let last;
		console.log(data);
		this.el.innerHTML = '';
		this.app.info.reset();
		for (let idx = 0; idx < data.length; idx++) {
			if (idx === 0) {
				const button = zen.dom.createElement({
					parent: this.el,
					cls: 'item',
					content: data[idx].name
				});

				button.addEventListener('click', ev => {
					this.app.storageRoots.selectRoot({
						dataset: data[idx].id
					});
				});
			} else {
				const button = zen.dom.createElement({
					parent: this.el,
					cls: 'item',
					content: data[idx].name
				});

				button.dataset.id = data[idx].id;
				button.dataset.type = 'folder';
				button.dataset.path = data[idx].path;
				button.dataset.name = data[idx].name;
				last = button;
				button.addEventListener('click', ev => {
					this.app.folders.getFolder(button);
				});
			}
		}
		this.app.folders.getFolder(last);
	}
	
	
	async setFolder (item) {
		let url;
		this.reset();
		switch (item.type) {
		case 'folder':
			url = `data/path/${item.id}`;
			break;
		case 'file':
			url = `data/path/${item.folder}`;
			break;
		}

		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.setPath(data);
		} catch (error) {
			console.error(error.message);
		}
		
	}

	
}

