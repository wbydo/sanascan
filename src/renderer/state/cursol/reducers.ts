import { combineReducers } from "redux";

import { Action } from "./actions";
import * as types from "./types";

import {MAX_COLUMN_INDEX} from "../../views/CharacterBoard";

interface RootState {
  activeColumn: number;
}

const initialState: RootState = {
  activeColumn: 0,
};

const activeColumnReducer = (state: number | undefined, action: Action) => {
  if (state === undefined || state === MAX_COLUMN_INDEX) {
    return initialState.activeColumn;
  }

  if (action.type === types.INCREMENT) {
    return state + 1;
  }
  return state;
};

const reducer = combineReducers({
  activeColumn: activeColumnReducer,
});

export default reducer;
