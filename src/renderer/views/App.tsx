import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./component/CharacterBoard";
import Configure from "./Configure";
import * as styles from "./App.css";

import { RootState, operations } from "../state/";

// import { ipcRenderer } from "electron";

interface StateProps {
  configureWindowIsActive: boolean;
  activeColumn: number;
  timerScanSpeed: number;
  result: string;
}

interface DispatchProps {
  configureWindowOpen: (scanSpeed: number) => void;
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
        <button onClick={this.configureWindowOpen}>設定</button>
        <button onClick={this.props.resetEstimator}>はじめから</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startFetchEstimatorId();
  }

  private configureWindowOpen = () => {
    this.props.configureWindowOpen(this.props.timerScanSpeed);
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
  (dispatch: Dispatch): DispatchProps => operations(dispatch),
)(App);
