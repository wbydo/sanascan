import * as React from "react";

import ColumnStatus from "./ColumnStatus";

const chars: string[][] = [
  ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"],
  ["い", "き", "し", "ち", "に", "ひ", "み", "",   "り", ""],
  ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "を"],
  ["え", "け", "せ", "て", "ね", "へ", "め", "",   "れ", ""],
  ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "を", "ん"],
];

export default class CharacterBoard extends React.Component<{}, {}> {
  public static readonly MAX_COLUMN_INDEX: number = chars[0].length - 1;

  public render() {
    return(
      <table>
        <caption></caption>
          {chars[0].map((row, idx) => {
            return <ColumnStatus isActive={idx === 1}/>;
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
