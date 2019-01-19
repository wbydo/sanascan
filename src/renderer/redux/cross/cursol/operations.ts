import { Dispatch } from "redux";

import { actions as cursolActions } from "../../state/cursol";
import { actions as httpActions } from "../../cross/http";

export const changeMode = (dispatch: Dispatch) => (mode: "normal" | "proposal") => {
  dispatch(cursolActions.setMode(mode));

  dispatch(cursolActions.reset());
  dispatch(httpActions.reset());
};
