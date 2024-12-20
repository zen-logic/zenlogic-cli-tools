import * as zen from './lib/zen.js';
import {StorageRoots} from './views/storageroots.js';
import {Folders} from './views/folders.js';
import {Files} from './views/files.js';
import {Breadcrumb} from './views/breadcrumb.js';
import {Stats} from './views/stats.js';
import {Search} from './views/search.js';
import {Info} from './views/info.js';
import {Actions} from './views/actions.js';
import {Activity} from './views/activity.js';

(() => {
	
	function App (params) {
		if (arguments.length > 0) this.init(params);
		return this;
	}

	
	App.prototype = {
		
		init: function (params) {
			console.log('application loaded');
			this.cfg = params;
			this.setup();
			return this;
		},


		setup: function () {
			this.openWebSocket();
			this.launch();
		},

		
		openWebSocket: function () {
			this.ws = new WebSocket(`ws://${location.hostname}:${window.ws}`);
			
			this.ws.addEventListener("open", (ev) => {
				this.ws.send(JSON.stringify({action: 'subscribe'}));
			});

			this.ws.addEventListener("close", (ev) => {
				console.log('WebSocket closed');
			});
			
			this.ws.addEventListener("error", (ev) => {
				console.log('WebSocket error');
			});
			
			this.ws.addEventListener("message", (ev) => {
				let data = JSON.parse(ev.data);
				console.log(data);
				this.activity.update(data);
			});
		},
		
		
		launch: function () {
			this.storageRoots = new StorageRoots(this, zen.dom.getElement('#storage-root-list'));
			this.folders = new Folders(this, zen.dom.getElement('#main-panel'));
			this.files = new Files(this, zen.dom.getElement('#main-panel'));
			this.breadcrumb = new Breadcrumb(this, zen.dom.getElement('#breadcrumb'));
			this.stats = new Stats(this, zen.dom.getElement('.status-bar'));
			this.search = new Search(this, zen.dom.getElement('#search'));
			this.info = new Info(this, zen.dom.getElement('#item-info'));
			this.actions = new Actions(this, zen.dom.getElement('#action-list'));
			this.activity = new Activity(this, zen.dom.getElement('#activity-panel'));
		},


		deselectAll: function () {
			this.storageRoots.deselect();
			this.folders.deselect();
			this.breadcrumb.reset();
		},


		createProcess: async function (config) {
			const pid = zen.util.createUUID();
			config.params.pid = pid;
			this.activity.processes[pid] = config;
			
			try {
				const request = new Request(config.endpoint, {
					method: "POST",
					body: JSON.stringify(config.params)
				});
				const response = await fetch(request);
				if (!response.ok) {
					throw new Error(`Response status: ${response.status}`);
				}
				const data = await response.json();
				console.log(data);
			} catch (error) {
				console.error(error);
			}
			
		}

	};

	window.app = new App({});

})();
