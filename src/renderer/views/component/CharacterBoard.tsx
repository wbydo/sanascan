import * as React from "react";

import ColumnStatus from "./ColumnStatus";
import * as styles from "./CharacterBoard.css";

import { Props } from "../App";

import { chars } from "../../constant";

export default class CharacterBoard extends React.Component<Props> {
  public render() {
    return(
      <table id="CharacterBoard" className={styles.characterBoard}>
        <caption></caption>
          {chars[0].map((_, idx) => {
            const isActiveColumn =  idx === this.props.cursol.activeColumn;
            const isColumnMode = "column" === this.props.cursol.direction;
            return <ColumnStatus isActive={isActiveColumn && isColumnMode}/>;
          })}
        <tbody>
          {chars.map((row, rowIdx) => {
            return(<tr>
              {row.map((c, colIdx) => {
                const isRowMode = "row" === this.props.cursol.direction;
                const isActiveColumn =  colIdx === this.props.cursol.activeColumn;
                const isActiveRow = rowIdx === this.props.cursol.activeRow;

                const className = isRowMode && isActiveColumn && isActiveRow ?
                    styles.activeData : styles.deactiveData;
                return <td className={className}>{c}</td>;
              })}
            </tr>
            );
          })}
        </tbody>
      </table>
    );
  }
}
