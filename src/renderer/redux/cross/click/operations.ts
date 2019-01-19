import { Dispatch } from "redux";

import { actions as httpActions } from "../http";
import { actions as timerActions } from "../timer";

import { actions as cursolActions } from "../../state/cursol";

import { RootState } from "../..";

import { chars } from "../../../constant";

export const click = (dispatch: Dispatch) => (state: RootState) => {
  dispatch(timerActions.kill());

  const mode = state.cursol.mode;
  const direction = state.cursol.direction;
  const col = state.cursol.activeColumn;
  if (mode === "proposal") {
    dispatch(httpActions.sendKey(col));
    dispatch(cursolActions.reset());

  } else if (direction === "column") {
    dispatch(cursolActions.setDirection("row"));

  } else {
    const row = state.cursol.activeRow;
    const key = chars[row][col];
    dispatch(httpActions.sendKey(key));
    dispatch(cursolActions.reset());
  }

  dispatch(timerActions.start());
};
