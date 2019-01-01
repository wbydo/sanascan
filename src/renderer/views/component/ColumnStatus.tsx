import * as React from "react";

import * as styles from "./ColumnStatus.css";

interface ColumnStatusProps {
  isActive: boolean;
}

export default class ColumnStatus extends React.Component<ColumnStatusProps, {}> {
  public render() {
    const className: string = this.props.isActive ? styles.active : styles.disactive;

    return(
      <colgroup span={1} className={className}/>
    );
  }
}
