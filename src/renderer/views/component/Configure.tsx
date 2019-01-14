import React from "react";

import * as styles from "./Configure.css";

import { Props } from "../App";

export default class Configure extends React.Component<Props> {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>環境設定</h1>
          <input type="number" value={this.props.configWindow.scanSpeed} onChange={this.handleChange}/>
          <button onClick={this.deactivateConfigure}>Off</button>
        </div>
      </div>
    );
  }

  private deactivateConfigure = () => {
    this.props.dispatch.configureWindowClose(this.props.configWindow.scanSpeed);
  }

  private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const scanSpeed  = parseInt(target.value, 10); // 10進数の意
    this.props.dispatch.changeDisplayValue(scanSpeed);
  }
}
