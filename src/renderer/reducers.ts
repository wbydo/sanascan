import { combineReducers } from "redux";

import {Action} from "./actions";
import CharacterBoard from "./CharacterBoard";
import {MAX_COLUMN_INDEX} from "./CharacterBoard";
import { INCREMENT } from "./types";
import SanaScanError from "./error";

interface RootState {
  activeColumn: number;
  scanSpeed: number;
}

// CharacterBoardReducer
// /////////////////////////////////////////////

type CharacterBoardState = number;

const initialState: number = 0;

const increment = (state: number, action: Action) => {
  if (action.type !== INCREMENT) {
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

  if (action.type === INCREMENT) {
    return increment(state, action);
  }
  return state;
};

// /////////////////////////////////////////////
// CharacterBoardReducer

// /////////////////////////////////////////////
// sagaReducer
type SagaState = number;
const initialSagaState: SagaState = 500;

const sagaReducer = (state: number | undefined, action: Action) => {
  if (state === undefined) {
    return initialSagaState;
  }

// 本来はアクション毎に振り分ける

  return state;
};

// sagaReducer
// /////////////////////////////////////////////

// rootReducer
// /////////////////////////////////////////////

export const rootReducer = combineReducers({
  activeColumn: characterBoardreducer,
  scanSpeed: sagaReducer,
});
// /////////////////////////////////////////////

// rootReducer
