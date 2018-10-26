import {CaluculatorAction} from "./actions";
import * as types from "./types";
import {CaluculatorError} from "./error";

export interface CaluculatorState {
  display: number;
}

type Reducer = (state: CaluculatorState | undefined, action: CaluculatorAction) => CaluculatorState;

const initialState: CaluculatorState = {
  display: 0,
};

export const reducer: Reducer = (state, action) => {
  if (state === undefined) {
    return initialState;
  }
  if (action.type === types.INPUT_FIGURE) {
    const prevDisplay = state.display;
    const nextDisplay = prevDisplay * 10 + action.value;
    return {display: nextDisplay};
  }
  throw new CaluculatorError();
};
