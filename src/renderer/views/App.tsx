import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./component/CharacterBoard";
import Configure, { Props as ConfigureProps } from "./component/Configure";
import * as styles from "./App.css";

import { RootState, operations, selectors } from "../state/";

// import { ipcRenderer } from "electron";

export interface StateProps {
  configureWindowIsActive: boolean;
  activeColumn: number;
  timerScanSpeed: number;
  result: string;
}

export interface DispatchProps {
  configureWindowOpen: (scanSpeed: number) => void;
  startFetchEstimatorId: () => void;
  sendKey: (key: number) => void;
  resetEstimator: () => void;
}

type Props = DispatchProps & StateProps & ConfigureProps;

class App extends React.Component<Props> {
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
        {this.props.configureWindowIsActive && <Configure { ...this.props }/>}
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
  (state: RootState) => selectors(state),
  (dispatch: Dispatch) => operations(dispatch),
)(App);
