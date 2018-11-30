import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import {Action, startTimer, activateConfigure} from "../state/actions";
import Configure from "./Configure";
import * as styles from "./App.css";

interface StateProps {
  modalIsActive: boolean;
}

interface DispatchProps {
  activateConfigure: () => void;
  startTimer: () => void;
}

type Props = StateProps & DispatchProps;

class App extends React.Component<Props> {
  public render() {
    return(
      <div id="App" className={styles.app}>
        <CharacterBoard />
        {this.props.modalIsActive && <Configure />}
        <button onClick={(event) => this.props.startTimer()}>設定</button>
      </div>
    );
  }

  public componentDidMount = () => {
    // return this.props.startIncrement();
  }
}

export default connect(
  (state: StateProps): StateProps => state,
  (dispatch: Dispatch<Action>): DispatchProps => {
    return {
      activateConfigure: () => dispatch(activateConfigure()),
      startTimer: () => dispatch(startTimer()),
    };
  },
)(App);
