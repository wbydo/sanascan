import { combineReducers } from "redux";

import {Action} from "./actions";
import {MAX_COLUMN_INDEX} from "../views/CharacterBoard";
import * as types from "./types";
import SanaScanError from "../error";

export interface RootState {
  activeColumn: number;
  scanSpeed: number;
  modalIsActive: boolean;
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
// scanSpeed
type SagaState = number;
const initialSagaState: SagaState = 500;

const sagaReducer = (state: number | undefined, action: Action) => {
  if (state === undefined) {
    return initialSagaState;
  }

  if (action.type === types.SET_SCAN_SPEED) {
    if (!("scanSpeed" in action)) {
      throw new TypeError();
    }

    return action.scanSpeed;
  }

  return state;
};

// scanSpeed
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

export const rootReducer = combineReducers({
  activeColumn: characterBoardreducer,
  modalIsActive: modalIsActiveReducer,
  scanSpeed: sagaReducer,
});

// rootReducer
// /////////////////////////////////////////////
