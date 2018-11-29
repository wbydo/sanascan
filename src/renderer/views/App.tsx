import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import {Action, startIncrement} from "../state/actions";
import { Modal } from "./Modal";

interface Props {
  startIncrement: () => void;
}

type MapDispatchToProps = (dispatch: Dispatch<Action>) => Props;

class App extends React.Component<Props> {
  public render() {
    return(
      <div>
        <CharacterBoard />
        <button>On</button>
      </div>
    );
  }

  public componentDidMount = () => {
    return this.props.startIncrement();
  }
}

const mdp: MapDispatchToProps = (dispatch) => {
  return {
    startIncrement: () => dispatch(startIncrement()),
  };
};

export default connect(null, mdp)(App);
