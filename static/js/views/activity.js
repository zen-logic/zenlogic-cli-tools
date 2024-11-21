import * as zen from '../lib/zen.js';

export class Activity {

	constructor (app, el) {
		this.app = app;
		this.el = el;
	}

	update (data) {
		console.log('here', data);
	}
	
}
