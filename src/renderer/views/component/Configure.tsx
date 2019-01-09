import React from "react";

import * as styles from "./Configure.css";

interface StateProps {
  configureWindowScanSpeed: number;
}

interface DispatchProps {
  configureWindowClose: (lastValue: number) => void;
  changeDisplayValue: (scanSpeed: number) => void;
}

export type Props = StateProps & DispatchProps;

export default class Configure extends React.Component<Props> {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>環境設定</h1>
          <input type="number" value={this.props.configureWindowScanSpeed} onChange={this.handleChange}/>
          <button onClick={this.deactivateConfigure}>Off</button>
        </div>
      </div>
    );
  }

  private deactivateConfigure = () => {
    this.props.configureWindowClose(this.props.configureWindowScanSpeed);
  }

  private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const scanSpeed  = parseInt(target.value, 10); // 10進数の意
    this.props.changeDisplayValue(scanSpeed);
  }
}
