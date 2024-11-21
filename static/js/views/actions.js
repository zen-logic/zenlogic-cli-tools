import * as zen from '../lib/zen.js';

export class Actions {

	constructor (app, el) {
		this.app = app;
		this.el = el;
	}

	addAction (action) {
		let panel = zen.dom.createElement({
			parent: this.el,
			cls: 'action-item',
			content: action.content
		});

		if (action.cls) {
			panel.classList.add(action.cls);
		}

		let buttons = zen.dom.createElement({
			parent: panel,
			cls: 'buttons'
		});
		
		let btn = zen.dom.createElement({
			parent: buttons,
			cls: ['btn', 'error'],
			content: 'dismiss'
		});

		btn.addEventListener('click', ev => {
			panel.remove();
		});


		if (action.buttons) {
			action.buttons.forEach(o => {
				
				btn = zen.dom.createElement({
					parent: buttons,
					cls: ['btn', 'default'],
					content: o.label
				});

				btn.addEventListener('click', ev => {
					o.action(action.data);
				});

			});
		}

		
		panel.data = action.data;
		panel.scrollIntoView({ behavior: "smooth", block: "start" });
	}
}

