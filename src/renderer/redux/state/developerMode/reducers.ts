import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../../util";

type Action = _Action<typeof actions>;

const initialState = false;

export const reducer = (state: boolean | undefined, action: Action) => {
  if (action.type === types.SET_ACTIVE) {
    return action.payload.isActive;
  }

  if (state === undefined) {
    return initialState;
  }

  return state;
};
