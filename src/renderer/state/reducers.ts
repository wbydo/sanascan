import { combineReducers } from "redux";

import {Action} from "./actions";
import {MAX_COLUMN_INDEX} from "../views/CharacterBoard";
import * as types from "./types";
import SanaScanError from "../error";

import { cursolReducer } from "./cursol/index";
import { timerReducer } from "./timer/index";

export interface RootState {
  cursol: {
    activeColumn: number;
  };
  modalIsActive: boolean;
  timer: {
    isActive: boolean;
    scanSpeed: number;
  };
}

// /////////////////////////////////////////////
// modalIsActive

const modalIsActiveReducer = (state: boolean | undefined, action: Action) => {
  if (state === undefined) {
    return false;
  }

  if (action.type === types.ACTIVATE_CONFIGURE) {
    return true;
  }

  if (action.type === types.DEACTIVATE_CONFIGURE) {
    return false;
  }

  return state;
};
// modalIsActive
// /////////////////////////////////////////////

// /////////////////////////////////////////////
// rootReducer

const reducer = combineReducers({
  cursol: cursolReducer,
  modalIsActive: modalIsActiveReducer,
  timer: timerReducer,
});

export default reducer;

// rootReducer
// /////////////////////////////////////////////
