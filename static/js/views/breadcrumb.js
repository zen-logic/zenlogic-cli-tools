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
	
}

