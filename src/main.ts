import {app, BrowserWindow, App} from "electron";

app.on("ready", () => {
  let mainWindow: BrowserWindow | null = new BrowserWindow({width: 360, height: 650});
  mainWindow.loadURL(`file://${__dirname}/renderer/index.html`);
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
});
