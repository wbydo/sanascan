import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import * as styles from "./App.css";
import { Props as _Props } from "./util";

import Buttons from "./component/Buttons";
import CharacterBoard from "./component/CharacterBoard";
import Configure from "./component/Configure";

import { RootState, operations } from "../redux";

// import { ipcRenderer } from "electron";

type StateProps = RootState;
type DispatchProps = ReturnType<typeof operations>;

export type Props = _Props<StateProps, DispatchProps>;

class App extends React.Component<Props> {
  public render() {
    return(
      <div
          id="App"
          className={styles.app}
      >
        <div>{this.props.estimator.result}</div>
        <div onMouseDown={() => this.props.dispatch.click(this.props)}>
          <CharacterBoard { ...this.props }/>
        </div>
        {this.props.configWindow.isActive && <Configure { ...this.props }/>}
        <Buttons { ...this.props }/>
      </div>
    );
  }

  public componentDidMount = () => {
    const { developerMode } = this.props;
    if (developerMode.isActive && developerMode.timer) {
      this.props.dispatch.developerMode.startTimer();
    }

    if (!developerMode.isActive) {
      this.props.dispatch.startFetchEstimatorId();
    }
  }
}

export default connect(
  (state: RootState) => state,
  (dispatch: Dispatch) => ({ dispatch: operations(dispatch) }),
)(App);
