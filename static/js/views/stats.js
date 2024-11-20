import * as zen from '../lib/zen.js';

export class Stats {

	constructor (app, el) {
		this.endpoint = 'data/stats';
		this.app = app;
		this.el = el;
		this.getStats();
		
	}


	populateStats (data) {
		this.el.innerHTML = '';
		console.log(data);

		let files = zen.util.readableNumber(data.files);
		let folders = zen.util.readableNumber(data.folders);
		
		let content = `Tracking: ${files} files and ${folders} folders`;
		const item = zen.dom.createElement({
			parent: this.el,
			content: content
		});
	}

	
	async getStats () {
		try {
			const response = await fetch(this.endpoint);
			if (!response.ok) {
				throw new Error(`Response status: ${response.status}`);
			}
			const data = await response.json();
			this.populateStats(data);
		} catch (error) {
			console.error(error.message);
		}
	}
	
	
}

