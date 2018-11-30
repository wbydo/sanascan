import React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import {Action, deactivateConfigure, setScanSpeed} from "../state/actions";
import * as styles from "./Configure.css";

interface StateProps {
  scanSpeed: number;
}

interface DispatchProps {
  deactivateConfigure: () => void;
  setScanSpeed: (scanSpeed: number) => void;
}

type Props = StateProps & DispatchProps;

class Configure extends React.Component<Props> {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>環境設定</h1>
          <input type="number" value={this.props.scanSpeed} onChange={this.handleChange}/>
          <button onClick={(event) => this.props.deactivateConfigure()}>Off</button>
        </div>
      </div>
    );
  }

  private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const scanSpeed  = parseInt(target.value, 10); // 10進数の意
    if ( !isNaN(scanSpeed) ) {
      this.props.setScanSpeed(scanSpeed);
    }
  }
}

export default connect(
  (state: StateProps) => state,
  (dispatch: Dispatch<Action>): DispatchProps => {
    return {
      deactivateConfigure: () => dispatch(deactivateConfigure()),
      setScanSpeed: (scanSpeed: number) => dispatch(setScanSpeed(scanSpeed)),
    };
  },
)(Configure);
