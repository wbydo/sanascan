import React from "react";

interface Props<T extends string> {
  state: T;
  labels: T[];
  dispatch: (mode: T) => void;
}

export default class Selector<T extends string> extends React.Component<Props<T>> {
  public render() {
    return(
      <select value={this.props.state} onChange={this.change}>
        {this.props.labels.map((l) => <option value={l}>{l}</option> )}
      </select>
    );
  }

  private change = (event: React.FormEvent<HTMLSelectElement>) => {
    const target = event.target as HTMLSelectElement;
    this.props.dispatch(target.value as T);
  }
}
