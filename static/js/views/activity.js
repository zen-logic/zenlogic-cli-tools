import * as zen from '../lib/zen.js';

export class Activity {

	constructor (app, el) {
		this.app = app;
		this.el = el;
		this.processes = {};
	}


	createItem () {
		let template = `
			<div class="header">
				<div class="description"></div>
				<div class="status"></div>
			</div>
			<div class="info">
				<div class="detail"></div>
				<div class="stats">
					<div><b>Files:</b> 32312</div>
					<div><b>Folders:</b> 185</div>
				</div>
			</div>`;
		
		let panel = zen.dom.createElement({
			parent: this.el,
			cls: 'item',
			content: template
		});

		panel.description = zen.dom.getElement('.header .description', panel);
		panel.status = zen.dom.getElement('.header .status', panel);
		panel.detail = zen.dom.getElement('.info .detail', panel);
		panel.stats = zen.dom.getElement('.info .stats', panel);
		
		return panel;
	}


	updateProcess (process, data) {
		if (!process.panel) process.panel = this.createItem(data);
		process.panel.description.innerHTML = data.description;
		process.panel.status.innerHTML = data.status;
		process.panel.detail.innerHTML = data.info.detail;
		process.panel.stats.innerHTML = '';
		if (data.info.stats !== undefined) {
			data.info.stats.forEach(o => {
				process.panel.stats.innerHTML += `<div><b>${o.label}:</b> ${o.value}</div>`;
			});
		}
	}
	
	
	update (data) {
		if (data.pid) {
			if (!this.processes[data.pid]) {
				this.processes[data.pid] = {
					pid: data.pid,
					description: data.description,
				};
			}
			let process = this.processes[data.pid];
			this.updateProcess(process, data);
		}
	}
	
}
