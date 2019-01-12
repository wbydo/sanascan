import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import * as styles from "./App.css";
import { Props as _Props } from "./util";

import Buttons from "./component/Buttons";
import CharacterBoard from "./component/CharacterBoard";
import Configure from "./component/Configure";

import { RootState, operations, selectors } from "../redux";

// import { ipcRenderer } from "electron";

export type StateProps = ReturnType<typeof selectors>;
export type DispatchProps = ReturnType<typeof operations>;

type Props = _Props<StateProps, DispatchProps>;

class App extends React.Component<Props> {
  public render() {
    return(
      <div
          id="App"
          className={styles.app}
      >
        <div>{this.props.result}</div>
        <div onClick={this.handleClick}>
          <CharacterBoard { ...this.props }/>
        </div>
        {this.props.configureWindowIsActive && <Configure { ...this.props }/>}
        <Buttons { ...this.props }/>
      </div>
    );
  }

  public componentDidMount = () => {
    if (!this.props.developerMode) {
      this.props.dispatch.startFetchEstimatorId();
    }
  }

  private handleClick = () => {
    this.props.dispatch.sendKey(this.props.activeColumn);
  }
}

export default connect(
  (state: RootState) => selectors(state),
  (dispatch: Dispatch) => ({ dispatch: operations(dispatch) }),
)(App);
