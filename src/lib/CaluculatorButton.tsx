import * as React from 'react';

interface KeyProps {
  label: string;
}

export default class CaluculatorButton extends React.Component<KeyProps, {}> {
  public render() {
    return(
      <div className="square_btn">
        <div className="num">{this.props.label}</div>
      </div>
    );
  }
}
