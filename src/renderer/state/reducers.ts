import { combineReducers } from "redux";

import {Action} from "./actions";
import {MAX_COLUMN_INDEX} from "../views/CharacterBoard";
import * as types from "./types";
import SanaScanError from "../error";

import { timerReducer } from "./timer/index";

export interface RootState {
  activeColumn: number;
  modalIsActive: boolean;
  timer: {
    isActive: boolean;
    scanSpeed: number;
  };
}

// /////////////////////////////////////////////
// activeColumn

type CharacterBoardState = number;

const initialState: number = 0;

const increment = (state: number, action: Action) => {
  if (action.type !== types.INCREMENT) {
    throw new SanaScanError();
  }

  if (state === MAX_COLUMN_INDEX) {
    return initialState;
  }
  return state + 1;
};

const characterBoardreducer = (state: number | undefined, action: Action) => {
  if (state === undefined) {
    return initialState;
  }

  if (action.type === types.INCREMENT) {
    return increment(state, action);
  }
  return state;
};

// activeColumn
// /////////////////////////////////////////////

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
  activeColumn: characterBoardreducer,
  modalIsActive: modalIsActiveReducer,
  timer: timerReducer,
});

export default reducer;

// rootReducer
// /////////////////////////////////////////////
