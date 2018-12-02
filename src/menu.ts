import { app, Menu, MenuItem, BrowserWindow } from "electron";

const SEPARATOR: "separator" = "separator";

const template = [
  {
    label: app.getName(), // Macの場合pListを弄らないと反映されない
    submenu: [
      {label: app.getName() + " について"},
      {type: SEPARATOR},
      {
        click: (_: MenuItem, browserWindow: BrowserWindow) => {
          browserWindow.webContents.send("openConfigureWindow");
        },
        label: "環境設定...",
      },
      {type: SEPARATOR},
      {
        accelerator: "CommandOrControl+Q",
        click: () => app.quit(),
        label: app.getName() + " を終了",
      },
    ],
  },
];

export const menu = Menu.buildFromTemplate(template);
