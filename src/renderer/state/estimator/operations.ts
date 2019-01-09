import {Dispatch} from "redux";

import * as actions from "./actions";

export const reset = (dispatch: Dispatch) => () => {
  dispatch(actions.reset());
};

export const sendKey = (dispatch: Dispatch) => (key: number) => {
  dispatch(actions.sendKey(key));
};

export const fetchId = (dispatch: Dispatch) => () => {
  dispatch(actions.fetchId("start"));
};
