import * as React from "react";

import CharacterBoard from "./character_board/CharacterBoard";

export default class App extends React.Component<{}, {}> {
  public render() {
    return(
      <CharacterBoard />
    );
  }
}
