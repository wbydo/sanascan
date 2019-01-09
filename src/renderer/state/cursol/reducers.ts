import { combineReducers } from "redux";

import * as actions from "./actions";
import * as types from "./types";

import SanaScanError from "../../error";

import {MAX_COLUMN_INDEX} from "../../constant";

import { Action as _Action } from "../util";
export type Action = _Action<typeof actions>;

interface RootState {
  activeColumn: number;
}

const initialState: RootState = {
  activeColumn: 0,
};

const increment = (state: number, action: Action): number => {
  if (action.type !== types.INCREMENT) {
    throw new SanaScanError();
  }

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

const reducer = combineReducers({
  activeColumn: activeColumnReducer,
});

export default reducer;
