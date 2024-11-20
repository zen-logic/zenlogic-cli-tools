import * as zen from './lib/zen.js';
import {StorageRoots} from './views/storageroots.js';
import {Folders} from './views/folders.js';
import {Files} from './views/files.js';
import {Breadcrumb} from './views/breadcrumb.js';
import {Stats} from './views/stats.js';
import {Search} from './views/search.js';

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


		openWebSocket: function () {
			const socketURL = `ws://${location.hostname}:${window.ws}`;
			self.ws = new WebSocket(socketURL);
			
			self.ws.addEventListener("open", (ev) => {
				self.ws.send(JSON.stringify({action: 'subscribe'}));
			});

			self.ws.addEventListener("close", (ev) => {
				console.log('WebSocket closed');
			});
			
			self.ws.addEventListener("error", (ev) => {
				console.log('WebSocket error');
			});
			
			self.ws.addEventListener("message", (ev) => {
				let data = JSON.parse(ev.data);
				console.log("Message from server ", data);
			});
		},
		
		
		setup: function () {
			this.openWebSocket();
			this.launch();
		},

		
		launch: function () {
			
			this.storageRoots = new StorageRoots(
				this, zen.dom.getElement('#storage-root-list')
			);

			this.folders = new Folders(
				this, zen.dom.getElement('#main-panel')
			);

			this.files = new Files(
				this, zen.dom.getElement('#main-panel')
			);

			this.breadcrumb = new Breadcrumb(
				this, zen.dom.getElement('#breadcrumb')
			);

			this.stats = new Stats(
				this, zen.dom.getElement('.status-bar')
			);
			
			this.search = new Search(
				this, zen.dom.getElement('#search')
			);
			
		},


		deselectAll: function () {
			this.storageRoots.deselect();
			this.folders.deselect();
			this.breadcrumb.reset();
		}
		
	};

	window.app = new App({});

})();
