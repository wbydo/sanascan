import { combineReducers } from "redux";

import {Action} from "./actions";
import CharacterBoard from "./CharacterBoard";
import {MAX_COLUMN_INDEX} from "./CharacterBoard";
import { INCREMENT } from "./types";
import SanaScanError from "./error";

interface RootState {
  activeColumn: number;
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

// rootReducer
// /////////////////////////////////////////////

export const rootReducer = combineReducers<RootState>({
  activeColumn: characterBoardreducer,
});
// /////////////////////////////////////////////

// rootReducer
