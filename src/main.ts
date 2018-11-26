import {app, BrowserWindow} from "electron";
import * as child_process from "child_process";

import * as util from "util";

const estimatorProcess = child_process.spawn(
  "pipenv",
  ["run", "gunicorn", "sanascan_backend.http:api"],
  {stdio: "inherit"},
);

app.on("ready", () => {
  let mainWindow: BrowserWindow | null = new BrowserWindow({width: 360, height: 650});
  mainWindow.loadURL(`file://${__dirname}/renderer/index.html`);
});

estimatorProcess.on("close", () => {
  app.exit()
});

app.once("will-quit", (event) => {
  event.preventDefault();
  estimatorProcess.kill();
});
