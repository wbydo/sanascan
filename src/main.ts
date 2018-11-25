import {app, BrowserWindow} from "electron";
import * as child_process from "child_process";

class EstimatorProcess {
  private processObject: child_process.ChildProcess | null

  constructor(){
    this.processObject = null;
  }

  public start = () => {
    this.processObject = child_process.spawn(
      'pipenv',
      ['run', 'gunicorn', 'sanascan_backend.http:api'],
      {stdio: 'inherit'}
    );
  }

  public stop = () => {
    if(this.processObject == null){
      throw new Error();
    }
    this.processObject.kill();
  }
}

const ep = new EstimatorProcess();

app.on("ready", async () => {
  await ep.start()

  let mainWindow: BrowserWindow | null = new BrowserWindow({width: 360, height: 650});
  mainWindow.loadURL(`file://${__dirname}/renderer/index.html`);
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
});

app.on("window-all-closed", async () => {
  await ep.stop();
});
