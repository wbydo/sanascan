import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import CharacterBoard from "./characterBoard/CharacterBoard";
import {Action as CharacterBoardAction} from "./characterBoard/actions";
import {increment} from "./characterBoard/actions";

interface Props {
  increment: () => void;
}

type MapDispatchToProps = (dispatch: Dispatch<CharacterBoardAction>) => Props;

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
