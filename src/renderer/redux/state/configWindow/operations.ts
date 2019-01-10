import {Dispatch} from "redux";

import * as actions from "./actions";

export const setScanSpeed = (dispatch: Dispatch) => (scanSpeed: number) => {
  dispatch(actions.setScanSpeed(scanSpeed));
};
