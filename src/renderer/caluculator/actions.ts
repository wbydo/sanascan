import {Dispatch} from "redux";

import * as types from "./types";

export interface CaluculatorAction {
  type: string;
  value: number;
}

export const input: (value: number) => CaluculatorAction = (value) => {
  return({
    type: types.INPUT_FIGURE,
    value,
  });
};

export class ActionDispatcher {
  private dispatch: Dispatch<CaluculatorAction>;

  constructor(dispatch: Dispatch<CaluculatorAction>) {
    this.dispatch = dispatch;
  }

  public input: (value: number) => void = (value) => {
    this.dispatch(input(value));
  }
}
