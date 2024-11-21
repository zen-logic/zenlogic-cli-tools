import * as zen from '../lib/zen.js';

export class Search {

	constructor (app, el) {
		this.endpoint = 'data/search';
		this.app = app;
		this.el = el;
		this.search = zen.dom.getElement('input[name="search"]', this.el);
		this.searchType = zen.dom.getElement('select[name="search-type"]', this.el);
		this.matchType = zen.dom.getElement('select[name="match-type"]', this.el);
		this.setup();
	}

	setup () {

		this.el.addEventListener('submit', ev => {
			ev.preventDefault();
			this.runSearch();
		});

	}

	deselect () {
		const panel = zen.dom.getElement('#main-panel');
		zen.dom.getElements(':scope tr', panel).forEach(el => {
			el.classList.remove('selected');
		});
	}
	
	selectItem (row) {
		if (row.classList.contains('selected')) {
			this.app.breadcrumb.setFolder(row.item);
		} else {
			this.deselect();
			row.classList.add('selected');
			console.log(row.item);
			row.dataset.id = row.item.id;
			switch(row.item.type) {
			case 'folder':
				this.app.info.showFolder(row);
				break;
			case 'file':
				this.app.info.showFile(row);
				break;
			}
		}
		
	}
	
	
	populateItems (data) {
		const panel = zen.dom.getElement('#main-panel');
		
		const table = zen.dom.createElement({
			parent: panel,
			tag: 'table',
			cls: 'search-results'
		});

		zen.dom.createElement({
			parent: table,
			tag: 'tr',
			cls: 'header',
			content: '<th>Storage</th><th>Path</th>'
		});
		
		data.forEach(o => {
			let row = zen.dom.createElement({parent: table, tag: 'tr'});
			zen.dom.createElement({
				parent: row,
				tag: 'td',
				content: `<nobr>${o.rootname}</nobr>`
			});
			row.item = o;
			let filepath = `<nobr>${o.fullpath}`;
			if (o.type === 'file') {
				filepath += `/${o.name}`;
			}
			filepath += '</nobr>';
			
			zen.dom.createElement({
				parent: row,
				tag: 'td',
				content: filepath
			});

			row.addEventListener('click', ev => {
				this.selectItem(row);
			});
		});

		const status = zen.dom.getElement('#breadcrumb');
		status.innerHTML = `<div class="results">${data.length} matching items found.</div>`;
	}

	
	async runSearch (hash, callback) {
		if (this.search.value.length > 1 || hash) {
			let searchData;
			const panel = zen.dom.getElement('#main-panel');
			panel.innerHTML = '';
			this.app.deselectAll();
			this.app.info.reset();

			if (hash) {
				searchData = {
					search: hash,
					type: 'hash',
					match: null
				};
			} else {
				searchData = {
					search: this.search.value,
					type: this.searchType.value,
					match: this.matchType.value
				};
			}
			
			try {
				const request = new Request(this.endpoint, {
					method: "POST",
					body: JSON.stringify(searchData),
				});
				const response = await fetch(request);
				if (!response.ok) {
					throw new Error(`Response status: ${response.status}`);
				}
				const data = await response.json();
				this.populateItems(data);
				if (callback) {
					callback(data);
				}
			} catch (error) {
				console.error(error.message);
			}
		}
	}

}

