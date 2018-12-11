import {app, BrowserWindow, Menu} from "electron";
import * as child_process from "child_process";

import { menu } from "./menu";

import installExtension, { REDUX_DEVTOOLS } from "electron-devtools-installer";

const estimatorProcess = child_process.spawn(
  "pipenv",
  ["run", "gunicorn", "sanascan_backend.http:api"],
  {stdio: "inherit"},
);

app.on("ready", () => {
  installExtension(REDUX_DEVTOOLS)
  .then((name) => console.log(`Added Extension:  ${name}`))
  .catch((err) => console.log("An error occurred: ", err));

  const mainWindow: BrowserWindow = new BrowserWindow(
    {width: 600, height: 500},
  );

  // Menu.setApplicationMenu(menu);
  mainWindow.loadURL(`file://${__dirname}/renderer/index.html`);
});

estimatorProcess.on("close", () => {
  app.exit();
});

app.once("will-quit", (event) => {
  event.preventDefault();
  estimatorProcess.kill();
});
