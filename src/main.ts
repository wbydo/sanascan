import {app, BrowserWindow, Menu} from "electron";
import * as child_process from "child_process";

import * as util from "util";

import { menu } from "./menu";

const estimatorProcess = child_process.spawn(
  "pipenv",
  ["run", "gunicorn", "sanascan_backend.http:api"],
  {stdio: "inherit"},
);

app.on("ready", () => {
  const mainWindow: BrowserWindow = new BrowserWindow(
    {width: 600, height: 500}
  );
  Menu.setApplicationMenu(menu);
  mainWindow.loadURL(`file://${__dirname}/renderer/index.html`);
});

estimatorProcess.on("close", () => {
  app.exit();
});

app.once("will-quit", (event) => {
  event.preventDefault();
  estimatorProcess.kill();
});
