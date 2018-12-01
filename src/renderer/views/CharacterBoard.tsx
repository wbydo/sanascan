import * as React from "react";
import {connect} from "react-redux";

import ColumnStatus from "./ColumnStatus";
import * as styles from "./CharacterBoard.css";

import { chars } from "../constant";

interface Props {
  activeColumn: number;
}

interface State {
  cursol: Props;
}

class CharacterBoard extends React.Component<Props, {}> {
  public render() {
    return(
      <table id="CharacterBoard" className={styles.characterBoard}>
        <caption></caption>
          {chars[0].map((_, idx) => {
            return <ColumnStatus isActive={idx === this.props.activeColumn}/>;
          })}
        <tbody>
          {chars.map((row) => {
            return(<tr>
              {row.map((c) => <td className={styles.data}>{c}</td>)}
            </tr>
            );
          })}
        </tbody>
      </table>
    );
  }
}

export default connect(
  (state: State) => state.cursol as Props,
  null,
)(CharacterBoard);
