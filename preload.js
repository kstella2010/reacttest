// Preload script to expose Node.js modules to the renderer process
const { ipcRenderer } = require('electron');

window.ipcRenderer = ipcRenderer;
