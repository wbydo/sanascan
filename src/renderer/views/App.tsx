import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import * as styles from "./App.css";

import CharacterBoard from "./component/CharacterBoard";
import Configure, { Props as ConfigureProps } from "./component/Configure";
import Buttons, { Props as ButtonsProps} from "./component/Buttons";

import { RootState, operations, selectors } from "../redux";

// import { ipcRenderer } from "electron";

interface StateProps {
  configureWindowIsActive: boolean;
  activeColumn: number;
  result: string;
}

interface DispatchProps {
  startFetchEstimatorId: () => void;
  sendKey: (key: number) => void;
}

export type Props = DispatchProps & StateProps & ConfigureProps & ButtonsProps;

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
        <Buttons { ...this.props }/>
      </div>
    );
  }

  public componentDidMount = () => {
    if (!this.props.developerMode) {
      this.props.startFetchEstimatorId();
    }
  }

  private handleClick = () => {
    this.props.sendKey(this.props.activeColumn);
  }
}

export default connect(
  (state: RootState) => selectors(state),
  (dispatch: Dispatch) => operations(dispatch),
)(App);
