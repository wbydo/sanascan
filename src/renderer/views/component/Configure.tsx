import React from "react";

import * as styles from "./Configure.css";

import { StateProps as AppStateProps } from "../App";
import { DispatchProps as AppDispatchProps } from "../App";
import { Props as _Props } from "../util";

type StateProps = Pick<AppStateProps, "configureWindowScanSpeed">;
type DispatchProps = Pick<
  AppDispatchProps,
  "configureWindowClose" | "changeDisplayValue"
>;

type Props = _Props<StateProps, DispatchProps>;

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
    this.props.dispatch.configureWindowClose(this.props.configureWindowScanSpeed);
  }

  private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const scanSpeed  = parseInt(target.value, 10); // 10進数の意
    this.props.dispatch.changeDisplayValue(scanSpeed);
  }
}
