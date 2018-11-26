import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./CharacterBoard";
import {Action, increment} from "./actions";

interface Props {
  increment: () => void;
}

type MapDispatchToProps = (dispatch: Dispatch<Action>) => Props;

class App extends React.Component<Props, {}> {
  public render() {
    return(
      <div onClick={this.handleOnClick}>
        <CharacterBoard />
      </div>
    );
  }

  public handleOnClick = (event: React.MouseEvent): void => {
    return this.props.increment();
  }
}

const mdp: MapDispatchToProps = (dispatch) => {
  return {increment: () => dispatch(increment())};
};

export default connect(null, mdp)(App);
