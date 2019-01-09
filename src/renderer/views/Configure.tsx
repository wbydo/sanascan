import React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import * as styles from "./Configure.css";

import { RootState } from "../state";
import { actions as configWindowActions } from "../state/configWindow";
import { actions as timerActions } from "../state/timer";

interface StateProps {
  scanSpeed: {
    configWindow: number,
    timer: number,
  };
}

interface DispatchProps {
  deactivateConfigure: (lastValue: number) => void;
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
    this.props.deactivateConfigure(this.props.scanSpeed.configWindow);
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
  (dispatch: Dispatch): DispatchProps => {
    return {
      changeDisplayValue: (scanSpeed: number) => {
        dispatch(configWindowActions.setScanSpeed(scanSpeed));
      },
      deactivateConfigure: (lastValue: number) => {
        if (lastValue > 0) {
          dispatch(timerActions.setScanSpeed(lastValue));
        }
        dispatch(configWindowActions.setActive(false));
        dispatch(timerActions.start());
      },
    };
  },
)(Configure);
