import React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import * as styles from "./Configure.css";

import { RootState, operations } from "../state";

interface StateProps {
  scanSpeed: {
    configWindow: number,
    timer: number,
  };
}

interface DispatchProps {
  configureWindowClose: (lastValue: number) => void;
  changeDisplayValue: (scanSpeed: number) => void;
}

type Props = StateProps & DispatchProps;

class Configure extends React.Component<Props> {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>環境設定</h1>
          <input type="number" value={this.props.scanSpeed.configWindow} onChange={this.handleChange}/>
          <button onClick={this.deactivateConfigure}>Off</button>
        </div>
      </div>
    );
  }

  private deactivateConfigure = () => {
    this.props.configureWindowClose(this.props.scanSpeed.configWindow);
  }

  private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const scanSpeed  = parseInt(target.value, 10); // 10進数の意
    this.props.changeDisplayValue(scanSpeed);
  }
}

export default connect(
  (state: RootState): StateProps => {
    return {
      scanSpeed: {
        configWindow: state.configWindow.scanSpeed,
        timer: state.timer.scanSpeed,
      },
    };
  },
  (dispatch: Dispatch): DispatchProps => operations(dispatch),
)(Configure);
