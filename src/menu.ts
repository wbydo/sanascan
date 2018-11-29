import { app, Menu, MenuItem, BrowserWindow, Event } from "electron";

const SEPARATOR : "separator" = "separator";

const template = [
  {
    label: app.getName(), // Macの場合pListを弄らないと反映されない
    submenu: [
      {label: app.getName() + " について"},
      {type: SEPARATOR},
      {label: "環境設定..."},
      {type: SEPARATOR},
      {
        label: app.getName() + " を終了",
        accelerator: 'CommandOrControl+Q',
        click: () => {
          app.quit();
        }
      }
    ],
  }
];

export const menu = Menu.buildFromTemplate(template);
