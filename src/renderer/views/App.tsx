import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import { start as startTimer } from "../state/timer/actions";
import Configure from "./Configure";
import * as styles from "./App.css";

interface StateProps {
  modalIsActive: boolean;
}

interface DispatchProps {
  // activateConfigure: () => void;
  startTimer: () => void;
}

type Props = StateProps & DispatchProps;

class App extends React.Component<Props> {
  public render() {
    return(
      <div id="App" className={styles.app}>
        <CharacterBoard />
        {this.props.modalIsActive && <Configure />}
        <button onClick={(event) => {undefined;}}>設定</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startTimer();
  }
}

export default connect(
  (state: StateProps): StateProps => state,
  (dispatch: Dispatch): DispatchProps => {
    return {
      // activateConfigure: () => dispatch(activateConfigure()),
      startTimer: () => dispatch(startTimer()),
    };
  },
)(App);
