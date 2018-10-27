import * as React from "react";

import CharacterBoard from "./characterBoard/CharacterBoard";

export default class App extends React.Component<{}, {}> {
  public render() {
    return(
      <CharacterBoard />
    );
  }
}
