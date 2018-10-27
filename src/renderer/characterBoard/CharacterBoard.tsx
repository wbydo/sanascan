import * as React from "react";
import {connect} from "react-redux";

import ColumnStatus from "./ColumnStatus";
import {State} from "./reducers";

const chars: string[][] = [
  ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"],
  ["い", "き", "し", "ち", "に", "ひ", "み", "",   "り", ""],
  ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "を"],
  ["え", "け", "せ", "て", "ね", "へ", "め", "",   "れ", ""],
  ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "を", "ん"],
];

export const MAX_COLUMN_INDEX: number = chars[0].length - 1;

type Props = State;

class CharacterBoard extends React.Component<Props, {}> {
  public render() {
    return(
      <table>
        <caption></caption>
          {chars[0].map((row, idx) => {
            return <ColumnStatus isActive={idx === this.props.activeColumn}/>;
          })}
        <tbody>
          {chars.map((row) => {
            return <tr>{row.map((c) => <td>{c}</td>)}</tr>;
          })}
        </tbody>
      </table>
    );
  }
}

export default connect(
  (state: State) => state as Props,
  null,
)(CharacterBoard);
