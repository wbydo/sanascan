import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./component/CharacterBoard";
import Configure from "./Configure";
import * as styles from "./App.css";

import { RootState } from "../state/";

import { actions as configWindowActions } from "../state/configWindow";
import { actions as timerActions } from "../state/timer";
import { actions as estimatorActions } from "../state/estimator";

// import { ipcRenderer } from "electron";

interface StateProps {
  configureWindowIsActive: boolean;
  activeColumn: number;
  timerScanSpeed: number;
  result: string;
}

interface DispatchProps {
  openConfigureWindow: (scanSpeed: number) => void;
  startFetchEstimatorId: () => void;
  sendKey: (key: number) => void;
  resetEstimator: () => void;
}

type Props = StateProps & DispatchProps;

class App extends React.Component<Props> {
  constructor(props: Props) {
    super(props);

    // ipcRenderer.on("openConfigureWindow", () => {
    //   this.openConfigureWindow();
    // });
  }

  public render() {
    return(
      <div
          id="App"
          className={styles.app}
      >
        <div>{this.props.result}</div>
        <div onClick={this.handleClick}>
          <CharacterBoard activeColumn={this.props.activeColumn}/>
        </div>
        {this.props.configureWindowIsActive && <Configure />}
        <button onClick={this.openConfigureWindow}>設定</button>
        <button onClick={this.props.resetEstimator}>はじめから</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startFetchEstimatorId();
  }

  private openConfigureWindow = () => {
    this.props.openConfigureWindow(this.props.timerScanSpeed);
  }

  private handleClick = () => {
    this.props.sendKey(this.props.activeColumn);
  }
}

export default connect(
  (state: RootState): StateProps => {
    return {
      activeColumn: state.cursol.activeColumn,
      configureWindowIsActive: state.configWindow.isActive,
      result: state.estimator.result,
      timerScanSpeed: state.timer.scanSpeed,
    };
  },
  (dispatch: Dispatch): DispatchProps => {
    return {
      openConfigureWindow: (scanSpeed: number) => {
        dispatch(timerActions.setActive(false));
        dispatch(configWindowActions.setScanSpeed(scanSpeed));
        dispatch(configWindowActions.setActive(true));
      },
      resetEstimator: () => dispatch(estimatorActions.reset()),
      sendKey: (key: number) => dispatch(estimatorActions.sendKey(key)),
      startFetchEstimatorId: () => dispatch(estimatorActions.fetchId("start")),
    };
  },
)(App);
