import React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import {Action, deactivateConfigure} from "../state/actions";
import * as styles from "./Configure.css";

interface DispatchProps {
  deactivateConfigure: () => void;
}

type Props = DispatchProps;

class Configure extends React.Component<Props> {
  public render() {
    return(
      <div id="Configure" className={styles.frame}>
        <div className={styles.content}>
          <h1>環境設定</h1>
          <button onClick={(event) => this.props.deactivateConfigure()}>Off</button>
        </div>
      </div>
    );
  }
}

export default connect(
  null,
  (dispatch: Dispatch<Action>): DispatchProps => {
    return {
      deactivateConfigure: () => dispatch(deactivateConfigure()),
    };
  },
)(Configure);
