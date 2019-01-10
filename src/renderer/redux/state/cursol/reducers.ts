import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import { RootState } from "../..";

import { Action as _Action } from "../../util";

import { MAX_COLUMN_INDEX } from "../../../constant";

export type Action = _Action<typeof actions>;

type State = RootState["cursol"];

const initialState: State = {
  activeColumn: 0,
  mode: "proposed",
};

const increment = (state: number, _: ReturnType<typeof actions.increment>): number => {
  if (state === MAX_COLUMN_INDEX) {
    return initialState.activeColumn;
  }

  return state + 1;
};

const activeColumnReducer = (state: number | undefined, action: Action) => {
  if (state === undefined) {
    return initialState.activeColumn;
  }

  if (action.type === types.INCREMENT) {
    return increment(state, action);
  }
  return state;
};

const modeReducer = (state: State["mode"] | undefined, action: Action) => {
  if (state === undefined) {
    return initialState.mode;
  }

  if (action.type === types.SET_MODE) {
    return action.payload.mode;
  }

  return state;
};

export const reducer = combineReducers({
  activeColumn: activeColumnReducer,
  mode: modeReducer,
});
