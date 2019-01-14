import * as actions from "./actions";
import * as types from "./types";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;

import { RootState } from "../../";

type State = RootState["developerMode"];

const initialState: State = {
  isActive: true,
};

export const reducer = (state: State | undefined, action: Action): State => {
  if (action.type === types.SET_ACTIVE) {
    return { isActive: action.payload.isActive };
  }

  if (state === undefined) {
    return initialState;
  }

  return state;
};
