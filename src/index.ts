import {app, BrowserWindow, App} from 'electron'

console.log(`file://${__dirname}/index.html`);

app.on('ready', function() {
  let mainWindow: BrowserWindow | null = new BrowserWindow({width: 360, height: 650});
  mainWindow.loadURL(`file://${__dirname}/index.html`);
  mainWindow.on('closed', () => {
  mainWindow = null
  })
});
